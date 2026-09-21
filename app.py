import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sidharth Shutter CRM",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1ajDjxHOqfQw_7qRNvMT4I6q9jujJ6tjPqe6M4kOdoIo/edit"

# ---------------------------------------------------------
# CLEAN MODERN CSS INJECTION
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Base background styling */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Sidebar aesthetic */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important;
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-label {
        font-size: 13px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        margin-top: 4px;
    }
    
    /* Header Container */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 12px;
        border-bottom: 2px solid #E2E8F0;
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 24px;
        font-weight: 800;
        color: #1E3A8A;
    }
    
    /* Clean Streamlit Form Container */
    [data-testid="stForm"] {
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        padding: 24px;
        background-color: #FFFFFF;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* Input adjustments */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, textarea {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border-color: #CBD5E1 !important;
    }
    
    /* Section Divider Headers */
    .form-section-title {
        font-size: 16px;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 12px;
        padding-bottom: 6px;
        border-bottom: 1px solid #E2E8F0;
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
    col_t, col_l = st.columns([4, 1])
    with col_t:
        st.markdown(f"<div class='header-title'>{title_text}</div>", unsafe_allow_html=True)
    with col_l:
        try:
            st.image("Company Logo.jpeg", use_container_width=True)
        except Exception:
            st.markdown("<p style='text-align:right; font-weight:700; color:#1E3A8A;'>SIDHARTH SHUTTER</p>", unsafe_allow_html=True)

PRODUCT_LIST = [
    "Motorised Swing Gates", "Motorised Sliding Gates", "Automatic Rolling Shutters",
    "Dock Leveller", "Boom Barriers", "Rolling Shutter motor Part", "Spare Part"
]
SOURCE_LIST = ["Marketing Team", "Whats App", "India Mart", "Sales Email", "Phone Call", "Reference"]
SALESPERSONS = ["Mansingh Rathore", "Sidharth Jain", "Jeevan Sharma", "Deepak Sethiya", "Rishabh Jain", "Bhavya Jain"]
CLIENT_TYPES = ["New Buy", "Dealer", "Architect", "Contractor", "Service", "OEM"]
TEAM_MEMBERS = ["Pooja", "Dolly", "Albert", "Rishabh", "Bhavya", "Other"]

SCHEMA_DATA = {
    "Leads Data": pd.DataFrame({
        "Sr. No": [1, 2],
        "Client ID": ["SSA-Sep-26-0102", "SSA-Sep-26-0215"],
        "Client Name": ["Rajesh Sharma", "Sunil Verma"],
        "Company Name": ["Apex Logistics", "Verma Builders"],
        "Number": ["+91 98290 12345", "+91 94140 56789"],
        "Product ": ["Automatic Rolling Shutters", "Motorised Sliding Gates"],
        "Assigned Salesperson": ["Mansingh Rathore", "Sidharth Jain"],
        "Quotation Status": ["Sent", "Sent"]
    }),
    "Quotation Sheet": pd.DataFrame({
        "Client  ID": ["SSA-Sep-26-0102"],
        "Client Name": ["Rajesh Sharma"],
        "Quotation Number": ["SSA/2026-27/0182"],
        "Qut. Amount": [285000]
    }),
    "Quotation Follow Up Tracker": pd.DataFrame({
        "Client ID": ["SSA-Sep-26-0102"],
        "Follow Up Date": ["2026-09-16"],
        "Status": ["In Discussion"]
    }),
    "Process Order": pd.DataFrame({
        "Client ID": ["SSA-Sep-26-0215"],
        "Payment Status": ["Advance Received"]
    })
}

# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #FFFFFF;'>Sidharth CRM</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio(
        "Navigation",
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
# STAGE 0: DASHBOARD
# ---------------------------------------------------------
if menu == "📊 Executive Dashboard":
    render_header("📊 Executive Sales Overview")
    
    df_leads = load_sheet("Leads Data")
    df_quotes = load_sheet("Quotation Sheet")
    df_orders = load_sheet("Process Order")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Leads</div><div class="metric-value">{len(df_leads)}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Quotations</div><div class="metric-value">{len(df_quotes)}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Process Orders</div><div class="metric-value">{len(df_orders)}</div></div>', unsafe_allow_html=True)
    with c4:
        total_val = df_quotes['Qut. Amount'].sum() if not df_quotes.empty and 'Qut. Amount' in df_quotes.columns else 0
        st.markdown(f'<div class="metric-card"><div class="metric-label">Pipeline Value</div><div class="metric-value">₹{total_val:,.0f}</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Recent Leads")
    if not df_leads.empty:
        st.dataframe(df_leads.tail(8), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 1: LEADS DATA (RE-STYLED FORM)
# ---------------------------------------------------------
elif menu == "📥 Stage 1: Leads Data":
    render_header("📥 Lead Capture & Registry")
    
    tab_add, tab_view = st.tabs(["➕ Add New Lead", "📋 Master Leads Registry"])
    
    with tab_add:
        with st.form("add_lead_form", clear_on_submit=True):
            st.markdown("<div class='form-section-title'>👤 Client & Corporate Details</div>", unsafe_allow_html=True)
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
                
            address = st.text_area("Address Details", height=80)
            
            st.markdown("<div class='form-section-title'>📦 Requirement & Sales Assignment</div>", unsafe_allow_html=True)
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
                remarks = st.text_area("Initial Remarks / Notes", height=80)
                
            submit_lead = st.form_submit_button("Save Lead Record")
            
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
                        st.success(f"Lead saved successfully! ID: {client_id}")

    with tab_view:
        df_leads = load_sheet("Leads Data")
        st.dataframe(df_leads, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 2: QUOTATIONS & FOLLOW-UPS
# ---------------------------------------------------------
elif menu == "📄 Stage 2: Quotations & Follow-ups":
    render_header("📄 Quotations & Follow-ups")
    tab_q, tab_f = st.tabs(["Quotations List", "Follow-up Log"])
    with tab_q:
        st.dataframe(load_sheet("Quotation Sheet"), use_container_width=True, hide_index=True)
    with tab_f:
        st.dataframe(load_sheet("Quotation Follow Up Tracker"), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 3: PROCESS ORDER
# ---------------------------------------------------------
elif menu == "⚙️ Stage 3: Process Order Execution":
    render_header("⚙️ Process Order Execution")
    st.dataframe(load_sheet("Process Order"), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# CLIENT DETAIL VIEW
# ---------------------------------------------------------
elif menu == "🔍 Client Detail View":
    render_header("🔍 Client Records")
    df_leads = load_sheet("Leads Data")
    if not df_leads.empty and "Client ID" in df_leads.columns:
        cid = st.selectbox("Select Client ID:", df_leads["Client ID"].unique())
        st.dataframe(df_leads[df_leads["Client ID"] == cid], use_container_width=True)
    else:
        st.info("No records found.")

# ---------------------------------------------------------
# DATABASE CONFIG GENERATOR
# ---------------------------------------------------------
elif menu == "🛠️ Database Config Generator":
    render_header("🛠️ Database Setup")
    
    st.info("Download CSV templates or generate configurations below.")
    for sheet_name, df in SCHEMA_DATA.items():
        with st.expander(f"Worksheet: {sheet_name}"):
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button(
                f"Download {sheet_name}.csv",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f"{sheet_name}.csv",
                mime="text/csv"
            )
