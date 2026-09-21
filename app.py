import streamlit as st
import pandas as pd
from datetime import datetime, date
from streamlit_gsheets import GSheetsConnection
import io

# ReportLab Imports for Branded PDF Generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sidharth Shutter & Automation - Enterprise CRM",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1ajDjxHOqfQw_7qRNvMT4I6q9jujJ6tjPqe6M4kOdoIo/edit"

# ---------------------------------------------------------
# CUSTOM CSS: STYLING & ACCENTS
# ---------------------------------------------------------
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; }
    header[data-testid="stHeader"] { background-color: #F8FAFC !important; }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #164194 !important;
        border-right: 2px solid #0e2d6b !important;
        padding-top: 20px !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        font-family: 'Segoe UI', Roboto, sans-serif !important;
    }

    /* Radio Inputs Fix */
    div[data-testid="stRadio"] label {
        font-size: 15px !important;
        font-weight: 600 !important;
        padding: 6px 10px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        background-color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 50% !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] > div:first-child {
        background-color: #00A859 !important;
        border: 3px solid #FFFFFF !important;
    }

    /* Logout Button */
    div[data-testid="stSidebar"] div.stButton > button {
        background-color: #00A859 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        width: 100% !important;
    }
    div[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #008f4c !important;
    }

    /* Form & Metric Cards */
    div[data-testid="stForm"], .saas-card {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        margin-bottom: 20px !important;
    }

    .metric-card {
        background-color: #FFFFFF !important;
        border: 2px solid #164194 !important;
        border-radius: 10px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 12px rgba(22, 65, 148, 0.08) !important;
        margin-bottom: 10px !important;
    }
    .metric-card-green { border-color: #00A859 !important; }
    .metric-card h5 {
        color: #164194 !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        margin: 0 0 4px 0 !important;
        text-transform: uppercase;
    }
    .metric-card-green h5 { color: #00A859 !important; }
    .metric-card h3 {
        color: #0F172A !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        margin: 0 !important;
    }

    /* Action Queue Card */
    .queue-card {
        background-color: #FFFFFF !important;
        border-left: 5px solid #EF4444 !important;
        border-top: 1px solid #CBD5E1 !important;
        border-right: 1px solid #CBD5E1 !important;
        border-bottom: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
    }

    /* Form Inputs Styling */
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1.5px solid #164194 !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] > div > div:last-child {
        background-color: #164194 !important;
    }
    div[data-baseweb="select"] svg { fill: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATABASE CONNECTIVITY HELPERS
# ---------------------------------------------------------
def get_connection():
    try:
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception:
        return None

def load_sheet(worksheet_name):
    conn = get_connection()
    if conn:
        try:
            return conn.read(spreadsheet=SPREADSHEET_URL, worksheet=worksheet_name, ttl=0)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

def save_sheet(worksheet_name, df_updated):
    conn = get_connection()
    if conn:
        try:
            conn.update(spreadsheet=SPREADSHEET_URL, worksheet=worksheet_name, data=df_updated)
            return True
        except Exception as e:
            st.error(f"Failed to update sheet: {e}")
            return False
    return False

# Master Configuration Options
PRODUCT_LIST = [
    "Motorised Swing Gates", "Motorised Sliding Gates", "Automatic Rolling Shutters",
    "Dock Leveller", "Boom Barriers", "Rolling Shutter motor Part", "Spare Part"
]
SOURCE_LIST = ["Marketing Team", "Whats App", "India Mart", "Sales Email", "Phone Call", "Reference"]
SALESPERSONS = ["Mansingh Rathore", "Sidharth Jain", "Jeevan Sharma", "Deepak Sethiya", "Rishabh Jain", "Bhavya Jain"]
CLIENT_TYPES = ["New Buy", "Dealer", "Architect", "Contractor", "Service", "OEM"]
TEAM_MEMBERS = ["Pooja", "Dolly", "Albert", "Rishabh", "Bhavya", "Other"]

# ---------------------------------------------------------
# PDF GENERATOR ENGINE (REPORTLAB)
# ---------------------------------------------------------
def generate_quotation_pdf(quote_details):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    # Brand Header Colors
    navy = colors.HexColor("#164194")
    green = colors.HexColor("#00A859")
    dark_text = colors.HexColor("#0F172A")

    title_style = ParagraphStyle('TitleStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=navy)
    subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=green)
    normal_style = ParagraphStyle('NormStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=dark_text)
    bold_style = ParagraphStyle('BoldStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=dark_text)

    # Header Row
    header_data = [
        [
            Paragraph("<b>SIDHARTH SHUTTER & AUTOMATION</b>", title_style),
            Paragraph("<b>QUOTATION</b><br><font size=8 color='#64748B'>Date: " + datetime.now().strftime('%d-%b-%Y') + "</font>", title_style)
        ],
        [
            Paragraph("Industrial Shutters, Automatic Gates & Automation Solutions", subtitle_style),
            Paragraph(f"<b>Quote No:</b> {quote_details.get('Quotation Number', 'SSA/2026/01')}", bold_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[340, 200])
    header_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(header_table)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=green, spaceAfter=15))

    # Client & Project Block
    client_info = [
        [Paragraph("<b>CUSTOMER DETAILS</b>", ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=11, textColor=navy)),
         Paragraph("<b>PROJECT SUMMARY</b>", ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=11, textColor=navy))],
        [
            Paragraph(f"<b>Client:</b> {quote_details.get('Client Name', '')}<br>"
                      f"<b>Company:</b> {quote_details.get('Company Name', 'N/A')}<br>"
                      f"<b>Phone:</b> {quote_details.get('Customer Contact Number', '')}<br>"
                      f"<b>City:</b> {quote_details.get('City', '')}", normal_style),
            Paragraph(f"<b>Client ID:</b> {quote_details.get('Client  ID', '')}<br>"
                      f"<b>Assigned Rep:</b> {quote_details.get('Assigned Salesperson', '')}<br>"
                      f"<b>Source:</b> {quote_details.get('Source', '')}", normal_style)
        ]
    ]
    info_table = Table(client_info, colWidths=[270, 270])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1"))
    ]))
    story.append(info_table)
    story.append(Spacer(1, 15))

    # Itemized Pricing Table
    qty = float(quote_details.get('Quantity', 1))
    total_amt = float(quote_details.get('Qut. Amount', 0))
    unit_price = total_amt / qty if qty > 0 else total_amt
    gst_amt = total_amt * 0.18
    grand_total = total_amt + gst_amt

    items_data = [
        [Paragraph("<b>Item / Specification</b>", bold_style), Paragraph("<b>Qty</b>", bold_style), Paragraph("<b>Unit Price (₹)</b>", bold_style), Paragraph("<b>Total (₹)</b>", bold_style)],
        [Paragraph(f"<b>{quote_details.get('Product ', 'Automation Equipment')}</b><br><font size=8 color='#475569'>{quote_details.get('Remarks', '')}</font>", normal_style),
         Paragraph(str(qty), normal_style), Paragraph(f"{unit_price:,.2f}", normal_style), Paragraph(f"{total_amt:,.2f}", normal_style)],
        ["", "", Paragraph("<b>Sub Total:</b>", normal_style), Paragraph(f"₹{total_amt:,.2f}", normal_style)],
        ["", "", Paragraph("<b>GST (18%):</b>", normal_style), Paragraph(f"₹{gst_amt:,.2f}", normal_style)],
        ["", "", Paragraph("<b>Grand Total:</b>", bold_style), Paragraph(f"<b>₹{grand_total:,.2f}</b>", bold_style)]
    ]

    items_table = Table(items_data, colWidths=[280, 50, 100, 110])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,1), 1, colors.HexColor("#CBD5E1")),
        ('LINEBELOW', (2,2), (-1,-1), 1, colors.HexColor("#E2E8F0"))
    ]))
    story.append(items_table)
    story.append(Spacer(1, 20))

    # Terms & Conditions
    terms_text = (
        "<b>Terms & Conditions:</b><br>"
        "1. 50% advance payment with purchase order; balance 50% prior to dispatch.<br>"
        "2. Delivery timeline: 10-15 working days from order confirmation.<br>"
        "3. Warranty: 12 Months manufacturer warranty against manufacturing defects.<br>"
        "4. Taxes: GST @ 18% extra as applicable."
    )
    story.append(Paragraph(terms_text, ParagraphStyle('Terms', fontName='Helvetica', fontSize=8, leading=12, textColor=colors.HexColor("#475569"))))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# ---------------------------------------------------------
