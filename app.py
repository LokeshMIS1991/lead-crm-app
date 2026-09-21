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
# CORPORATE BRAND UI ENGINE
# Primary Blue: #184B9C | Dark Blue: #0E2C68 | Accent Blue: #2965C1 | Emerald Green: #00A859
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* 1. Global Page Reset & Styling */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background-color: #F8FAFC !important;
        color: #0E2C68 !important;
    }

    header[data-testid="stHeader"] { 
        background-color: transparent !important; 
    }

    /* 2. Hide Unstyled Sidebar Strings */
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] span {
        display: none !important;
    }

    /* 3. Modernized Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #184B9C 0%, #0E2C68 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding-top: 1rem !important;
        box-shadow: 4px 0 20px rgba(14, 44, 104, 0.08) !important;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Sidebar Radio Item Customization */
    div[data-testid="stRadio"] label {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        font-size: 13.5px !important;
        font-weight: 500 !important;
        padding: 10px 14px !important;
        margin-bottom: 6px !important;
        border-radius: 8px !important;
        transition: all 0.2s ease-in-out !important;
        cursor: pointer !important;
    }
    div[data-testid="stRadio"] label:hover {
        background-color: rgba(255, 255, 255, 0.15) !important;
        transform: translateX(3px);
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        background-color: rgba(255, 255, 255, 0.3) !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 50% !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] {
        background: rgba(255, 255, 255, 0.2) !important;
        border-left: 4px solid #00A859 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] > div:first-child {
        background-color: #00A859 !important;
        border: 2px solid #FFFFFF !important;
    }

    /* Sidebar Logout Button */
    div[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(135deg, #00A859 0%, #008F4C 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(0, 168, 89, 0.25) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div[data-testid="stSidebar"] div.stButton > button:hover {
        background: linear-gradient(135deg, #008F4C 0%, #00753E 100%) !important;
        box-shadow: 0 6px 16px rgba(0, 168, 89, 0.35) !important;
        transform: translateY(-1px);
    }

    /* 4. Typography & Headers */
    .stMainBlockContainer h1, 
    .stMainBlockContainer h2, 
    .stMainBlockContainer h3, 
    .stMainBlockContainer h4 {
        color: #0E2C68 !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    .stMainBlockContainer label,
    .stMainBlockContainer label p {
        color: #184B9C !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        margin-bottom: 4px !important;
    }

    .main-header {
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #0E2C68 !important;
        margin-bottom: 20px !important;
        border-bottom: 2px solid #E2E8F0 !important;
        padding-bottom: 12px !important;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .section-title {
        color: #184B9C !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        margin-top: 18px !important;
        margin-bottom: 12px !important;
        padding-bottom: 6px !important;
        border-bottom: 1px solid #E2E8F0 !important;
        letter-spacing: -0.01em;
    }

    /* 5. Enhanced Form Container Cards & Login Box */
    div[data-testid="stForm"], .saas-card {
        background-color: #FFFFFF !important;
        border: 2px solid #184B9C !important;
        border-radius: 16px !important;
        padding: 32px 36px !important;
        box-shadow: 0 12px 32px rgba(14, 44, 104, 0.08) !important;
        margin-bottom: 20px !important;
        width: 100% !important;
    }

    /* INPUT FIELD CONTAINER - FORCED WHITE FILL & BLUE BORDER */
    div[data-baseweb="input"],
    div[data-baseweb="base-input"] {
        background-color: #FFFFFF !important;
        border: 2px solid #184B9C !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        transition: all 0.2s ease-in-out !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #0E2C68 !important;
        box-shadow: 0 0 0 3px rgba(24, 75, 156, 0.2) !important;
    }

    /* Input Text Field Inside */
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #0E2C68 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 12px !important;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #64748B !important;
        opacity: 0.8 !important;
    }

    /* Password Eye Icon Button Container */
    div[data-testid="stTextInput"] button {
        background-color: transparent !important;
        border: none !important;
    }

    div[data-testid="stTextInput"] button svg {
        fill: #184B9C !important;
        stroke: #184B9C !important;
    }

    /* CHECKBOX SQUARE CUSTOMIZATION (White Fill + Blue Border) */
    div[data-testid="stCheckbox"] [role="checkbox"] {
        background-color: #FFFFFF !important;
        border: 2px solid #184B9C !important;
        border-radius: 4px !important;
    }

    div[data-testid="stCheckbox"] [role="checkbox"][aria-checked="true"] {
        background-color: #184B9C !important;
        border-color: #184B9C !important;
    }

    div[data-testid="stCheckbox"] [role="checkbox"] svg {
        fill: #184B9C !important;
    }

    div[data-testid="stCheckbox"] [role="checkbox"][aria-checked="true"] svg {
        fill: #FFFFFF !important;
    }

    div[data-testid="stCheckbox"] label span p {
        color: #184B9C !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
    }

    /* Notification Popups (st.warning, st.error, st.success, st.info) */
    div[data-testid="stAlert"] {
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    div[data-testid="stAlert"] * {
        color: #1E293B !important;
    }

    div[data-testid="stAlert"] [data-testid="stNotificationContentWarning"] {
        background-color: #FEF3C7 !important;
        color: #92400E !important;
        border: 1px solid #FCD34D !important;
    }

    div[data-testid="stAlert"] [data-testid="stNotificationContentError"] {
        background-color: #FEE2E2 !important;
        color: #991B1B !important;
        border: 1px solid #FCA5A5 !important;
    }

    div[data-testid="stAlert"] [data-testid="stNotificationContentSuccess"] {
        background-color: #D1FAE5 !important;
        color: #065F46 !important;
        border: 1px solid #6EE7B7 !important;
    }

    div[data-testid="stAlert"] [data-testid="stNotificationContentInfo"] {
        background-color: #E0F2FE !important;
        color: #075985 !important;
        border: 1px solid #7DD3FC !important;
    }

    /* Form Submit Buttons */
    div[data-testid="stFormSubmitButton"] button,
    button[kind="primaryFormSubmit"] {
        background: linear-gradient(135deg, #00A859 0%, #008F4C 100%) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        padding: 12px 20px !important;
        margin-top: 15px !important;
        width: 100% !important;
        box-shadow: 0 4px 14px rgba(0, 168, 89, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    div[data-testid="stFormSubmitButton"] button:hover,
    button[kind="primaryFormSubmit"]:hover {
        background: linear-gradient(135deg, #008F4C 0%, #00753E 100%) !important;
        box-shadow: 0 6px 18px rgba(0, 168, 89, 0.4) !important;
        transform: translateY(-1px);
    }

    /* Standard Interactive Buttons */
    div.stButton > button {
        border-radius: 6px !important;
        border: 1px solid #CBD5E1 !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    /* 6. Tabs Styling */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"] div p {
        color: #64748B !important;
        font-size: 14px !important;
    }
    button[aria-selected="true"] {
        border-bottom: 3px solid #184B9C !important;
        background-color: rgba(24, 75, 156, 0.04) !important;
    }
    button[aria-selected="true"] div p {
        color: #184B9C !important;
        font-weight: 700 !important;
    }

    /* 7. Dashboard Metric Cards */
    .metric-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-left: 4px solid #184B9C !important;
        border-radius: 10px !important;
        padding: 16px 20px !important;
        box-shadow: 0 2px 8px rgba(14, 44, 104, 0.04) !important;
        margin-bottom: 10px !important;
    }
    .metric-card-green { 
        border-left-color: #00A859 !important; 
    }
    .metric-card h5 {
        color: #64748B !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        margin: 0 0 6px 0 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-card-green h5 { color: #00A859 !important; }
    .metric-card h3 {
        color: #0E2C68 !important;
        font-size: 26px !important;
        font-weight: 800 !important;
        margin: 0 !important;
    }

    /* 8. Queue & Activity Cards */
    .queue-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-left: 4px solid #184B9C !important;
        border-radius: 8px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 2px 6px rgba(14, 44, 104, 0.03) !important;
    }

    /* 9. Dataframes & Tables Wrapper */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        padding: 8px !important;
        box-shadow: 0 2px 8px rgba(14, 44, 104, 0.03) !important;
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

    navy = colors.HexColor("#184B9C")
    green = colors.HexColor("#00A859")
    dark_text = colors.HexColor("#0E2C68")

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
# AUTHENTICATION & SESSION MANAGEMENT
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "user_display_name" not in st.session_state:
    st.session_state.user_display_name = None

if "username" not in st.session_state:
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

# EXPLICIT AUTH GATEKEEPER - RUNS BEFORE SIDEBAR OR APP CONTENT
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, col, c2 = st.columns([1, 1.8, 1])
    with col:
        with st.form("login_form"):
            try:
                st.image("Company Logo.jpeg", use_container_width=True)
            except Exception:
                st.markdown("<h2 style='text-align: center; color: #184B9C; font-weight:800; letter-spacing:-0.02em;'>🏭 SIDHARTH SHUTTER</h2>", unsafe_allow_html=True)
            
            st.markdown("<p style='text-align: center; color: #64748B; font-weight: 600; font-size: 14px; margin-top: -10px; margin-bottom: 20px;'>Enterprise CRM & Operations Portal</p>", unsafe_allow_html=True)
            
            # 1. Username Field
            user_input = st.text_input("Username", placeholder="e.g. admin or dolly").strip().lower()
            
            # 2. Password Field
            if "show_pwd" not in st.session_state:
                st.session_state.show_pwd = False

            pass_type = "text" if st.session_state.get("show_pwd_checkbox", False) else "password"
            pass_input = st.text_input("Password", type=pass_type, placeholder="Enter password").strip()

            # 3. Show Password Checkbox
            st.checkbox("Show Password", key="show_pwd_checkbox")

            submit = st.form_submit_button("🔑 Login to Dashboard", use_container_width=True)

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
    st.stop()

# ---------------------------------------------------------
# DYNAMIC ROLE-BASED SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    try:
        st.image("Company Logo.jpeg", use_container_width=True)
    except Exception:
        st.write("🏭 **SSA CRM**")
        
    st.markdown(f"<h3 style='margin-bottom:2px; font-size: 16px !important; font-weight:700; color:#FFFFFF;'>👋 {st.session_state.user_display_name}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #00A859 !important; font-weight:600; font-size:12px !important; text-transform:uppercase; letter-spacing:0.05em;'>Role: {st.session_state.user_role}</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border:none; border-top: 1px solid rgba(255,255,255,0.15); margin: 12px 0;'>", unsafe_allow_html=True)

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

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.user_role = None
        st.session_state.user_display_name = None
        st.rerun()

# ---------------------------------------------------------
# LEAD CAPTURE PORTAL
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

# ---------------------------------------------------------
# ADMIN PERFORMANCE & PROGRESS CONTROL MODULE
# ---------------------------------------------------------
elif menu == "📈 Admin Performance & Progress Control":
    st.markdown("<div class='main-header'>📈 Performance & Operational Control Hub</div>", unsafe_allow_html=True)

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
                st.bar_chart(data=perf_matrix, x="Salesperson", y="Total Leads Assigned", color="#184B9C")
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
                    st.markdown(f"<p style='color:#184B9C; font-weight:700;'>Active Leads for {selected_emp}: {len(emp_leads)}</p>", unsafe_allow_html=True)
                    st.dataframe(emp_leads, use_container_width=True, hide_index=True)
                with e2:
                    st.markdown(f"<p style='color:#184B9C; font-weight:700;'>Issued Quotes for {selected_emp}: {len(emp_quotes)}</p>", unsafe_allow_html=True)
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
                st.bar_chart(data=q_status_counts, x="Quote Status", y="Count", color="#184B9C")
            else:
                st.info("No quotation pipeline data available.")

# ---------------------------------------------------------
# USER MANAGEMENT (ADMIN ONLY)
# ---------------------------------------------------------
elif menu == "👥 User Management (Admin)":
    st.markdown("<div class='main-header'>👥 User Credentials & Role Management</div>", unsafe_allow_html=True)
    
    df_users = load_sheet("Users")
    
    st.markdown("<div class='section-title'>📋 Registered CRM Users</div>", unsafe_allow_html=True)
    if not df_users.empty:
        st.dataframe(df_users, use_container_width=True, hide_index=True)
    else:
        st.warning("No users found in the 'Users' worksheet tab.")

    st.markdown("<div class='section-title'>➕ Add New User Credentials</div>", unsafe_allow_html=True)
    with st.form("add_user_form", clear_on_submit=True):
        u1, u2 = st.columns(2)
        with u1:
            new_username = st.text_input("Username *").strip().lower()
            new_password = st.text_input("Password *", type="password")
        with u2:
            new_role = st.selectbox("Role *", ["Admin", "Salesperson", "Back-Office", "Operations"])
            new_disp_name = st.text_input("Display Name *")
            
        submit_u = st.form_submit_button("💾 Create User Account", use_container_width=True)
        if submit_u:
            if not new_username or not new_password or not new_disp_name:
                st.error("Please complete all required fields.")
            else:
                new_row = {
                    "Username": new_username,
                    "Password": new_password,
                    "Role": new_role,
                    "Display Name": new_disp_name
                }
                conn = get_connection()
                if conn:
                    df_u_ex = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="Users")
                    df_u_up = pd.concat([df_u_ex, pd.DataFrame([new_row])], ignore_index=True)
                    conn.update(spreadsheet=SPREADSHEET_URL, worksheet="Users", data=df_u_up)
                    st.success(f"✅ User '{new_username}' added to Google Sheets!")

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
                    <b style='color:#184B9C; font-size:15px;'>{client_name}</b> &nbsp;|&nbsp; <span style='color:#64748B; font-size:13px;'>Quote: {quote_no}</span><br>
                    <span style='font-size:13.5px;'>📞 <b>Contact:</b> {phone} &nbsp;|&nbsp; 💰 <b>Amount:</b> ₹{amt} &nbsp;|&nbsp; 👤 <b>Rep:</b> {row.get('Assigned Salesperson', 'Unassigned')}</span>
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
                st.markdown("<hr style='border:none; border-top:1px dashed #E2E8F0; margin: 15px 0;'>", unsafe_allow_html=True)
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
