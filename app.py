import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sidharth Shutter & Automation - Sales CRM",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# TARGET GOOGLE SHEET URL
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1ajDjxHOqfQw_7qRNvMT4I6q9jujJ6tjPqe6M4kOdoIo/edit"

# ---------------------------------------------------------
# BRAND STYLING & CUSTOM COLOR OVERRIDES
# Theme Palette:
#   - Navy Blue: #164194 (Primary)
#   - Green:     #00A859 (Secondary Accent)
#   - Light Slate Background: #F8FAFC
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Global Text & Heading Color Enforcement */
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, span, div, label {
        color: #164194 !important;
    }

    /* Top Navigation Header Bar Override */
    header[data-testid="stHeader"] {
        background-color: #F8FAFC !important;
    }
    header[data-testid="stHeader"] * {
        color: #164194 !important;
    }

    /* Global App Main Content Area Background */
    .stApp {
        background-color: #F8FAFC !important;
    }

    /* Left Panel Sidebar: Exact Brand Navy Blue with White Text */
    [data-testid="stSidebar"] {
        background-color: #164194 !important;
        color: #FFFFFF !important;
        border-right: 2px solid #0F3275 !important;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Sidebar Logo & Branding Styling */
    .sidebar-oval-logo {
        background-color: #FFFFFF;
        border: 2px solid #00A859;
        border-radius: 50px / 30px;
        padding: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        text-align: center;
        margin-bottom: 12px;
    }

    /* Page Main Header */
    .main-header {
        font-size: 26px;
        font-weight: 800;
        color: #164194 !important;
        margin-bottom: 10px;
        border-bottom: 3px solid #00A859;
        padding-bottom: 8px;
    }

    .top-right-logo {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding-bottom: 10px;
    }

    /* KPI Summary Cards */
    .kpi-card {
        background: #FFFFFF !important;
        padding: 20px 15px;
        border-radius: 12px;
        border-left: 6px solid #164194 !important;
        border: 1px solid #CBD5E1;
        box-shadow: 0 4px 12px rgba(22, 65, 148, 0.08);
        text-align: center;
    }

    .kpi-card-green {
        border-left: 6px solid #00A859 !important;
    }

    .kpi-card h5 {
        color: #00A859 !important;
        font-size: 13px;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .kpi-card h2 {
        color: #164194 !important;
        font-size: 28px;
        font-weight: 800;
        margin: 0;
    }

    /* Banner Card for Schema Setup Page */
    .banner-card {
        background: linear-gradient(135deg, #164194 0%, #0e2d6b 100%);
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 10px 25px rgba(22, 65, 148, 0.25);
        margin-bottom: 24px;
    }

    .banner-card * {
        color: #FFFFFF !important;
    }

    .banner-badge {
        background-color: #00A859 !important;
        color: #FFFFFF !important;
        font-size: 11px;
        font-weight: 800;
        padding: 4px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
        margin-bottom: 10px;
    }

    .banner-title {
        font-size: 24px;
        font-weight: 800;
        margin: 0 0 8px 0;
    }

    .banner-desc {
        font-size: 14px;
        opacity: 0.9;
        margin: 0;
        line-height: 1.5;
    }

    /* Setup Step Card */
    .step-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #CBD5E1;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }

    .step-badge {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background-color: #164194;
        color: #FFFFFF !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 14px;
        margin-bottom: 10px;
    }

    .step-badge-green {
        background-color: #00A859 !important;
    }

    /* Form Field Labels and Input Customization */
    .stTextInput label, .stSelectbox label, .stNumberInput label, .stTextArea label, .stDateInput label {
        color: #164194 !important;
        font-weight: 700 !important;
    }

    .stTextInput>div>div>input, .stSelectbox>div>div, .stTextArea>div>div>textarea, .stDateInput input {
        background-color: #FFFFFF !important;
        color: #164194 !important;
        border: 1.5px solid #164194 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    /* Submit / Action Buttons */
    .stButton>button, div[data-testid="stFormSubmitButton"]>button {
        background-color: #164194 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 700 !important;
        padding: 10px 24px !important;
    }

    .stButton>button * , div[data-testid="stFormSubmitButton"]>button * {
        color: #FFFFFF !important;
    }

    .stButton>button:hover, div[data-testid="stFormSubmitButton"]>button:hover {
        background-color: #00A859 !important;
    }

    /* Tabs Component Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: #E2E8F0 !important;
        padding: 6px !important;
        border-radius: 10px !important;
    }

    .stTabs [data-baseweb="tab"] * {
        color: #164194 !important;
        font-weight: 700 !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #164194 !important;
    }

    .stTabs [aria-selected="true"] * {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# GOOGLE SHEETS CONNECTION & DATA HELPERS
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

def render_header(title_text):
    col_title, col_logo = st.columns([4, 1.2])
    with col_title:
        st.markdown(f"<div class='main-header'>{title_text}</div>", unsafe_allow_html=True)
    with col_logo:
        st.markdown("<div class='top-right-logo'>", unsafe_allow_html=True)
        try:
            st.image("Company Logo.jpeg", use_container_width=True)
        except Exception:
            pass
        st.markdown("</div>", unsafe_allow_html=True)

# Master Dropdown Options
PRODUCT_LIST = [
    "Motorised Swing Gates", "Motorised Sliding Gates", "Automatic Rolling Shutters",
    "Dock Leveller", "Boom Barriers", "Rolling Shutter motor Part", "Spare Part"
]
SOURCE_LIST = ["Marketing Team", "Whats App", "India Mart", "Sales Email", "Phone Call", "Reference"]
SALESPERSONS = ["Mansingh Rathore", "Sidharth Jain", "Jeevan Sharma", "Deepak Sethiya", "Rishabh Jain", "Bhavya Jain"]
CLIENT_TYPES = ["New Buy", "Dealer", "Architect", "Contractor", "Service", "OEM"]
TEAM_MEMBERS = ["Pooja", "Dolly", "Albert", "Rishabh", "Bhavya", "Other"]

# ---------------------------------------------------------
# SAMPLE SCHEMA DATASETS (FOR CONFIG GENERATOR PAGE)
# ---------------------------------------------------------
SCHEMA_DATA = {
    "Leads Data": pd.DataFrame({
        "Sr. No": [1, 2, 3],
        "Client ID": ["SSA-Sep-26-0102", "SSA-Sep-26-0215", "SSA-Sep-26-0340"],
        "Date Stamp": ["2026-09-15 10:30:00", "2026-09-15 11:15:00", "2026-09-15 14:00:00"],
        "Client Name": ["Rajesh Sharma", "Sunil Verma", "Amit Patel"],
        "Company Name": ["Apex Logistics", "Verma Builders", "Patel Warehousing"],
        "Number": ["+91 98290 12345", "+91 94140 56789", "+91 98250 99887"],
        "Email": ["rajesh@apexlogistics.in", "s.verma@vermagroup.com", "amit@patelwh.com"],
        "Product ": ["Automatic Rolling Shutters", "Motorised Sliding Gates", "Dock Leveller"],
        "Qty": [3, 1, 2],
        "Address": ["Plot 12, Vishwakarma Industrial Area", "C-45, Nirman Nagar", "GIDC Phase 3"],
        "City": ["Jaipur", "Jaipur", "Ahmedabad"],
        "State": ["Rajasthan", "Rajasthan", "Gujarat"],
        "Source": ["India Mart", "WhatsApp", "Sales Email"],
        "Assigned Salesperson": ["Mansingh Rathore", "Sidharth Jain", "Jeevan Sharma"],
        "Type of client": ["New Buy", "Architect", "Contractor"],
        "Quotation Status": ["Sent", "Sent", "Not Sent"],
        "Leads Handle By": ["Pooja", "Dolly", "Rishabh"],
        "Quotation Sent By": ["Dolly", "Rishabh", "Other"],
        "Remarks": ["High priority commercial requirement.", "Architect specified SSA gate automation.", "Awaiting structural site dimensions."]
    }),
    "Quotation Sheet": pd.DataFrame({
        "Client  ID": ["SSA-Sep-26-0102", "SSA-Sep-26-0215"],
        "Date Stamp": ["2026-09-15 10:30:00", "2026-09-15 11:15:00"],
        "Client Name": ["Rajesh Sharma", "Sunil Verma"],
        "Company Name": ["Apex Logistics", "Verma Builders"],
        "Customer Contact Number": ["+91 98290 12345", "+91 94140 56789"],
        "Product ": ["Automatic Rolling Shutters", "Motorised Sliding Gates"],
        "Quantity": [3, 1],
        "City": ["Jaipur", "Jaipur"],
        "Source": ["India Mart", "WhatsApp"],
        "Assigned Salesperson": ["Mansingh Rathore", "Sidharth Jain"],
        "Quotation Status": ["Sent", "Approved"],
        "Quotation Shared By": ["Dolly", "Rishabh"],
        "Quotation Number": ["SSA/2026-27/0182", "SSA/2026-27/0183"],
        "Qut. Amount": [285000, 145000],
        "Remarks": ["Commercial quote shared with GST & transport.", "Approved by client via email."]
    }),
    "Quotation Follow Up Tracker": pd.DataFrame({
        "Client ID": ["SSA-Sep-26-0102", "SSA-Sep-26-0215"],
        "Quotation Number": ["SSA/2026-27/0182", "SSA/2026-27/0183"],
        "Client Name": ["Rajesh Sharma", "Sunil Verma"],
        "Company Name": ["Apex Logistics", "Verma Builders"],
        "Contact Number": ["+91 98290 12345", "+91 94140 56789"],
        "Product": ["Automatic Rolling Shutters", "Motorised Sliding Gates"],
        "Quotation Amount": [285000, 145000],
        "Follow Up Date": ["2026-09-16", "2026-09-15"],
        "Followed By": ["Pooja", "Dolly"],
        "Client Response / Remarks": ["Client requested 5% discount for bulk payment.", "PO confirmed. Advance expected tomorrow."],
        "Next Follow Up Date": ["2026-09-18", "2026-09-16"],
        "Status": ["In Discussion", "Approved"]
    }),
    "Process Order": pd.DataFrame({
        "Client ID": ["SSA-Sep-26-0215"],
        "Quotation Number": ["SSA/2026-27/0183"],
        "Purchase Order Number": ["PO-VERMA-992"],
        "Qut. Amount": [145000],
        "Advance Amount": [50000],
        "Start Date": ["2026-09-15"],
        "Payment Status": ["Advance Received"],
        "Drawing Status": ["Done"],
        "Measurement": ["Done"],
        "Production Status": ["In Progress"],
        "Dispatch Status": ["Pending"],
        "Document Submission": ["Done"],
        "Material Receiving": ["Pending"],
        "Invoice Status": ["Pending"],
        "Installation Invoice": ["Pending"],
        "Operational Notes": ["Production underway at factory."]
    })
}

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<div class='sidebar-oval-logo'>", unsafe_allow_html=True)
    try:
        st.image("Company Logo.jpeg", use_container_width=True)
    except Exception:
        st.write("🏭 **SSA CRM**")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; font-size: 20px; font-weight: 800; color: #FFFFFF !important;'>SIDHARTH SHUTTER</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-weight: 700; color: #00A859 !important;'>CRM & Operational Pipeline</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio(
        "WORKFLOW NAVIGATION",
        [
            "📊 Executive Dashboard",
            "🔍 Client Detail View",
            "📥 Stage 1: Leads Data",
            "📄 Stage 2: Quotations & Follow-ups",
            "⚙️ Stage 3: Process Order Execution",
            "🛠️ Database Config Generator"
        ]
    )

# ---------------------------------------------------------
# STAGE 0: EXECUTIVE DASHBOARD
# ---------------------------------------------------------
if menu == "📊 Executive Dashboard":
    render_header("📊 Executive Sales & Operations Overview")
    
    df_leads = load_sheet("Leads Data")
    df_quotes = load_sheet("Quotation Sheet")
    df_orders = load_sheet("Process Order")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="kpi-card"><h5>Total Leads</h5><h2>{len(df_leads)}</h2></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card kpi-card-green"><h5>Quotations Sent</h5><h2>{len(df_quotes)}</h2></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-card"><h5>Active Process Orders</h5><h2>{len(df_orders)}</h2></div>', unsafe_allow_html=True)
    with c4:
        total_val = df_quotes['Qut. Amount'].sum() if not df_quotes.empty and 'Qut. Amount' in df_quotes.columns else 0
        st.markdown(f'<div class="kpi-card kpi-card-green"><h5>Pipeline Value</h5><h2>₹{total_val:,.0f}</h2></div>', unsafe_allow_html=True)
        
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #164194 !important; font-weight: 800;'>🔥 Recent Activity Registry</h3>", unsafe_allow_html=True)
    
    if not df_leads.empty:
        st.dataframe(df_leads.tail(8), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# CLIENT DETAIL VIEW PAGE
# ---------------------------------------------------------
elif menu == "🔍 Client Detail View":
    render_header("🔍 Client Detailed Inspection View")
    
    df_leads = load_sheet("Leads Data")
    df_quotes = load_sheet("Quotation Sheet")
    df_followup = load_sheet("Quotation Follow Up Tracker")
    df_orders = load_sheet("Process Order")

    client_id_list = []
    if not df_leads.empty:
        col_name = [c for c in df_leads.columns if "client id" in c.lower() or "client_id" in c.lower()]
        if col_name:
            client_id_list = df_leads[col_name[0]].dropna().unique().tolist()

    if not client_id_list:
        st.warning("⚠️ No Client records found in Google Sheet.")
    else:
        selected_client_id = st.selectbox("🔎 Select Client ID to View Full History:", client_id_list)

        def filter_by_client_id(df, cid):
            if df.empty:
                return pd.DataFrame()
            matching_cols = [c for c in df.columns if "client id" in c.lower() or "client_id" in c.lower()]
            if matching_cols:
                return df[df[matching_cols[0]].astype(str) == str(cid)]
            return pd.DataFrame()

        lead_match = filter_by_client_id(df_leads, selected_client_id)
        quote_match = filter_by_client_id(df_quotes, selected_client_id)
        followup_match = filter_by_client_id(df_followup, selected_client_id)
        order_match = filter_by_client_id(df_orders, selected_client_id)

        tab_l, tab_q, tab_f, tab_o = st.tabs([
            "📥 Lead Record",
            "📄 Quotations",
            "📞 Follow-up Log",
            "⚙️ Operational Execution"
        ])

        with tab_l:
            st.dataframe(lead_match, use_container_width=True, hide_index=True)
        with tab_q:
            st.dataframe(quote_match, use_container_width=True, hide_index=True)
        with tab_f:
            st.dataframe(followup_match, use_container_width=True, hide_index=True)
        with tab_o:
            st.dataframe(order_match, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 1: LEADS DATA
# ---------------------------------------------------------
elif menu == "📥 Stage 1: Leads Data":
    render_header("📥 Stage 1: Lead Capture & Management")
    
    tab_add, tab_view = st.tabs(["➕ Add New Lead", "📋 Master Leads Registry"])
    
    with tab_add:
        with st.form("add_lead_form", clear_on_submit=True):
            st.markdown("<h5 style='color: #00A859 !important;'>👤 Client & Corporate Details</h5>", unsafe_allow_html=True)
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
                
            address = st.text_area("Address Details", height=2)
            
            st.markdown("<h5 style='color: #00A859 !important;'>📦 Requirement & Sales Assignment</h5>", unsafe_allow_html=True)
            c4, c5, c6 = st.columns(3)
            with c4:
                product = st.selectbox("Product Requirement *", PRODUCT_LIST)
                qty = st.number_input("Quantity", min_value=1, value=1)
            with c5:
                source = st.selectbox("Lead Source", SOURCE_LIST)
                client_type = st.selectbox("Type of Client", CLIENT_TYPES)
            with c6:
                assigned_sp = st.selectbox("Assigned Salesperson", SALESPERSONS)
                handle_by = st.selectbox("Leads Handle By", TEAM_MEMBERS)
                
            c7, c8 = st.columns(2)
            with c7:
                quotation_status = st.selectbox("Quotation Status", ["Not Sent", "Sent", "Under Review"])
                quotation_sent_by = st.selectbox("Quotation Sent By", TEAM_MEMBERS)
            with c8:
                remarks = st.text_area("Initial Remarks / Notes")
                
            submit_lead = st.form_submit_button("💾 Save Lead to Google Sheet")
            
            if submit_lead:
                if not client_name or not number:
                    st.error("Please fill required fields: Client Name and Contact Number.")
                else:
                    date_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    client_id = f"SSA-{datetime.now().strftime('%b-%y')}-{datetime.now().strftime('%M%S')}"
                    
                    new_lead = {
                        "Sr. No": len(load_sheet("Leads Data")) + 1,
                        "Client ID": client_id,
                        "Date Stamp": date_stamp,
                        "Client Name": client_name,
                        "Company Name": company_name,
                        "Number": number,
                        "Email": email,
                        "Product ": product,
                        "Qty": qty,
                        "Address": address,
                        "City": city,
                        "State": state,
                        "Source": source,
                        "Assigned Salesperson": assigned_sp,
                        "Type of client": client_type,
                        "Quotation Status": quotation_status,
                        "Leads Handle By": handle_by,
                        "Quotation Sent By": quotation_sent_by,
                        "Remarks": remarks
                    }
                    
                    conn = get_connection()
                    if conn:
                        df_existing = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="Leads Data")
                        df_updated = pd.concat([df_existing, pd.DataFrame([new_lead])], ignore_index=True)
                        conn.update(spreadsheet=SPREADSHEET_URL, worksheet="Leads Data", data=df_updated)
                        st.success(f"✅ Lead Created Successfully in Google Sheet! Generated Client ID: **{client_id}**")

    with tab_view:
        df_leads = load_sheet("Leads Data")
        st.dataframe(df_leads, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 2: QUOTATIONS & FOLLOW-UP TRACKER
# ---------------------------------------------------------
elif menu == "📄 Stage 2: Quotations & Follow-ups":
    render_header("📄 Stage 2: Quotations & Follow-up Panel")
    tab_q_list, tab_followup = st.tabs(["📋 Quotation Master", "📞 Follow-up Tracker"])
    
    with tab_q_list:
        df_quotes = load_sheet("Quotation Sheet")
        st.dataframe(df_quotes, use_container_width=True, hide_index=True)

    with tab_followup:
        df_followup = load_sheet("Quotation Follow Up Tracker")
        st.dataframe(df_followup, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 3: PROCESS ORDER EXECUTION
# ---------------------------------------------------------
elif menu == "⚙️ Stage 3: Process Order Execution":
    render_header("⚙️ Stage 3: Order Execution & Operations")
    df_orders = load_sheet("Process Order")
    st.dataframe(df_orders, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 4: DATABASE CONFIG & SCHEMA GENERATOR (NEW SEPARATE VIEW)
# ---------------------------------------------------------
elif menu == "🛠️ Database Config Generator":
    render_header("🛠️ Google Sheets Architecture & Config Generator")
    
    # Banner Intro Box
    st.markdown("""
        <div class="banner-card">
            <span class="banner-badge">A to Z Schema Setup</span>
            <div class="banner-title">Google Sheets Architecture & Config Generator</div>
            <div class="banner-desc">
                Preview and download complete, perfectly formatted CSV datasets for all 4 worksheets required by your Streamlit CRM app. Use these template files to structure your Google Sheets workbook, and copy the pre-built secrets.toml configuration below.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Schema Preview & Download Tabs
    tab_leads, tab_quote, tab_follow, tab_proc, tab_sec = st.tabs([
        "📥 1. Leads Data",
        "📄 2. Quotation Sheet",
        "📞 3. Follow Up Tracker",
        "⚙️ 4. Process Order",
        "🔑 Streamlit secrets.toml Setup"
    ])
    
    with tab_leads:
        st.markdown("<h4 style='color: #164194 !important;'>Worksheet: <code>Leads Data</code></h4>", unsafe_allow_html=True)
        st.markdown("Stores incoming inquiries, customer contact details, lead sources, and salesperson assignments.")
        
        df_template = SCHEMA_DATA["Leads Data"]
        st.dataframe(df_template, use_container_width=True, hide_index=True)
        
        csv_data = df_template.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Leads Data.csv Template",
            data=csv_data,
            file_name="Leads Data.csv",
            mime="text/csv"
        )

    with tab_quote:
        st.markdown("<h4 style='color: #164194 !important;'>Worksheet: <code>Quotation Sheet</code></h4>", unsafe_allow_html=True)
        st.markdown("Tracks commercial quotation numbers, valuation amounts, statuses, and team member ownership.")
        
        df_template = SCHEMA_DATA["Quotation Sheet"]
        st.dataframe(df_template, use_container_width=True, hide_index=True)
        
        csv_data = df_template.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Quotation Sheet.csv Template",
            data=csv_data,
            file_name="Quotation Sheet.csv",
            mime="text/csv"
        )

    with tab_follow:
        st.markdown("<h4 style='color: #164194 !important;'>Worksheet: <code>Quotation Follow Up Tracker</code></h4>", unsafe_allow_html=True)
        st.markdown("Logs active communication logs, client responses, and scheduled follow-up dates.")
        
        df_template = SCHEMA_DATA["Quotation Follow Up Tracker"]
        st.dataframe(df_template, use_container_width=True, hide_index=True)
        
        csv_data = df_template.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📞 Download Quotation Follow Up Tracker.csv Template",
            data=csv_data,
            file_name="Quotation Follow Up Tracker.csv",
            mime="text/csv"
        )

    with tab_proc:
        st.markdown("<h4 style='color: #164194 !important;'>Worksheet: <code>Process Order</code></h4>", unsafe_allow_html=True)
        st.markdown("Tracks operational post-approval execution: drawings, production, payments, dispatch, and invoices.")
        
        df_template = SCHEMA_DATA["Process Order"]
        st.dataframe(df_template, use_container_width=True, hide_index=True)
        
        csv_data = df_template.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⚙️ Download Process Order.csv Template",
            data=csv_data,
            file_name="Process Order.csv",
            mime="text/csv"
        )

    with tab_sec:
        # Step Guide Cards
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.markdown("""
                <div class="step-card">
                    <div class="step-badge">1</div>
                    <h4 style="color: #164194; font-weight: 800; font-size: 15px; margin-bottom: 6px;">Create Google Sheet</h4>
                    <p style="font-size: 12px; color: #475569; margin: 0;">Create a new Google Sheet named <strong>"Sidharth Shutter CRM Master"</strong>. Create 4 tab worksheets matching the names exactly.</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col_s2:
            st.markdown("""
                <div class="step-card">
                    <div class="step-badge step-badge-green">2</div>
                    <h4 style="color: #164194; font-weight: 800; font-size: 15px; margin-bottom: 6px;">Import CSV Files</h4>
                    <p style="font-size: 12px; color: #475569; margin: 0;">Import each downloaded CSV template into its corresponding worksheet tab (File → Import → Replace current sheet).</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col_s3:
            st.markdown("""
                <div class="step-card">
                    <div class="step-badge">3</div>
                    <h4 style="color: #164194; font-weight: 800; font-size: 15px; margin-bottom: 6px;">Share Access</h4>
                    <p style="font-size: 12px; color: #475569; margin: 0;">Share the Google Sheet with your Google Cloud Service Account Email with <strong>Editor</strong> permissions.</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🔑 Configuration Snippet: `.streamlit/secrets.toml`")
        
        secrets_toml_code = f"""# .streamlit/secrets.toml
[connections.gsheets]
spreadsheet = "{SPREADSHEET_URL}"
type = "service_account"
project_id = "your-gcp-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\\nYOUR_PRIVATE_KEY_HERE\\n-----END PRIVATE KEY-----\\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "12345678901234567890"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account..."
"""
        st.code(secrets_toml_code, language="toml")
