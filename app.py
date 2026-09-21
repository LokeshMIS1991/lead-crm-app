import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sidharth Shutter CRM Database",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM CSS TO MATCH HTML INTERFACE EXACTLY
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #F8FAFC !important;
    }
    
    /* Top Header Bar */
    .header-bar {
        background-color: #FFFFFF;
        padding: 12px 24px;
        border-bottom: 1px solid #E2E8F0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .header-title {
        color: #164194;
        font-weight: 800;
        font-size: 20px;
        margin: 0;
    }
    
    .header-subtitle {
        color: #00A859;
        font-weight: 700;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0;
    }

    /* Tabs Styling - Matching Pill/Tab Bar in Screenshot */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 6px !important;
        gap: 8px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        color: #334155 !important;
        border: none !important;
        background-color: transparent !important;
    }

    /* Active Tab Highlight (Navy Blue Button Style) */
    .stTabs [aria-selected="true"] {
        background-color: #164194 !important;
        color: #FFFFFF !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }

    /* Remove Streamlit default tab bottom indicator line */
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* Content Card Container */
    .content-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        margin-top: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .worksheet-title {
        color: #164194;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .worksheet-sub {
        color: #64748B;
        font-size: 13px;
        margin-bottom: 20px;
    }

    /* Download Buttons Customization */
    .stDownloadButton>button {
        background-color: #164194 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        border: none !important;
        padding: 8px 16px !important;
    }

    .stDownloadButton>button:hover {
        background-color: #0E2D6B !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SAMPLE DATA SCHEMAS
# ---------------------------------------------------------
df_leads = pd.DataFrame([
    {
        "SR. NO": 1, "CLIENT ID": "SSA-Sep-26-0102", "DATE STAMP": "2026-09-15 10:30:00",
        "CLIENT NAME": "Rajesh Sharma", "COMPANY NAME": "Apex Logistics", "NUMBER": "+91 98290 12345",
        "EMAIL": "rajesh@apexlogistics.in", "PRODUCT": "Automatic Rolling Shutters", "QTY": 3,
        "ADDRESS": "Plot 12, VKIA", "CITY": "Jaipur", "STATE": "Rajasthan", "SOURCE": "India Mart",
        "ASSIGNED SALESPERSON": "Mansingh Rathore", "TYPE OF CLIENT": "New Buy",
        "QUOTATION STATUS": "Sent", "LEADS HANDLE BY": "Pooja", "QUOTATION SENT BY": "Dolly",
        "REMARKS": "High priority commercial requirement."
    },
    {
        "SR. NO": 2, "CLIENT ID": "SSA-Sep-26-0215", "DATE STAMP": "2026-09-15 11:15:00",
        "CLIENT NAME": "Sunil Verma", "COMPANY NAME": "Verma Builders", "NUMBER": "+91 94140 56789",
        "EMAIL": "s.verma@vermagroup.com", "PRODUCT": "Motorised Sliding Gates", "QTY": 1,
        "ADDRESS": "C-45, Nirman Nagar", "CITY": "Jaipur", "STATE": "Rajasthan", "SOURCE": "WhatsApp",
        "ASSIGNED SALESPERSON": "Sidharth Jain", "TYPE OF CLIENT": "Architect",
        "QUOTATION STATUS": "Sent", "LEADS HANDLE BY": "Dolly", "QUOTATION SENT BY": "Rishabh",
        "REMARKS": "Architect specified SSA gate automation."
    },
    {
        "SR. NO": 3, "CLIENT ID": "SSA-Sep-26-0340", "DATE STAMP": "2026-09-15 14:00:00",
        "CLIENT NAME": "Amit Patel", "COMPANY NAME": "Patel Warehousing", "NUMBER": "+91 98250 99887",
        "EMAIL": "amit@patelwh.com", "PRODUCT": "Dock Leveller", "QTY": 2,
        "ADDRESS": "GIDC Phase 3", "CITY": "Ahmedabad", "STATE": "Gujarat", "SOURCE": "Sales Email",
        "ASSIGNED SALESPERSON": "Jeevan Sharma", "TYPE OF CLIENT": "Contractor",
        "QUOTATION STATUS": "Not Sent", "LEADS HANDLE BY": "Rishabh", "QUOTATION SENT BY": "Other",
        "REMARKS": "Awaiting structural site dimensions."
    }
])

df_quotation = pd.DataFrame([
    {
        "CLIENT ID": "SSA-Sep-26-0102", "DATE STAMP": "2026-09-15 10:30:00", "CLIENT NAME": "Rajesh Sharma",
        "COMPANY NAME": "Apex Logistics", "NUMBER": "+91 98290 12345", "PRODUCT": "Automatic Rolling Shutters",
        "QUANTITY": 3, "CITY": "Jaipur", "SOURCE": "India Mart", "ASSIGNED SALESPERSON": "Mansingh Rathore",
        "QUOTATION STATUS": "Sent", "QUOTATION SHARED BY": "Dolly", "QUOTATION NUMBER": "SSA/2026-27/0182",
        "QUT. AMOUNT": 285000, "REMARKS": "Commercial quote shared with GST & transport."
    }
])

df_followup = pd.DataFrame([
    {
        "CLIENT ID": "SSA-Sep-26-0102", "QUOTATION NUMBER": "SSA/2026-27/0182", "CLIENT NAME": "Rajesh Sharma",
        "COMPANY NAME": "Apex Logistics", "CONTACT NUMBER": "+91 98290 12345", "PRODUCT": "Automatic Rolling Shutters",
        "QUOTATION AMOUNT": 285000, "FOLLOW UP DATE": "2026-09-16", "FOLLOWED BY": "Pooja",
        "CLIENT RESPONSE": "Client requested 5% discount for bulk payment.", "NEXT FOLLOW UP DATE": "2026-09-18", "STATUS": "In Discussion"
    }
])

df_process = pd.DataFrame([
    {
        "CLIENT ID": "SSA-Sep-26-0215", "QUOTATION NUMBER": "SSA/2026-27/0183", "PURCHASE ORDER NUMBER": "PO-VERMA-992",
        "QUT. AMOUNT": 145000, "ADVANCE AMOUNT": 50000, "START DATE": "2026-09-15", "PAYMENT STATUS": "Advance Received",
        "DRAWING STATUS": "Done", "MEASUREMENT": "Done", "PRODUCTION STATUS": "In Progress", "DISPATCH STATUS": "Pending",
        "OPERATIONAL NOTES": "Production underway at factory."
    }
])

# Helper function to convert dataframe to CSV string
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# ---------------------------------------------------------
# HEADER BAR
# ---------------------------------------------------------
st.markdown("""
    <div class="header-bar">
        <div>
            <div class="header-title">SIDHARTH SHUTTER & AUTOMATION</div>
            <div class="header-subtitle">CRM Database & Schema Architect</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# TABS (MATCHING TOP TAB NAVIGATION)
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📇 1. Leads Data",
    "📄 2. Quotation Sheet",
    "📞 3. Follow Up Tracker",
    "🚚 4. Process Order",
    "🔑 Streamlit secrets.toml Setup"
])

# ---------------------------------------------------------
# TAB 1: LEADS DATA
# ---------------------------------------------------------
with tab1:
    col_title, col_btn = st.columns([3, 1])
    with col_title:
        st.markdown("<div class='worksheet-title'>📊 Worksheet: <code>Leads Data</code></div>", unsafe_allow_html=True)
        st.markdown("<div class='worksheet-sub'>Stores incoming inquiries, customer contact details, lead sources, and salesperson assignments.</div>", unsafe_allow_html=True)
    with col_btn:
        st.download_button(
            label="📥 Download `Leads Data.csv`",
            data=convert_df_to_csv(df_leads),
            file_name="Leads Data.csv",
            mime="text/csv"
        )
    
    st.dataframe(df_leads, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# TAB 2: QUOTATION SHEET
# ---------------------------------------------------------
with tab2:
    col_title, col_btn = st.columns([3, 1])
    with col_title:
        st.markdown("<div class='worksheet-title'>📊 Worksheet: <code>Quotation Sheet</code></div>", unsafe_allow_html=True)
        st.markdown("<div class='worksheet-sub'>Tracks commercial quotation numbers, valuation amounts, statuses, and team member ownership.</div>", unsafe_allow_html=True)
    with col_btn:
        st.download_button(
            label="📥 Download `Quotation Sheet.csv`",
            data=convert_df_to_csv(df_quotation),
            file_name="Quotation Sheet.csv",
            mime="text/csv"
        )
    
    st.dataframe(df_quotation, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# TAB 3: FOLLOW UP TRACKER
# ---------------------------------------------------------
with tab3:
    col_title, col_btn = st.columns([3, 1])
    with col_title:
        st.markdown("<div class='worksheet-title'>📊 Worksheet: <code>Quotation Follow Up Tracker</code></div>", unsafe_allow_html=True)
        st.markdown("<div class='worksheet-sub'>Logs active communication logs, client responses, and scheduled follow-up dates.</div>", unsafe_allow_html=True)
    with col_btn:
        st.download_button(
            label="📥 Download `Follow Up Tracker.csv`",
            data=convert_df_to_csv(df_followup),
            file_name="Quotation Follow Up Tracker.csv",
            mime="text/csv"
        )
    
    st.dataframe(df_followup, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# TAB 4: PROCESS ORDER
# ---------------------------------------------------------
with tab4:
    col_title, col_btn = st.columns([3, 1])
    with col_title:
        st.markdown("<div class='worksheet-title'>📊 Worksheet: <code>Process Order</code></div>", unsafe_allow_html=True)
        st.markdown("<div class='worksheet-sub'>Tracks operational post-approval execution: drawings, production, payments, dispatch, and invoices.</div>", unsafe_allow_html=True)
    with col_btn:
        st.download_button(
            label="📥 Download `Process Order.csv`",
            data=convert_df_to_csv(df_process),
            file_name="Process Order.csv",
            mime="text/csv"
        )
    
    st.dataframe(df_process, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# TAB 5: SECRETS TOML SETUP
# ---------------------------------------------------------
with tab5:
    st.markdown("<div class='worksheet-title'>⚙️ Streamlit Configuration File: <code>.streamlit/secrets.toml</code></div>", unsafe_allow_html=True)
    st.markdown("<div class='worksheet-sub'>Copy and paste this snippet into your local project directory or Streamlit Community Cloud settings.</div>", unsafe_allow_html=True)
    
    secrets_code = """# .streamlit/secrets.toml
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/YOUR_GOOGLE_SHEET_ID_HERE/edit"
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
    st.code(secrets_code, language="toml")