# AUTHENTICATION & USER ROLES
# ---------------------------------------------------------
USERS = {
    "admin": ("admin123", "Admin", "System Administrator"),
    "mansingh": ("sales123", "Salesperson", "Mansingh Rathore"),
    "sidharth": ("sales123", "Salesperson", "Sidharth Jain"),
    "pooja": ("backoffice123", "Back-Office", "Pooja"),
    "dolly": ("backoffice123", "Back-Office", "Dolly"),
    "ops": ("ops123", "Operations", "Operations Team")
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.user_display_name = None
    st.session_state.username = None

def login_form():
    st.markdown("<br>", unsafe_allow_html=True)
    c1, col, c2 = st.columns([1, 1.2, 1])
    with col:
        with st.form("login_form"):
            try:
                st.image("Company Logo.jpeg", use_container_width=True)
            except Exception:
                st.markdown("<h2 style='text-align: center; color: #164194; font-weight:800;'>🏭 SIDHARTH SHUTTER</h2>", unsafe_allow_html=True)
            
            st.markdown("<p style='text-align: center; color: #164194; font-weight: 700; font-size: 16px;'>Sales CRM & Workflow Portal</p>", unsafe_allow_html=True)
            user_input = st.text_input("Username").strip().lower()
            pass_input = st.text_input("Password", type="password")
            submit = st.form_submit_button("🔑 Login to Dashboard", use_container_width=True)

            if submit:
                if user_input in USERS and USERS[user_input][0] == pass_input:
                    st.session_state.authenticated = True
                    st.session_state.username = user_input
                    st.session_state.user_role = USERS[user_input][1]
                    st.session_state.user_display_name = USERS[user_input][2]
                    st.rerun()
                else:
                    st.error("Invalid Username or Password.")

if not st.session_state.authenticated:
    login_form()
    st.stop()

# ---------------------------------------------------------
# DYNAMIC ROLE-BASED SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    try:
        st.image("Company Logo.jpeg", use_container_width=True)
    except Exception:
        st.write("🏭 **SSA CRM**")
        
    st.markdown(f"<h3 style='margin-bottom:2px; font-size: 18px !important;'>👋 {st.session_state.user_display_name}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #38BDF8 !important; font-weight:700; font-size:14px !important;'>Role: {st.session_state.user_role}</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Custom Navigation Per Role
    if st.session_state.user_role == "Salesperson":
        menu = st.radio("NAVIGATION", ["⚡ Follow-up Queue & Workday", "📥 Add New Lead", "📄 Quotation Generator", "🔍 Client Inspector"])
    elif st.session_state.user_role == "Back-Office":
        menu = st.radio("NAVIGATION", ["📄 Quotation Generator & Convert", "⚡ Follow-up Queue & Workday", "📞 Follow-up Master", "🔍 Client Inspector"])
    elif st.session_state.user_role == "Operations":
        menu = st.radio("NAVIGATION", ["⚙️ Process Order Execution", "🔍 Client Inspector"])
    else: # Admin / Executive
        menu = st.radio("NAVIGATION", [
            "🏆 Sales Leaderboard & Analytics",
            "⚡ Follow-up Queue & Workday",
            "📥 Add New Lead",
            "📄 Quotation Generator & Convert",
            "📞 Follow-up Master",
            "⚙️ Process Order Execution",
            "🔍 Client Inspector"
        ])

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ---------------------------------------------------------
# MODULE 1: AUTOMATED FOLLOW-UP QUEUE & OUTCOME BUTTONS
# ---------------------------------------------------------
if menu in ["⚡ Follow-up Queue & Workday", "📞 Follow-up Master"]:
    st.markdown(f"<div class='main-header'>⚡ Active Follow-up Queue: {st.session_state.user_display_name}</div>", unsafe_allow_html=True)

    df_follow = load_sheet("Quotation Follow Up Tracker")

    if not df_follow.empty:
        # Filter reps if logged in as Salesperson
        if st.session_state.user_role == "Salesperson" and "Assigned Salesperson" in df_follow.columns:
            queue_df = df_follow[df_follow["Assigned Salesperson"] == st.session_state.user_display_name]
        else:
            queue_df = df_follow

        active_queue = queue_df[queue_df["Follow-up Status"] != "Closed / Converted"] if "Follow-up Status" in queue_df.columns else queue_df

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='metric-card'><h5>Pending Calls</h5><h3>{len(active_queue)}</h3></div>", unsafe_allow_html=True)
        with c2:
            approved_count = len(queue_df[queue_df["Follow-up Status"] == "Approved"]) if "Follow-up Status" in queue_df.columns else 0
            st.markdown(f"<div class='metric-card metric-card-green'><h5>Approved Deals</h5><h3>{approved_count}</h3></div>", unsafe_allow_html=True)
        with c3:
            val = pd.to_numeric(queue_df['Quotation Amount'], errors='coerce').sum() if 'Quotation Amount' in queue_df.columns else 0
            st.markdown(f"<div class='metric-card'><h5>Queue Value</h5><h3>₹{val:,.0f}</h3></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🎯 Pending Action Items (1-Click Logging)</div>", unsafe_allow_html=True)

        if not active_queue.empty:
            for idx, row in active_queue.iterrows():
                client_id = row.get("Client ID", f"Ref-{idx}")
                client_name = row.get("Client Name", "Client")
                phone = row.get("Contact Number", "N/A")
                amt = row.get("Quotation Amount", "0")
                quote_no = row.get("Quotation Number", "N/A")

                st.markdown(f"""
                <div class='queue-card'>
                    <b style='color:#164194; font-size:16px;'>{client_name}</b> | <span style='color:#64748B;'>Quote: {quote_no}</span><br>
                    📞 <b>Contact:</b> {phone} | 💰 <b>Amount:</b> ₹{amt} | 👤 <b>Rep:</b> {row.get('Assigned Salesperson', 'Unassigned')}
                </div>
                """, unsafe_allow_html=True)

                b1, b2, b3, b4 = st.columns(4)
                with b1:
                    if st.button("✅ Connected - Interested", key=f"int_{idx}"):
                        df_follow.at[idx, "Follow-up Status"] = "Interested - Followup Scheduled"
                        df_follow.at[idx, "Last Follow-up Date"] = datetime.now().strftime("%Y-%m-%d")
                        save_sheet("Quotation Follow Up Tracker", df_follow)
                        st.success("Updated: Scheduled next follow-up.")
                        st.rerun()
                with b2:
                    if st.button("⏳ Busy - Reschedule", key=f"res_{idx}"):
                        df_follow.at[idx, "Follow-up Status"] = "Rescheduled"
                        df_follow.at[idx, "Last Follow-up Date"] = datetime.now().strftime("%Y-%m-%d")
                        save_sheet("Quotation Follow Up Tracker", df_follow)
                        st.warning("Updated: Marked as Rescheduled.")
                        st.rerun()
                with b3:
                    if st.button("🎉 Approved & Closed", key=f"app_{idx}"):
                        df_follow.at[idx, "Follow-up Status"] = "Closed / Converted"
                        df_follow.at[idx, "Last Follow-up Date"] = datetime.now().strftime("%Y-%m-%d")
                        save_sheet("Quotation Follow Up Tracker", df_follow)
                        st.balloons()
                        st.success("Deal Won! Closed successfully.")
                        st.rerun()
                with b4:
                    if st.button("❌ Lost / Dropped", key=f"lost_{idx}"):
                        df_follow.at[idx, "Follow-up Status"] = "Lost"
                        df_follow.at[idx, "Last Follow-up Date"] = datetime.now().strftime("%Y-%m-%d")
                        save_sheet("Quotation Follow Up Tracker", df_follow)
                        st.error("Updated: Marked as Lost.")
                        st.rerun()
                st.markdown("---")
        else:
            st.info("🎉 No pending follow-ups in your queue!")

    st.markdown("<div class='section-title'>📋 Full Follow-up Database</div>", unsafe_allow_html=True)
    st.dataframe(df_follow, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# MODULE 2: BRANDED PDF QUOTATION GENERATOR & CONVERT
# ---------------------------------------------------------
elif menu in ["📄 Quotation Generator", "📄 Quotation Generator & Convert"]:
    st.markdown("<div class='main-header'>📄 Branded PDF Quotation Generator</div>", unsafe_allow_html=True)

    df_quotes = load_sheet("Quotation Sheet")
    df_leads = load_sheet("Leads Data")

    tab1, tab2 = st.tabs(["⚡ Convert Lead to Quote & PDF", "📋 Existing Quotation PDFs"])

    with tab1:
        if not df_leads.empty:
            selected_client = st.selectbox("Select Lead Record:", df_leads["Client ID"].tolist() if "Client ID" in df_leads.columns else [])
            if selected_client:
                lead_row = df_leads[df_leads["Client ID"] == selected_client].iloc[0]

                with st.form("pdf_quote_form"):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        c_name = st.text_input("Client Name", value=str(lead_row.get("Client Name", "")))
                        comp_name = st.text_input("Company Name", value=str(lead_row.get("Company Name", "")))
                    with c2:
                        phone = st.text_input("Contact Number", value=str(lead_row.get("Number", "")))
                        city = st.text_input("City", value=str(lead_row.get("City", "")))
                    with c3:
                        quote_no = st.text_input("Quotation Number", value=f"SSA/2026/{datetime.now().strftime('%M%S')}")
                        product = st.selectbox("Product Requirement", PRODUCT_LIST, index=0)

                    c4, c5 = st.columns(2)
                    with c4:
                        qty = st.number_input("Quantity", min_value=1, value=int(lead_row.get("Qty", 1)))
                        amt = st.number_input("Subtotal Amount (₹)", min_value=1000, step=5000, value=45000)
                    with c5:
                        assigned_sp = st.selectbox("Salesperson", SALESPERSONS)
                        remarks = st.text_area("Quotation Remarks", value=f"Supply & installation of {product}")

                    generate_btn = st.form_submit_button("📄 Issue Quotation & Build PDF", use_container_width=True)

                    if generate_btn:
                        quote_payload = {
                            "Client  ID": selected_client,
                            "Client Name": c_name,
                            "Company Name": comp_name,
                            "Customer Contact Number": phone,
                            "City": city,
                            "Quotation Number": quote_no,
                            "Product ": product,
                            "Quantity": qty,
                            "Qut. Amount": amt,
                            "Assigned Salesperson": assigned_sp,
                            "Source": lead_row.get("Source", "Marketing"),
                            "Remarks": remarks
                        }

                        # Save quote row to Master Quotation Sheet
                        conn = get_connection()
                        if conn:
                            df_q_existing = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="Quotation Sheet")
                            df_q_updated = pd.concat([df_q_existing, pd.DataFrame([quote_payload])], ignore_index=True)
                            conn.update(spreadsheet=SPREADSHEET_URL, worksheet="Quotation Sheet", data=df_q_updated)

                        # Generate PDF
                        pdf_bytes = generate_quotation_pdf(quote_payload)
                        st.success(f"✅ Quotation {quote_no} Generated Successfully!")

                        st.download_button(
                            label="📥 Download Official PDF Quotation",
                            data=pdf_bytes,
                            file_name=f"{quote_no.replace('/', '_')}_{c_name}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

    with tab2:
        st.markdown("<div class='section-title'>📋 Issued Quotation Registry</div>", unsafe_allow_html=True)
        if not df_quotes.empty:
            st.dataframe(df_quotes, use_container_width=True, hide_index=True)

            selected_q_no = st.selectbox("Select Issued Quote to Re-generate PDF:", df_quotes["Quotation Number"].dropna().unique() if "Quotation Number" in df_quotes.columns else [])
            if selected_q_no and st.button("📄 Generate PDF for Selected Quote"):
                q_row = df_quotes[df_quotes["Quotation Number"] == selected_q_no].iloc[0].to_dict()
                pdf_bytes = generate_quotation_pdf(q_row)
                st.download_button(
                    label=f"📥 Download PDF ({selected_q_no})",
                    data=pdf_bytes,
                    file_name=f"{selected_q_no.replace('/', '_')}.pdf",
                    mime="application/pdf"
                )

# ---------------------------------------------------------
# MODULE 3: SALES LEADERBOARD & ANALYTICS CHARTS (ADMIN VIEW)
# ---------------------------------------------------------
elif menu == "🏆 Sales Leaderboard & Analytics":
    st.markdown("<div class='main-header'>🏆 Sales Performance & Revenue Leaderboard</div>", unsafe_allow_html=True)

    df_leads = load_sheet("Leads Data")
    df_quotes = load_sheet("Quotation Sheet")
    df_follow = load_sheet("Quotation Follow Up Tracker")

    # Executive KPI Overview
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='metric-card'><h5>Total Inquiries</h5><h3>{len(df_leads)}</h3></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card metric-card-green'><h5>Quotations Sent</h5><h3>{len(df_quotes)}</h3></div>", unsafe_allow_html=True)
    with c3:
        val = pd.to_numeric(df_quotes['Qut. Amount'], errors='coerce').sum() if not df_quotes.empty and 'Qut. Amount' in df_quotes.columns else 0
        st.markdown(f"<div class='metric-card'><h5>Pipeline Value</h5><h3>₹{val:,.0f}</h3></div>", unsafe_allow_html=True)
    with c4:
        closed_deals = len(df_follow[df_follow["Follow-up Status"] == "Closed / Converted"]) if not df_follow.empty and "Follow-up Status" in df_follow.columns else 0
        st.markdown(f"<div class='metric-card metric-card-green'><h5>Won Orders</h5><h3>{closed_deals}</h3></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("<div class='section-title'>🥇 Rep Leaderboard (By Quoted Value)</div>", unsafe_allow_html=True)
        if not df_quotes.empty and "Assigned Salesperson" in df_quotes.columns:
            df_quotes['Numeric_Amt'] = pd.to_numeric(df_quotes['Qut. Amount'], errors='coerce').fillna(0)
            rep_summary = df_quotes.groupby("Assigned Salesperson")["Numeric_Amt"].agg(['sum', 'count']).reset_index()
            rep_summary.columns = ["Salesperson", "Total Revenue (₹)", "Quotes Issued"]
            rep_summary = rep_summary.sort_values(by="Total Revenue (₹)", ascending=False)
            st.dataframe(rep_summary, use_container_width=True, hide_index=True)
        else:
            st.info("No sales rep activity recorded yet.")

    with col_right:
        st.markdown("<div class='section-title'>📊 Lead Distribution by Source</div>", unsafe_allow_html=True)
        if not df_leads.empty and "Source" in df_leads.columns:
            source_counts = df_leads["Source"].value_counts().reset_index()
            source_counts.columns = ["Lead Source", "Total Leads"]
            st.bar_chart(data=source_counts, x="Lead Source", y="Total Leads", color="#164194")
        else:
            st.info("No lead source data available.")

    st.markdown("<div class='section-title'>📦 Product Demand Breakdown</div>", unsafe_allow_html=True)
    if not df_leads.empty and "Product " in df_leads.columns:
        prod_counts = df_leads["Product "].value_counts().reset_index()
        prod_counts.columns = ["Product Category", "Inquiries"]
        st.bar_chart(data=prod_counts, x="Product Category", y="Inquiries", color="#00A859")

# ---------------------------------------------------------
# OTHER EXISTING MODULES
# ---------------------------------------------------------
elif menu == "📥 Add New Lead":
    st.markdown("<div class='main-header'>📥 Lead Capture Portal</div>", unsafe_allow_html=True)
    with st.form("add_lead_form", clear_on_submit=True):
        st.markdown("<div class='section-title'>👤 Client Details</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            client_name = st.text_input("Client Name *")
            company_name = st.text_input("Company Name *")
        with c2:
            number = st.text_input("Contact Number *")
            email = st.text_input("Email ID")
        with c3:
            city = st.text_input("City")
            state = st.text_input("State")

        st.markdown("<div class='section-title'>📦 Requirement Details</div>", unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)
        with c4:
            product = st.selectbox("Product *", PRODUCT_LIST)
            qty = st.number_input("Quantity", min_value=1, value=1)
        with c5:
            source = st.selectbox("Source", SOURCE_LIST)
            client_type = st.selectbox("Client Type", CLIENT_TYPES)
        with c6:
            assigned_sp = st.selectbox("Assigned Rep", SALESPERSONS)
            handle_by = st.selectbox("Handled By", TEAM_MEMBERS)

        remarks = st.text_area("Initial Remarks", height=80)
        submit_lead = st.form_submit_button("💾 Save Lead", use_container_width=True)

        if submit_lead:
            if not client_name or not number:
                st.error("Please fill in Client Name and Number.")
            else:
                client_id = f"SSA-{datetime.now().strftime('%b-%y')}-{datetime.now().strftime('%M%S')}"
                new_lead = {
                    "Sr. No": len(load_sheet("Leads Data")) + 1,
                    "Client ID": client_id,
                    "Date Stamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Client Name": client_name,
                    "Company Name": company_name,
                    "Number": number,
                    "Email": email,
                    "Product ": product,
                    "Qty": qty,
                    "City": city,
                    "State": state,
                    "Source": source,
                    "Assigned Salesperson": assigned_sp,
                    "Type of client": client_type,
                    "Quotation Status": "Not Sent",
                    "Leads Handle By": handle_by,
                    "Remarks": remarks
                }
                conn = get_connection()
                if conn:
                    df_ex = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="Leads Data")
                    df_up = pd.concat([df_ex, pd.DataFrame([new_lead])], ignore_index=True)
                    conn.update(spreadsheet=SPREADSHEET_URL, worksheet="Leads Data", data=df_up)
                    st.success(f"✅ Lead Created! Client ID: {client_id}")

elif menu == "⚙️ Process Order Execution":
    st.markdown("<div class='main-header'>⚙️ Operational & Factory Execution</div>", unsafe_allow_html=True)
    st.dataframe(load_sheet("Process Order"), use_container_width=True, hide_index=True)

elif menu == "🔍 Client Inspector":
    st.markdown("<div class='main-header'>🔍 Client 360 Degree Inspector</div>", unsafe_allow_html=True)
    df_leads = load_sheet("Leads Data")
    if not df_leads.empty and "Client ID" in df_leads.columns:
        cid = st.selectbox("Select Client ID:", df_leads["Client ID"].dropna().unique())
        if cid:
            st.dataframe(df_leads[df_leads["Client ID"] == cid], use_container_width=True, hide_index=True)
