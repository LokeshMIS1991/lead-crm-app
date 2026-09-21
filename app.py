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

# Initialize Session State for Password Visibility
if "show_pwd" not in st.session_state:
    st.session_state.show_pwd = False

# ---------------------------------------------------------
# BRAND UI STYLING
# Logo Colors: Primary Blue (#184B9C) | Dark Blue (#0E2C68) | Brand Green (#00A859)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Global Background */
    .stApp, header[data-testid="stHeader"] { 
        background-color: #FFFFFF !important; 
    }

    /* Hide Unstyled Sidebar Strings */
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] span {
        display: none !important;
    }

    /* Sidebar Navigation Styling */
    [data-testid="stSidebar"] {
        background-color: #184B9C !important;
        border-right: 2px solid #0E2C68 !important;
        padding-top: 10px !important;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        font-family: 'Segoe UI', Roboto, sans-serif !important;
    }

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

    /* Main Section Typography */
    .stMainBlockContainer h1, 
    .stMainBlockContainer h2, 
    .stMainBlockContainer h3, 
    .stMainBlockContainer h4, 
    .stMainBlockContainer p, 
    .stMainBlockContainer span,
    .stMainBlockContainer label,
    .stMainBlockContainer label p {
        color: #184B9C !important;
        font-family: 'Segoe UI', Roboto, sans-serif !important;
        font-weight: 700 !important;
    }

    .main-header {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #184B9C !important;
        margin-bottom: 15px !important;
        border-bottom: 3px solid #00A859 !important;
        padding-bottom: 8px !important;
    }

    .section-title {
        color: #184B9C !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        margin-top: 15px !important;
        margin-bottom: 10px !important;
        border-bottom: 1.5px solid #CBD5E1 !important;
        padding-bottom: 4px !important;
    }

    /* ---------------------------------------------------------
       CUSTOM LOGIN CARD & BRANDED BLUE INPUT BOXES
       --------------------------------------------------------- */
    div[data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 2px solid #184B9C !important;
        border-radius: 16px !important;
        padding: 35px 30px !important;
        box-shadow: 0 10px 30px rgba(24, 75, 156, 0.15) !important;
    }

    /* HIDE BROKEN STREAMLIT INTERNAL INPUT ICON TEXT */
    div[data-testid="stInputIconButton"],
    div[data-testid="stInputIconButton"] * {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* BLUE INPUT BOXES (Matching Logo Blue) */
    div[data-testid="stForm"] input[type="text"], 
    div[data-testid="stForm"] input[type="password"] {
        background-color: #184B9C !important;
        color: #FFFFFF !important;
        border: 1.5px solid #0E2C68 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stForm"] input::placeholder {
        color: #E2E8F0 !important;
        opacity: 0.85 !important;
    }

    div[data-testid="stForm"] input:focus {
        border-color: #00A859 !important;
        box-shadow: 0 0 0 2px rgba(0, 168, 89, 0.3) !important;
    }

    /* EYE ICON TOGGLE BUTTON (White Icon, Transparent Background) */
    div[data-testid="stForm"] div.stButton > button {
        background-color: #184B9C !important;
        color: #FFFFFF !important;
        border: 1.5px solid #0E2C68 !important;
        border-radius: 8px !important;
        height: 42px !important;
        margin-top: 28px !important;
        padding: 0 !important;
        font-size: 18px !important;
        width: 100% !important;
    }
    div[data-testid="stForm"] div.stButton > button:hover {
        background-color: #0E2C68 !important;
        color: #FFFFFF !important;
    }

    /* COMPACT REDUCED-WIDTH LOGIN BUTTON */
    div[data-testid="stFormSubmitButton"] button,
    div[data-testid="stFormSubmitButton"] button p,
    div[data-testid="stFormSubmitButton"] button span {
        background-color: #00A859 !important;
        background-image: none !important;
        color: #FFFFFF !important;
        border-radius: 25px !important;
        border: none !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        padding: 8px 16px !important;
        margin-top: 15px !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(0, 168, 89, 0.3) !important;
    }
    
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #008f4c !important;
        color: #FFFFFF !important;
    }

    /* General Page Tables & Metric Cards */
    .metric-card {
        background-color: #FFFFFF !important;
        border: 2px solid #184B9C !important;
        border-radius: 8px !important;
        padding: 14px 18px !important;
        box-shadow: 0 4px 10px rgba(24, 75, 156, 0.06) !important;
    }
    .metric-card-green { border-color: #00A859 !important; }
    .metric-card h5 { color: #184B9C !important; font-size: 13px !important; margin: 0 0 4px 0 !important; }
    .metric-card h3 { color: #0E2C68 !important; font-size: 28px !important; margin: 0 !important; }

    .queue-card {
        background-color: #FFFFFF !important;
        border-left: 5px solid #184B9C !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        padding: 14px !important;
        margin-bottom: 10px !important;
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
# AUTHENTICATION & USER MANAGEMENT
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.user_display_name = None
    st.session_state.username = None

def fetch_users_from_sheets():
    df_users = load_sheet("Users")
    users_dict = {}

    if not df_users.empty:
        df_users.columns = [str(c).strip().title() for c in df_users.columns]
        req_cols = ["Username", "Password", "Role", "Display Name"]
        if all(col in df_users.columns for col in req_cols):
            for _, row in df_users.iterrows():
                u_val = str(row["Username"]).strip().lower()
                p_raw = row["Password"]
                if pd.api.types.is_float_dtype(type(p_raw)) and p_raw.is_integer():
                    p_val = str(int(p_raw)).strip()
                else:
                    p_val = str(p_raw).split('.')[0] if str(p_raw).endswith('.0') else str(p_raw).strip()

                r_val = str(row["Role"]).strip()
                d_val = str(row["Display Name"]).strip()

                if u_val and u_val != "nan" and p_val and p_val != "nan":
                    users_dict[u_val] = (p_val, r_val, d_val)

    default_users = {
        "admin": ("admin123", "Admin", "System Administrator"),
        "mansingh": ("sales123", "Salesperson", "Mansingh Rathore"),
        "sidharth": ("sales123", "Salesperson", "Sidharth Jain"),
        "pooja": ("backoffice123", "Back-Office", "Pooja"),
        "dolly": ("backoffice123", "Back-Office", "Dolly"),
        "ops": ("ops123", "Operations", "Operations Team")
    }

    for u, data in default_users.items():
        if u not in users_dict:
            users_dict[u] = data

    return users_dict

def toggle_pwd():
    st.session_state.show_pwd = not st.session_state.show_pwd

def login_form():
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Grid structure to center and limit the form width
    c1, col, c2 = st.columns([1, 1.1, 1])
    with col:
        with st.form("login_form"):
            try:
                st.image("Company Logo.jpeg", use_container_width=True)
            except Exception:
                st.markdown("<h2 style='text-align: center; color: #184B9C; font-weight:800;'>🏭 SIDHARTH SHUTTER</h2>", unsafe_allow_html=True)
            
            st.markdown("<p style='text-align: center; color: #184B9C; font-weight: 700; font-size: 15px;'>Sales CRM & Workflow Portal</p>", unsafe_allow_html=True)
            
            user_input = st.text_input("Username", placeholder="e.g. admin or dolly").strip().lower()
            
            p_col1, p_col2 = st.columns([5.5, 1])
            pass_type = "text" if st.session_state.show_pwd else "password"
            
            with p_col1:
                pass_input = st.text_input("Password", type=pass_type, placeholder="Enter password").strip()
            with p_col2:
                eye_btn = st.form_submit_button("👁️", on_click=toggle_pwd)

            # Center and reduce the width of the login button using columns
            b_col1, b_col2, b_col3 = st.columns([0.25, 0.5, 0.25])
            with b_col2:
                submit = st.form_submit_button("🔑 Login", use_container_width=True)

            if submit:
                if not user_input or not pass_input:
                    st.warning("Please enter both Username and Password.")
                else:
                    users = fetch_users_from_sheets()
                    if user_input in users and users[user_input][0] == pass_input:
                        st.session_state.authenticated = True
                        st.session_state.username = user_input
                        st.session_state.user_role = users[user_input][1]
                        st.session_state.user_display_name = users[user_input][2]
                        st.rerun()
                    else:
                        st.error("Invalid Username or Password.")

# Check Authentication Status
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
    st.markdown(f"<p style='color: #E2E8F0 !important; font-weight:700; font-size:13px !important;'>Role: {st.session_state.user_role}</p>", unsafe_allow_html=True)
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
            "🔍 Client Inspector",
            "👥 User Management (Admin)"
        ])

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ---------------------------------------------------------
# MAIN CRM CONTENT ROUTER
# ---------------------------------------------------------
if menu == "📥 Add New Lead":
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

elif menu == "🔍 Client Inspector":
    st.markdown("<div class='main-header'>🔍 Client 360 Degree Inspector</div>", unsafe_allow_html=True)
    df_leads = load_sheet("Leads Data")
    if not df_leads.empty and "Client ID" in df_leads.columns:
        cid = st.selectbox("Select Client ID:", df_leads["Client ID"].dropna().unique())
        if cid:
            st.dataframe(df_leads[df_leads["Client ID"] == cid], use_container_width=True, hide_index=True)
