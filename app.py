import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import io

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
# SCOPED CSS ENGINE (FIXED INVISIBLE TEXT & DISTORTED LAYOUT)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Global Page Background */
    .stApp, header[data-testid="stHeader"] { 
        background-color: #F8FAFC !important; 
    }

    /* ---------------------------------------------------------
       1. SIDEBAR NAVIGATION STYLING
       --------------------------------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #164194 !important;
        border-right: 2px solid #0e2d6b !important;
        padding-top: 15px !important;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        font-family: 'Segoe UI', Roboto, sans-serif !important;
    }

    /* Radio Button Navigation Labels */
    div[data-testid="stRadio"] label {
        font-size: 14px !important;
        font-weight: 600 !important;
        padding: 6px 10px !important;
        margin-bottom: 2px !important;
        border-radius: 6px !important;
    }
    div[data-testid="stRadio"] label:hover {
        background-color: rgba(255, 255, 255, 0.15) !important;
    }

    /* Radio Selection Indicator */
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        background-color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 50% !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] > div:first-child {
        background-color: #00A859 !important;
        border: 3px solid #FFFFFF !important;
    }

    /* Sidebar Logout Button */
    div[data-testid="stSidebar"] div.stButton > button {
        background-color: #00A859 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        padding: 8px 16px !important;
        width: 100% !important;
    }
    div[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #008f4c !important;
    }

    /* ---------------------------------------------------------
       2. MAIN CONTENT AREA TYPOGRAPHY & HEADERS (FIX FOR BLANK TEXT)
       --------------------------------------------------------- */
    .stMainBlockContainer h1, 
    .stMainBlockContainer h2, 
    .stMainBlockContainer h3, 
    .stMainBlockContainer h4, 
    .stMainBlockContainer p, 
    .stMainBlockContainer span, 
    .stMainBlockContainer div {
        color: #0F172A;
    }

    .main-header {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #164194 !important;
        margin-bottom: 15px !important;
        border-bottom: 3px solid #00A859 !important;
        padding-bottom: 8px !important;
    }

    .section-title {
        color: #164194 !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        margin-top: 15px !important;
        margin-bottom: 10px !important;
        border-bottom: 1.5px solid #CBD5E1 !important;
        padding-bottom: 4px !important;
    }

    /* ---------------------------------------------------------
       3. METRIC CARDS & QUEUE CARDS
       --------------------------------------------------------- */
    .metric-card {
        background-color: #FFFFFF !important;
        border: 2px solid #164194 !important;
        border-radius: 8px !important;
        padding: 14px 18px !important;
        box-shadow: 0 4px 10px rgba(22, 65, 148, 0.06) !important;
        margin-bottom: 10px !important;
    }
    .metric-card-green { 
        border-color: #00A859 !important; 
    }
    .metric-card h5 {
        color: #164194 !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        margin: 0 0 4px 0 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card-green h5 { 
        color: #00A859 !important; 
    }
    .metric-card h3 {
        color: #0F172A !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        margin: 0 !important;
    }

    .queue-card {
        background-color: #FFFFFF !important;
        border-left: 5px solid #164194 !important;
        border-top: 1px solid #CBD5E1 !important;
        border-right: 1px solid #CBD5E1 !important;
        border-bottom: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        padding: 14px !important;
        margin-bottom: 10px !important;
    }

    /* ---------------------------------------------------------
       4. TABS STYLING FIX
       --------------------------------------------------------- */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 6px 6px 0 0 !important;
        padding: 8px 16px !important;
    }
    button[data-baseweb="tab"] div p {
        color: #164194 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }
    button[aria-selected="true"] {
        border-bottom: 3px solid #00A859 !important;
        background-color: #FFFFFF !important;
    }
    button[aria-selected="true"] div p {
        color: #00A859 !important;
    }

    /* ---------------------------------------------------------
       5. FORM & INPUT CONTROLS STYLING
       --------------------------------------------------------- */
    div[data-testid="stForm"], .saas-card {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important;
        padding: 20px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
        margin-bottom: 15px !important;
    }

    .stMainBlockContainer label, .stMainBlockContainer label * {
        color: #164194 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }

    div[data-baseweb="input"], 
    div[data-baseweb="textarea"], 
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1.5px solid #164194 !important;
        border-radius: 6px !important;
        color: #0F172A !important;
    }

    div[data-baseweb="select"] > div > div:last-child {
        background-color: #164194 !important;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
    }
    div[data-baseweb="select"] svg { fill: #FFFFFF !important; }

    /* Main Area Buttons */
    .stMainBlockContainer .stButton>button, 
    div[data-testid="stFormSubmitButton"]>button {
        background-color: #164194 !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        border: none !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        padding: 8px 20px !important;
    }
    .stMainBlockContainer .stButton>button:hover, 
    div[data-testid="stFormSubmitButton"]>button:hover {
        background-color: #00A859 !important;
    }

    /* Dataframe Container */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important;
        padding: 6px !important;
    }
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
# PDF GENERATOR ENGINE
# ---------------------------------------------------------
def generate_quotation_pdf(quote_details):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
    except ImportError:
        st.error("The ReportLab library is missing. Please ensure 'reportlab' is added to requirements.txt.")
        return None

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    navy = colors.HexColor("#164194")
    green = colors.HexColor("#00A859")
    dark_text = colors.HexColor("#0F172A")

    title_style = ParagraphStyle('TitleStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=navy)
    subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=green)
    normal_style = ParagraphStyle('NormStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=dark_text)
    bold_style = ParagraphStyle('BoldStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=dark_text)

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
            
            st.markdown("<p style='text-align: center; color: #164194; font-weight: 700; font-size: 15px;'>Sales CRM & Workflow Portal</p>", unsafe_allow_html=True)
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
        
    st.markdown(f"<h3 style='margin-bottom:2px; font-size: 18px !important; font-weight:700;'>👋 {st.session_state.user_display_name}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #38BDF8 !important; font-weight:700; font-size:13px !important;'>Role: {st.session_state.user_role}</p>", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.user_role == "Salesperson":
        menu = st.radio("NAVIGATION", ["⚡ Follow-up Queue & Workday", "📥 Add New Lead", "📄 Quotation Generator", "🔍 Client Inspector"])
    elif st.session_state.user_role == "Back-Office":
        menu = st.radio("NAVIGATION", ["📄 Quotation Generator & Convert", "⚡ Follow-up Queue & Workday", "📞 Follow-up Master", "🔍 Client Inspector"])
    elif st.session_state.user_role == "Operations":
        menu = st.radio("NAVIGATION", ["⚙️ Process Order Execution", "🔍 Client Inspector"])
    else: # Admin
        menu = st.radio("NAVIGATION", [
            "📈 Admin Performance & Progress Control",
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
# ADMIN PERFORMANCE & PROGRESS CONTROL MODULE
# ---------------------------------------------------------
if menu == "📈 Admin Performance & Progress Control":
    st.markdown("<div class='main-header'>📈 Executive Employee Performance & Operational Progress</div>", unsafe_allow_html=True)

    df_leads = load_sheet("Leads Data")
    df_quotes = load_sheet("Quotation Sheet")
    df_follow = load_sheet("Quotation Follow Up Tracker")
    df_orders = load_sheet("Process Order")

    tab_perf, tab_prog = st.tabs(["👤 Employee Performance Tracker", "⚙️ Work & Operations Progress"])

    with tab_perf:
        st.markdown("<div class='section-title'>📊 Salesperson Activity & Performance Matrix</div>", unsafe_allow_html=True)

        if not df_leads.empty and "Assigned Salesperson" in df_leads.columns:
            leads_per_rep = df_leads["Assigned Salesperson"].value_counts().reset_index()
            leads_per_rep.columns = ["Salesperson", "Total Leads Assigned"]

            if not df_quotes.empty and "Assigned Salesperson" in df_quotes.columns:
                quotes_per_rep = df_quotes.groupby("Assigned Salesperson").agg(
                    Quotes_Sent=('Quotation Number', 'count'),
                    Quoted_Value=('Qut. Amount', lambda x: pd.to_numeric(x, errors='coerce').sum())
                ).reset_index()

                perf_matrix = pd.merge(leads_per_rep, quotes_per_rep, on="Salesperson", how="left").fillna(0)
            else:
                perf_matrix = leads_per_rep
                perf_matrix["Quotes_Sent"] = 0
                perf_matrix["Quoted_Value"] = 0

            if not df_follow.empty and "Assigned Salesperson" in df_follow.columns and "Follow-up Status" in df_follow.columns:
                closed_df = df_follow[df_follow["Follow-up Status"] == "Closed / Converted"]
                closed_per_rep = closed_df.groupby("Assigned Salesperson").size().reset_index(name="Deals_Won")
                perf_matrix = pd.merge(perf_matrix, closed_per_rep, on="Salesperson", how="left").fillna(0)
            else:
                perf_matrix["Deals_Won"] = 0

            st.dataframe(perf_matrix, use_container_width=True, hide_index=True)

            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("<div class='section-title'>📈 Total Inquiries Handled Per Rep</div>", unsafe_allow_html=True)
                st.bar_chart(data=perf_matrix, x="Salesperson", y="Total Leads Assigned", color="#164194")
            with c2:
                st.markdown("<div class='section-title'>💰 Total Pipeline Quoted Value (₹)</div>", unsafe_allow_html=True)
                st.bar_chart(data=perf_matrix, x="Salesperson", y="Quoted_Value", color="#00A859")

            st.markdown("---")
            st.markdown("<div class='section-title'>🔍 Individual Employee Inspector</div>", unsafe_allow_html=True)
            selected_emp = st.selectbox("Select Employee to View Assigned Work:", SALESPERSONS)

            if selected_emp:
                emp_leads = df_leads[df_leads["Assigned Salesperson"] == selected_emp] if not df_leads.empty else pd.DataFrame()
                emp_quotes = df_quotes[df_quotes["Assigned Salesperson"] == selected_emp] if not df_quotes.empty else pd.DataFrame()

                e1, e2 = st.columns(2)
                with e1:
                    st.markdown(f"<p style='color:#164194; font-weight:700;'>Active Leads for {selected_emp}: {len(emp_leads)}</p>", unsafe_allow_html=True)
                    st.dataframe(emp_leads, use_container_width=True, hide_index=True)
                with e2:
                    st.markdown(f"<p style='color:#164194; font-weight:700;'>Issued Quotes for {selected_emp}: {len(emp_quotes)}</p>", unsafe_allow_html=True)
                    st.dataframe(emp_quotes, use_container_width=True, hide_index=True)

    with tab_prog:
        st.markdown("<div class='section-title'>⚙️ Operational Progress & Factory Execution Funnel</div>", unsafe_allow_html=True)

        o1, o2, o3 = st.columns(3)
        with o1:
            st.markdown(f"<div class='metric-card'><h5>Total Inquiries</h5><h3>{len(df_leads)}</h3></div>", unsafe_allow_html=True)
        with o2:
            st.markdown(f"<div class='metric-card metric-card-green'><h5>Quotations Generated</h5><h3>{len(df_quotes)}</h3></div>", unsafe_allow_html=True)
        with o3:
            st.markdown(f"<div class='metric-card'><h5>Orders in Execution</h5><h3>{len(df_orders)}</h3></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("<div class='section-title'>📊 Factory Order Status Progress</div>", unsafe_allow_html=True)
            if not df_orders.empty and "Current Status" in df_orders.columns:
                status_counts = df_orders["Current Status"].value_counts().reset_index()
                status_counts.columns = ["Execution Status", "Total Jobs"]
                st.bar_chart(data=status_counts, x="Execution Status", y="Total Jobs", color="#00A859")
            else:
                st.info("No operational orders recorded in sheet.")

        with col_b:
            st.markdown("<div class='section-title'>📋 Quotation Status Pipeline</div>", unsafe_allow_html=True)
            if not df_quotes.empty and "Quotation Status" in df_quotes.columns:
                q_status_counts = df_quotes["Quotation Status"].value_counts().reset_index()
                q_status_counts.columns = ["Quote Status", "Count"]
                st.bar_chart(data=q_status_counts, x="Quote Status", y="Count", color="#164194")
            else:
                st.info("No quotation pipeline data available.")

# ---------------------------------------------------------
# FOLLOW-UP QUEUE & WORKDAY
# ---------------------------------------------------------
elif menu in ["⚡ Follow-up Queue & Workday", "📞 Follow-up Master"]:
    st.markdown(f"<div class='main-header'>⚡ Active Follow-up Queue: {st.session_state.user_display_name}</div>", unsafe_allow_html=True)

    df_follow = load_sheet("Quotation Follow Up Tracker")

    if not df_follow.empty:
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
# BRANDED PDF QUOTATION GENERATOR & CONVERT
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

                        conn = get_connection()
                        if conn:
                            df_q_existing = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="Quotation Sheet")
                            df_q_updated = pd.concat([df_q_existing, pd.DataFrame([quote_payload])], ignore_index=True)
                            conn.update(spreadsheet=SPREADSHEET_URL, worksheet="Quotation Sheet", data=df_q_updated)

                        pdf_bytes = generate_quotation_pdf(quote_payload)
                        st.success(f"✅ Quotation {quote_no} Generated Successfully!")

                        if pdf_bytes:
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
                if pdf_bytes:
                    st.download_button(
                        label=f"📥 Download PDF ({selected_q_no})",
                        data=pdf_bytes,
                        file_name=f"{selected_q_no.replace('/', '_')}.pdf",
                        mime="application/pdf"
                    )

# ---------------------------------------------------------
# ADD NEW LEAD
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

# ---------------------------------------------------------
# PROCESS ORDER EXECUTION
# ---------------------------------------------------------
elif menu == "⚙️ Process Order Execution":
    st.markdown("<div class='main-header'>⚙️ Operational & Factory Execution</div>", unsafe_allow_html=True)
    st.dataframe(load_sheet("Process Order"), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# CLIENT INSPECTOR
# ---------------------------------------------------------
elif menu == "🔍 Client Inspector":
    st.markdown("<div class='main-header'>🔍 Client 360 Degree Inspector</div>", unsafe_allow_html=True)
    df_leads = load_sheet("Leads Data")
    if not df_leads.empty and "Client ID" in df_leads.columns:
        cid = st.selectbox("Select Client ID:", df_leads["Client ID"].dropna().unique())
        if cid:
            st.dataframe(df_leads[df_leads["Client ID"] == cid], use_container_width=True, hide_index=True)
