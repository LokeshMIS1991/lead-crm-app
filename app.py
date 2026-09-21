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
# RESTORED PREMIUM NAVY & GREEN BRAND THEME + BUG FIXES
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Global Background */
    .stApp {
        background-color: #F8FAFC !important;
    }

    /* Top Navigation Header Override */
    header[data-testid="stHeader"] {
        background-color: #F8FAFC !important;
    }

    /* Left Panel Sidebar: Exact Brand Navy Blue with White Text */
    [data-testid="stSidebar"] {
        background-color: #164194 !important;
        border-right: 2px solid #0e2d6b !important;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Sidebar Oval Logo Box */
    .sidebar-oval-logo {
        background-color: #FFFFFF;
        border: 2px solid #00A859;
        border-radius: 50px / 30px;
        padding: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        text-align: center;
        margin-bottom: 12px;
    }

    /* Page Main Header Bar */
    .main-header {
        font-size: 26px;
        font-weight: 800;
        color: #164194 !important;
        margin-bottom: 10px;
        border-bottom: 3px solid #00A859;
        padding-bottom: 8px;
    }

    /* KPI Summary Cards */
    .kpi-card {
        background: #FFFFFF !important;
        padding: 20px 15px;
        border-radius: 12px;
        border-left: 6px solid #164194 !important;
        border-top: 1px solid #CBD5E1;
        border-right: 1px solid #CBD5E1;
        border-bottom: 1px solid #CBD5E1;
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

    /* Banner Card for Config Page */
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

    /* FORM STYLING & BUG FIXES FOR DARK TEXTAREAS / NUMBER INPUTS */
    div[data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 12px !important;
        padding: 24px !important;
        box-shadow: 0 4px 12px rgba(22, 65, 148, 0.05) !important;
    }

    /* Form Section Headers */
    .form-header-title {
        color: #164194 !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        margin-top: 10px !important;
        margin-bottom: 14px !important;
        border-bottom: 2px solid #F1F5F9;
        padding-bottom: 6px;
    }

    /* Target ALL Input fields, TextAreas, Selectboxes, and NumberInputs cleanly */
    div[data-baseweb="input"] input, 
    div[data-baseweb="base-input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] div {
        background-color: #FFFFFF !important;
        color: #164194 !important;
        font-weight: 600 !important;
    }

    /* Textarea container fix */
    div[data-baseweb="textarea"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #164194 !important;
        border-radius: 8px !important;
    }

    /* Input borders */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        border: 1.5px solid #164194 !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
    }

    /* Form Labels */
    .stMainBlockContainer label {
        color: #164194 !important;
        font-weight: 700 !important;
        font-size: 13px !important;
    }

    /* Primary Buttons Styling */
    .stButton>button, div[data-testid="stFormSubmitButton"]>button {
        background-color: #164194 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 700 !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease-in-out;
    }

    .stButton>button *, div[data-testid="stFormSubmitButton"]>button * {
        color: #FFFFFF !important;
    }

    .stButton>button:hover, div[data-testid="stFormSubmitButton"]>button:hover {
        background-color: #00A859 !important;
        box-shadow: 0 4px 12px rgba(0, 168, 89, 0.3) !important;
    }

    /* Tabs Component Customization */
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
        border-radius: 6px !important;
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
        try:
            st.image("Company Logo.jpeg", use_container_width=True)
        except Exception:
            pass

# Master Options
PRODUCT_LIST = [
    "Motorised Swing Gates", "Motorised Sliding Gates", "Automatic Rolling Shutters",
    "Dock Leveller", "Boom Barriers", "Rolling Shutter motor Part", "Spare Part"
]
SOURCE_LIST = ["Marketing Team", "Whats App", "India Mart", "Sales Email", "Phone Call", "Reference"]
SALESPERSONS = ["Mansingh Rathore", "Sidharth Jain", "Jeevan Sharma", "Deepak Sethiya", "Rishabh Jain", "Bhavya Jain"]
CLIENT_TYPES = ["New Buy", "Dealer", "Architect", "Contractor", "Service", "OEM"]
TEAM_MEMBERS = ["Pooja", "Dolly", "Albert", "Rishabh", "Bhavya", "Other"]

# CONFIG / SCHEMA DATASETS
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
    
    st.markdown("<p style='text-align: center; font-size: 18px; font-weight: 800; color: #FFFFFF !important;'>SIDHARTH SHUTTER</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-weight: 700; color: #00A859 !important; font-size: 12px; margin-top:-10px;'>CRM & Operational Pipeline</p>", unsafe_allow_html=True)
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
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #164194 !important; font-weight: 800;'>🔥 Recent Inquiries & Activity</h3>", unsafe_allow_html=True)
    
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
        st.info("ℹ️ No records found in connected database.")
    else:
        selected_client_id = st.selectbox("🔎 Select Client ID to View Details:", client_id_list)

        def filter_by_client_id(df, cid):
            if df.empty:
                return pd.DataFrame()
            matching_cols = [c for c in df.columns if "client id" in c.lower() or "client_id" in c.lower()]
            if matching_cols:
                return df[df[matching_cols[0]].astype(str) == str(cid)]
            return pd.DataFrame()

        tab_l, tab_q, tab_f, tab_o = st.tabs([
            "📥 Lead Record",
            "📄 Quotations",
            "📞 Follow-up Log",
            "⚙️ Operational Execution"
        ])

        with tab_l:
            st.dataframe(filter_by_client_id(df_leads, selected_client_id), use_container_width=True, hide_index=True)
        with tab_q:
            st.dataframe(filter_by_client_id(df_quotes, selected_client_id), use_container_width=True, hide_index=True)
        with tab_f:
            st.dataframe(filter_by_client_id(df_followup, selected_client_id), use_container_width=True, hide_index=True)
        with tab_o:
            st.dataframe(filter_by_client_id(df_orders, selected_client_id), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 1: LEADS DATA
# ---------------------------------------------------------
elif menu == "📥 Stage 1: Leads Data":
    render_header("📥 Stage 1: Lead Capture & Management")
    
    tab_add, tab_view = st.tabs(["➕ Add New Lead", "📋 Master Leads Registry"])
    
    with tab_add:
        with st.form("add_lead_form", clear_on_submit=True):
            st.markdown("<div class='form-header-title'>👤 Client & Corporate Details</div>", unsafe_allow_html=True)
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
                
            address = st.text_area("Address Details", height=100)
            
            st.markdown("<div class='form-header-title'>📦 Requirement & Sales Assignment</div>", unsafe_allow_html=True)
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
                remarks = st.text_area("Initial Remarks / Notes", height=100)
                
            submit_lead = st.form_submit_button("💾 Save Lead to Database")
            
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
                        st.success(f"✅ Lead Created Successfully! Client ID: **{client_id}**")

    with tab_view:
        df_leads = load_sheet("Leads Data")
        st.dataframe(df_leads, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 2: QUOTATIONS & FOLLOW-UPS
# ---------------------------------------------------------
elif menu == "📄 Stage 2: Quotations & Follow-ups":
    render_header("📄 Stage 2: Quotations & Follow-up Panel")
    tab_q_list, tab_followup = st.tabs(["📋 Quotation Master", "📞 Follow-up Tracker"])
    
    with tab_q_list:
        st.dataframe(load_sheet("Quotation Sheet"), use_container_width=True, hide_index=True)

    with tab_followup:
        st.dataframe(load_sheet("Quotation Follow Up Tracker"), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 3: PROCESS ORDER EXECUTION
# ---------------------------------------------------------
elif menu == "⚙️ Stage 3: Process Order Execution":
    render_header("⚙️ Stage 3: Order Execution & Operations")
    st.dataframe(load_sheet("Process Order"), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 4: DATABASE CONFIG & SCHEMA GENERATOR
# ---------------------------------------------------------
elif menu == "🛠️ Database Config Generator":
    render_header("🛠️ Google Sheets Architecture & Config Generator")
    
    st.markdown("""
        <div class="banner-card">
            <span class="banner-badge">A to Z Schema Setup</span>
            <div class="banner-title">Google Sheets Architecture & Config Generator</div>
            <div class="banner-desc">
                Download complete, perfectly formatted CSV datasets for all 4 worksheets required by your Streamlit CRM app.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    tab_leads, tab_quote, tab_follow, tab_proc = st.tabs([
        "📥 1. Leads Data",
        "📄 2. Quotation Sheet",
        "📞 3. Follow Up Tracker",
        "⚙️ 4. Process Order"
    ])
    
    for tab, key in zip([tab_leads, tab_quote, tab_follow, tab_proc], SCHEMA_DATA.keys()):
        with tab:
            df_template = SCHEMA_DATA[key]
            st.dataframe(df_template, use_container_width=True, hide_index=True)
            st.download_button(
                label=f"📥 Download `{key}.csv`",
                data=df_template.to_csv(index=False).encode('utf-8'),
                file_name=f"{key}.csv",
                mime="text/csv"
            )
