import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

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
# CUSTOM CSS: BLUE OUTLINE + WHITE INPUTS + INCREASED FONTS
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Global Page Background */
    .stApp {
        background-color: #F8FAFC !important;
    }

    header[data-testid="stHeader"] {
        background-color: #F8FAFC !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #164194 !important;
        border-right: 2px solid #0e2d6b !important;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        font-size: 15px !important;
    }

    /* Container & Form Cards */
    div[data-testid="stForm"], .saas-card {
        background-color: #FFFFFF !important;
        border: 2px solid #164194 !important;
        border-radius: 12px !important;
        padding: 24px !important;
        box-shadow: 0 4px 12px rgba(22, 65, 148, 0.08) !important;
        margin-bottom: 20px !important;
    }

    /* Page Titles & Headers */
    .main-header {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #164194 !important;
        margin-bottom: 15px;
        border-bottom: 3px solid #00A859;
        padding-bottom: 8px;
    }

    .section-title {
        color: #164194 !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        margin-top: 10px !important;
        margin-bottom: 14px !important;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 6px;
    }

    /* FORM FIELD LABELS - INCREASED FONT SIZE */
    .stMainBlockContainer label, label * {
        color: #164194 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }

    /* COMPLETE FIX FOR ALL INPUT BOXES (WHITE INSIDE + BLUE OUTLINE) */
    div[data-baseweb="input"], 
    div[data-baseweb="base-input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 2px solid #164194 !important;
        border-radius: 8px !important;
    }

    /* INPUT TEXT INSIDE BOXES */
    div[data-baseweb="input"] input, 
    div[data-baseweb="base-input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }

    /* Active Focus State for Inputs */
    div[data-baseweb="textarea"]:focus-within, 
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #00A859 !important;
        box-shadow: 0 0 0 2px rgba(0, 168, 89, 0.2) !important;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #FFFFFF !important;
        border: 2px solid #164194 !important;
        border-left: 6px solid #164194 !important;
        border-radius: 10px !important;
        padding: 18px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        text-align: center;
    }

    .metric-card-green {
        border-left: 6px solid #00A859 !important;
    }

    .metric-card h5 {
        color: #64748B !important;
        font-size: 13px !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        margin-bottom: 6px !important;
    }

    .metric-card h3 {
        color: #164194 !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        margin: 0 !important;
    }

    /* Buttons Styling */
    .stButton>button, div[data-testid="stFormSubmitButton"]>button {
        background-color: #164194 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        padding: 10px 24px !important;
    }

    .stButton>button:hover, div[data-testid="stFormSubmitButton"]>button:hover {
        background-color: #00A859 !important;
        box-shadow: 0 4px 12px rgba(0, 168, 89, 0.3) !important;
    }

    /* Dataframe Container Styling */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border: 2px solid #164194 !important;
        border-radius: 10px !important;
        padding: 8px !important;
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

# Master Data Options
PRODUCT_LIST = [
    "Motorised Swing Gates", "Motorised Sliding Gates", "Automatic Rolling Shutters",
    "Dock Leveller", "Boom Barriers", "Rolling Shutter motor Part", "Spare Part"
]
SOURCE_LIST = ["Marketing Team", "Whats App", "India Mart", "Sales Email", "Phone Call", "Reference"]
SALESPERSONS = ["Mansingh Rathore", "Sidharth Jain", "Jeevan Sharma", "Deepak Sethiya", "Rishabh Jain", "Bhavya Jain"]
CLIENT_TYPES = ["New Buy", "Dealer", "Architect", "Contractor", "Service", "OEM"]
TEAM_MEMBERS = ["Pooja", "Dolly", "Albert", "Rishabh", "Bhavya", "Other"]

# ---------------------------------------------------------
# AUTHENTICATION & USER SESSION MANAGEMENT
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
            # Company Logo Integration on Login Page
            try:
                st.image("Company Logo.jpeg", use_container_width=True)
            except Exception:
                st.markdown("<h2 style='text-align: center; color: #164194; font-weight:800;'>🏭 SIDHARTH SHUTTER</h2>", unsafe_allow_html=True)
            
            st.markdown("<p style='text-align: center; color: #164194; font-weight: 700; font-size: 16px; margin-top: 10px;'>Sales CRM & Workflow Portal</p>", unsafe_allow_html=True)
            
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
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    try:
        st.image("Company Logo.jpeg", use_container_width=True)
    except Exception:
        st.write("🏭 **SSA CRM**")
        
    st.markdown(f"<h3 style='margin-bottom:2px; font-size: 18px !important;'>👋 {st.session_state.user_display_name}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #00A859 !important; font-weight:700; font-size:14px !important;'>Role: {st.session_state.user_role}</p>", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.user_role == "Salesperson":
        menu = st.radio("NAVIGATION", ["🎯 My Workday & Tasks", "📥 Add New Lead", "🔍 Client Inspector"])
    elif st.session_state.user_role == "Back-Office":
        menu = st.radio("NAVIGATION", ["📄 Convert Leads to Quotes", "📞 Follow-up Tracker", "🔍 Client Inspector"])
    elif st.session_state.user_role == "Operations":
        menu = st.radio("NAVIGATION", ["⚙️ Process Order Execution", "🔍 Client Inspector"])
    else: # Admin
        menu = st.radio("NAVIGATION", [
            "📊 Executive Dashboard",
            "🎯 My Workday & Tasks",
            "📥 Add New Lead",
            "📄 Convert Leads to Quotes",
            "📞 Follow-up Tracker",
            "⚙️ Process Order Execution",
            "🔍 Client Inspector"
        ])

    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ---------------------------------------------------------
# WORKFLOW PAGE 1: MY WORKDAY & TASKS
# ---------------------------------------------------------
if menu == "🎯 My Workday & Tasks":
    st.markdown(f"<div class='main-header'>🎯 Workday Portal: {st.session_state.user_display_name}</div>", unsafe_allow_html=True)

    df_leads = load_sheet("Leads Data")
    df_follow = load_sheet("Quotation Follow Up Tracker")

    if not df_leads.empty and "Assigned Salesperson" in df_leads.columns:
        my_leads = df_leads[df_leads["Assigned Salesperson"] == st.session_state.user_display_name] if st.session_state.user_role == "Salesperson" else df_leads
    else:
        my_leads = pd.DataFrame()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='metric-card'><h5>My Active Leads</h5><h3>{len(my_leads)}</h3></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card metric-card-green'><h5>Total Pipeline Leads</h5><h3>{len(df_leads)}</h3></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><h5>Pending Follow-ups</h5><h3>{len(df_follow)}</h3></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📋 My Assigned Lead Records</div>", unsafe_allow_html=True)
    if not my_leads.empty:
        st.dataframe(my_leads, use_container_width=True, hide_index=True)
    else:
        st.info("No active leads currently assigned to your profile.")

# ---------------------------------------------------------
# WORKFLOW PAGE 2: ADD NEW LEAD
# ---------------------------------------------------------
elif menu == "📥 Add New Lead":
    st.markdown("<div class='main-header'>📥 Lead Capture Portal</div>", unsafe_allow_html=True)

    with st.form("add_lead_form", clear_on_submit=True):
        st.markdown("<div class='section-title'>👤 Client & Corporate Details</div>", unsafe_allow_html=True)
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

        st.markdown("<div class='section-title'>📦 Requirement & Sales Assignment</div>", unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)
        with c4:
            product = st.selectbox("Product Requirement *", PRODUCT_LIST)
            qty = st.number_input("Quantity", min_value=1, value=1)
        with c5:
            source = st.selectbox("Lead Source", SOURCE_LIST)
            client_type = st.selectbox("Type of Client", CLIENT_TYPES)
        with c6:
            default_sp_idx = SALESPERSONS.index(st.session_state.user_display_name) if st.session_state.user_display_name in SALESPERSONS else 0
            assigned_sp = st.selectbox("Assigned Salesperson", SALESPERSONS, index=default_sp_idx)
            handle_by = st.selectbox("Leads Handle By", TEAM_MEMBERS)

        c7, c8 = st.columns(2)
        with c7:
            quotation_status = st.selectbox("Quotation Status", ["Not Sent", "Sent", "Under Review"])
            quotation_sent_by = st.selectbox("Quotation Sent By", TEAM_MEMBERS)
        with c8:
            remarks = st.text_area("Initial Remarks / Notes", height=100)

        submit_lead = st.form_submit_button("💾 Save Lead to Master Sheet", use_container_width=True)

        if submit_lead:
            if not client_name or not number:
                st.error("Please complete all required fields: Client Name and Contact Number.")
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
                    st.success(f"✅ Lead Created Successfully! Client ID: {client_id}")

# ---------------------------------------------------------
# WORKFLOW PAGE 3: CONVERT LEADS TO QUOTES
# ---------------------------------------------------------
elif menu == "📄 Convert Leads to Quotes":
    st.markdown("<div class='main-header'>📄 Quotation Creation & Master</div>", unsafe_allow_html=True)

    df_leads = load_sheet("Leads Data")
    
    if not df_leads.empty:
        st.markdown("<div class='section-title'>⚡ Quick Convert Lead to Quotation</div>", unsafe_allow_html=True)
        unquoted = df_leads[df_leads["Quotation Status"] != "Sent"] if "Quotation Status" in df_leads.columns else df_leads

        if not unquoted.empty:
            selected_client = st.selectbox("Select Lead to Generate Quotation:", unquoted["Client ID"].tolist())
            lead_row = unquoted[unquoted["Client ID"] == selected_client].iloc[0]

            with st.form("create_quote_form"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.text_input("Client ID", value=lead_row.get("Client ID", ""), disabled=True)
                    st.text_input("Client Name", value=lead_row.get("Client Name", ""), disabled=True)
                with c2:
                    quote_no = st.text_input("Quotation Number *", value=f"SSA/2026-27/{datetime.now().strftime('%M%S')}")
                    quote_amt = st.number_input("Quotation Amount (₹) *", min_value=0, step=5000)
                with c3:
                    shared_by = st.selectbox("Quotation Shared By", TEAM_MEMBERS)
                    q_status = st.selectbox("Status", ["Sent", "Approved", "Revised Required"])

                quote_remarks = st.text_area("Quotation Remarks", value=f"Quoted for {lead_row.get('Product ', '')} - Qty: {lead_row.get('Qty', 1)}", height=100)
                submit_quote = st.form_submit_button("📄 Save & Issue Quotation", use_container_width=True)

                if submit_quote:
                    new_quote = {
                        "Client  ID": lead_row.get("Client ID", ""),
                        "Date Stamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Client Name": lead_row.get("Client Name", ""),
                        "Company Name": lead_row.get("Company Name", ""),
                        "Customer Contact Number": lead_row.get("Number", ""),
                        "Product ": lead_row.get("Product ", ""),
                        "Quantity": lead_row.get("Qty", 1),
                        "City": lead_row.get("City", ""),
                        "Source": lead_row.get("Source", ""),
                        "Assigned Salesperson": lead_row.get("Assigned Salesperson", ""),
                        "Quotation Status": q_status,
                        "Quotation Shared By": shared_by,
                        "Quotation Number": quote_no,
                        "Qut. Amount": quote_amt,
                        "Remarks": quote_remarks
                    }
                    conn = get_connection()
                    if conn:
                        df_q_existing = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="Quotation Sheet")
                        df_q_updated = pd.concat([df_q_existing, pd.DataFrame([new_quote])], ignore_index=True)
                        conn.update(spreadsheet=SPREADSHEET_URL, worksheet="Quotation Sheet", data=df_q_updated)
                        st.success(f"✅ Quotation {quote_no} linked to {selected_client} successfully!")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📋 Master Quotation Registry</div>", unsafe_allow_html=True)
    st.dataframe(load_sheet("Quotation Sheet"), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# WORKFLOW PAGE 4: FOLLOW-UP TRACKER
# ---------------------------------------------------------
elif menu == "📞 Follow-up Tracker":
    st.markdown("<div class='main-header'>📞 Quotation Follow-up Management</div>", unsafe_allow_html=True)
    st.dataframe(load_sheet("Quotation Follow Up Tracker"), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# WORKFLOW PAGE 5: PROCESS ORDER EXECUTION
# ---------------------------------------------------------
elif menu == "⚙️ Process Order Execution":
    st.markdown("<div class='main-header'>⚙️ Operational & Factory Pipeline Execution</div>", unsafe_allow_html=True)
    st.dataframe(load_sheet("Process Order"), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# WORKFLOW PAGE 6: CLIENT INSPECTOR
# ---------------------------------------------------------
elif menu == "🔍 Client Inspector":
    st.markdown("<div class='main-header'>🔍 Client 360 Degree View</div>", unsafe_allow_html=True)
    
    df_leads = load_sheet("Leads Data")
    df_quotes = load_sheet("Quotation Sheet")
    df_followup = load_sheet("Quotation Follow Up Tracker")
    df_orders = load_sheet("Process Order")

    client_id_list = []
    if not df_leads.empty:
        col_name = [c for c in df_leads.columns if "client id" in c.lower() or "client_id" in c.lower()]
        if col_name:
            client_id_list = df_leads[col_name[0]].dropna().unique().tolist()

    if client_id_list:
        selected_client_id = st.selectbox("🔎 Select Client ID to Inspect:", client_id_list)

        def filter_by_client_id(df, cid):
            if df.empty:
                return pd.DataFrame()
            matching_cols = [c for c in df.columns if "client id" in c.lower() or "client_id" in c.lower()]
            if matching_cols:
                return df[df[matching_cols[0]].astype(str) == str(cid)]
            return pd.DataFrame()

        t1, t2, t3, t4 = st.tabs(["📥 Lead Record", "📄 Quotations", "📞 Follow-ups", "⚙️ Operations"])
        with t1:
            st.dataframe(filter_by_client_id(df_leads, selected_client_id), use_container_width=True, hide_index=True)
        with t2:
            st.dataframe(filter_by_client_id(df_quotes, selected_client_id), use_container_width=True, hide_index=True)
        with t3:
            st.dataframe(filter_by_client_id(df_followup, selected_client_id), use_container_width=True, hide_index=True)
        with t4:
            st.dataframe(filter_by_client_id(df_orders, selected_client_id), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# WORKFLOW PAGE 7: EXECUTIVE DASHBOARD
# ---------------------------------------------------------
elif menu == "📊 Executive Dashboard":
    st.markdown("<div class='main-header'>📊 Executive Sales & Operations Analytics</div>", unsafe_allow_html=True)

    df_leads = load_sheet("Leads Data")
    df_quotes = load_sheet("Quotation Sheet")
    df_orders = load_sheet("Process Order")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='metric-card'><h5>Total Inquiries</h5><h3>{len(df_leads)}</h3></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card metric-card-green'><h5>Quotations Issued</h5><h3>{len(df_quotes)}</h3></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><h5>Orders in Production</h5><h3>{len(df_orders)}</h3></div>", unsafe_allow_html=True)
    with c4:
        val = df_quotes['Qut. Amount'].sum() if not df_quotes.empty and 'Qut. Amount' in df_quotes.columns else 0
        st.markdown(f"<div class='metric-card metric-card-green'><h5>Pipeline Value</h5><h3>₹{val:,.0f}</h3></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📋 Recent Activity Feed</div>", unsafe_allow_html=True)
    if not df_leads.empty:
        st.dataframe(df_leads.tail(10), use_container_width=True, hide_index=True)
