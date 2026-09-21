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

# ---------------------------------------------------------
# BRAND STYLING & CUSTOM COLOR OVERRIDES
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Top Navigation Header Bar Override */
    header[data-testid="stHeader"] {
        background-color: #F8FAFC !important;
    }
    
    header[data-testid="stHeader"] * {
        color: #164194 !important;
    }

    /* Global App Background */
    .stApp {
        background-color: #F8FAFC !important;
    }
    
    /* Left Panel Sidebar: Exact Brand Navy Blue */
    [data-testid="stSidebar"] {
        background-color: #164194 !important;
        color: #FFFFFF !important;
        border-right: 2px solid #0F3275 !important;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* Sidebar Oval Logo Badge */
    .sidebar-oval-logo {
        background-color: #FFFFFF;
        border: 2px solid #00A859;
        border-radius: 50px / 30px;
        padding: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        text-align: center;
        margin-bottom: 12px;
    }
    
    .sidebar-oval-logo img {
        max-width: 90%;
        border-radius: 20px;
    }

    /* Page Main Header */
    .main-header {
        font-size: 26px;
        font-weight: 800;
        color: #164194;
        margin-bottom: 10px;
        border-bottom: 3px solid #00A859;
        padding-bottom: 8px;
        letter-spacing: -0.5px;
    }

    /* Top Right Header Logo Position */
    .top-right-logo {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding-bottom: 10px;
    }

    /* KPI Summary Cards */
    .kpi-card {
        background: #FFFFFF;
        padding: 20px 15px;
        border-radius: 12px;
        border-left: 6px solid #164194;
        border-right: 1px solid #CBD5E1;
        border-top: 1px solid #CBD5E1;
        border-bottom: 1px solid #CBD5E1;
        box-shadow: 0 4px 12px rgba(22, 65, 148, 0.08);
        text-align: center;
    }
    
    .kpi-card-green {
        border-left: 6px solid #00A859;
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

    /* Form Field Label Color Customization */
    .stTextInput label, .stSelectbox label, .stNumberInput label, .stTextArea label, .stDateInput label {
        color: #164194 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }

    /* Form Inputs and Dropdowns */
    .stTextInput>div>div>input, 
    .stSelectbox>div>div, 
    .stSelectbox [data-baseweb="select"]>div,
    .stTextArea>div>div>textarea,
    .stDateInput>div>div,
    .stDateInput input {
        background-color: #FFFFFF !important;
        color: #164194 !important;
        border: 1.5px solid #164194 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    .stSelectbox [data-baseweb="select"] * {
        color: #164194 !important;
    }

    .stDateInput div[role="button"] {
        background-color: #FFFFFF !important;
        color: #164194 !important;
    }

    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #164194 !important;
    }

    .stTextInput>div>div>input:focus, 
    .stSelectbox>div>div:focus, 
    .stTextArea>div>div>textarea:focus, 
    .stDateInput input:focus {
        border-color: #00A859 !important;
        box-shadow: 0 0 0 2px rgba(0, 168, 89, 0.2) !important;
    }

    /* Quantity Box Styling */
    .stNumberInput input {
        background-color: #E0F2FE !important;
        color: #164194 !important;
        font-weight: 800 !important;
    }
    
    .stNumberInput>div>div {
        background-color: #E0F2FE !important;
        border: 1.5px solid #164194 !important;
        border-radius: 8px !important;
    }

    .stNumberInput button {
        background-color: #164194 !important;
        color: #FFFFFF !important;
        border: none !important;
    }

    /* Buttons */
    .stButton>button, div[data-testid="stFormSubmitButton"]>button {
        background-color: #164194 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 700 !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover, div[data-testid="stFormSubmitButton"]>button:hover {
        background-color: #00A859 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(0, 168, 89, 0.35) !important;
    }
    
    /* Accordion / Expander */
    .stExpander [data-baseweb="accordion"] [role="button"] {
        background-color: #164194 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }

    .stExpander [data-baseweb="accordion"] [role="button"] * {
        color: #FFFFFF !important;
    }

    /* Permanent Red Tab Labels */
    .stTabs [data-baseweb="tab"],
    .stTabs [data-baseweb="tab"] *,
    .stTabs [data-baseweb="tab-list"] button,
    .stTabs [data-baseweb="tab-list"] button *,
    .stTabs [aria-selected="true"],
    .stTabs [aria-selected="true"] *,
    .stTabs [aria-selected="false"],
    .stTabs [aria-selected="false"] * {
        color: #FF0000 !important;
        fill: #FF0000 !important;
        font-weight: 800 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #FF0000 !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #FF0000 !important;
    }

    /* Container Box */
    [data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #164194 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 10px rgba(22, 65, 148, 0.08) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# GOOGLE SHEETS CONNECTION & DATA HELPERS
# ---------------------------------------------------------
def get_connection():
    try:
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {e}")
        return None

def load_sheet(sheet_name):
    conn = get_connection()
    if conn:
        try:
            return conn.read(worksheet=sheet_name, ttl=0)
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
            try:
                st.image("Company_Logo.png", use_container_width=True)
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
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<div class='sidebar-oval-logo'>", unsafe_allow_html=True)
    try:
        st.image("Company Logo.jpeg", use_container_width=True)
    except Exception:
        try:
            st.image("Company_Logo.png", use_container_width=True)
        except Exception:
            pass
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; font-size: 20px; font-weight: 800; color: #FFFFFF !important; margin-top: -5px;'>SIDHARTH SHUTTER</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-weight: 700; color: #00A859 !important; margin-top: -12px;'>CRM & Operational Pipeline</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio(
        "WORKFLOW NAVIGATION",
        [
            "📊 Executive Dashboard",
            "📥 Stage 1: Leads Data",
            "📄 Stage 2: Quotations & Follow-ups",
            "⚙️ Stage 3: Process Order Execution"
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
    st.subheader("🔥 Recent Activity Registry")
    if not df_leads.empty:
        st.dataframe(df_leads.tail(8), use_container_width=True, hide_index=True)

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
                
            submit_lead = st.form_submit_button("💾 Save Lead")
            
            if submit_lead:
                if not client_name or not number:
                    st.error("Please fill required fields: Client Name and Contact Number.")
                else:
                    date_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    client_id = f"SSA-{datetime.now().strftime('%b-%y')}-{datetime.now().strftime('%M%S')}"
                    
                    df_existing_leads = load_sheet("Leads Data")
                    new_lead = {
                        "Sr. No": len(df_existing_leads) + 1,
                        "Client ID": client_id,
                        "Date Stamp": date_stamp,
                        "Client Name": client_name,
                        "Company Name": company_name,
                        "Number": number,
                        "Email": email,
                        "Product": product,
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
                        df_updated = pd.concat([df_existing_leads, pd.DataFrame([new_lead])], ignore_index=True)
                        conn.update(worksheet="Leads Data", data=df_updated)
                        
                        if quotation_status == "Sent":
                            auto_quote = {
                                "Client ID": client_id,
                                "Date Stamp": date_stamp,
                                "Client Name": client_name,
                                "Company Name": company_name,
                                "Customer Contact Number": number,
                                "Product": product,
                                "Quantity": qty,
                                "City": city,
                                "Source": source,
                                "Assigned Salesperson": assigned_sp,
                                "Quotation Status": "Sent",
                                "Quotation Shared By": quotation_sent_by,
                                "Qut. Amount": 0
                            }
                            df_q_existing = load_sheet("Quotation Sheet")
                            df_q_updated = pd.concat([df_q_existing, pd.DataFrame([auto_quote])], ignore_index=True)
                            conn.update(worksheet="Quotation Sheet", data=df_q_updated)
                            st.info("🔄 Lead saved & common details auto-transferred to Quotation Sheet!")
                        
                        st.success(f"✅ Lead Created Successfully! Generated Client ID: **{client_id}**")
                    else:
                        st.error("Google Sheets connection error. Please verify secrets.toml settings.")

    with tab_view:
        df_leads = load_sheet("Leads Data")
        st.dataframe(df_leads, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 2: QUOTATIONS & FOLLOW-UP TRACKER
# ---------------------------------------------------------
elif menu == "📄 Stage 2: Quotations & Follow-ups":
    render_header("📄 Stage 2: Quotations & Follow-up Panel")
    
    tab_q_list, tab_update, tab_followup = st.tabs(["📋 Quotation Master", "✏️ Update Quotation Details", "📞 Follow-up Tracker"])
    
    with tab_q_list:
        df_quotes = load_sheet("Quotation Sheet")
        st.dataframe(df_quotes, use_container_width=True, hide_index=True)
        
    with tab_update:
        st.subheader("Update Commercial Quotation Details")
        with st.form("update_quote_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                q_client_id = st.text_input("Client ID *")
                q_number = st.text_input("Quotation Number (e.g. SSA/2025-26/1827)")
            with c2:
                q_amount = st.number_input("Quotation Amount (₹)", min_value=0, step=1000)
                q_status = st.selectbox("Quotation Status", ["Sent", "Approved", "Revised", "Cancelled"])
            with c3:
                q_shared_by = st.selectbox("Quotation Shared By", TEAM_MEMBERS)
                q_date = st.date_input("Update Date")
                
            q_notes = st.text_area("Quotation / Approval Remarks")
            
            submit_quote_update = st.form_submit_button("💾 Save Quotation Update")
            
            if submit_quote_update:
                if not q_client_id:
                    st.error("Client ID is required to update quotation records.")
                else:
                    conn = get_connection()
                    if conn:
                        df_q_existing = load_sheet("Quotation Sheet")
                        
                        # Check if record exists to update, or add a new record
                        if not df_q_existing.empty and "Client ID" in df_q_existing.columns and q_client_id in df_q_existing["Client ID"].values:
                            idx = df_q_existing[df_q_existing["Client ID"] == q_client_id].index[0]
                            df_q_existing.loc[idx, "Quotation Number"] = q_number
                            df_q_existing.loc[idx, "Qut. Amount"] = q_amount
                            df_q_existing.loc[idx, "Quotation Status"] = q_status
                            df_q_existing.loc[idx, "Quotation Shared By"] = q_shared_by
                            df_q_existing.loc[idx, "Date Stamp"] = str(q_date)
                            if "Remarks" in df_q_existing.columns:
                                df_q_existing.loc[idx, "Remarks"] = q_notes
                            df_q_updated = df_q_existing
                        else:
                            quote_entry = {
                                "Client ID": q_client_id,
                                "Quotation Number": q_number,
                                "Qut. Amount": q_amount,
                                "Quotation Status": q_status,
                                "Quotation Shared By": q_shared_by,
                                "Date Stamp": str(q_date),
                                "Remarks": q_notes
                            }
                            df_q_updated = pd.concat([df_q_existing, pd.DataFrame([quote_entry])], ignore_index=True)
                        
                        conn.update(worksheet="Quotation Sheet", data=df_q_updated)
                        
                        # Auto-move to Process Order when status becomes Approved
                        if q_status == "Approved":
                            df_o_existing = load_sheet("Process Order")
                            auto_order = {
                                "Client ID": q_client_id,
                                "Quotation Number": q_number,
                                "Qut. Amount": q_amount,
                                "Start Date": datetime.now().strftime("%Y-%m-%d"),
                                "Production Status": "Pending",
                                "Payment Status": "Pending",
                                "Drawing Status": "Pending",
                                "Dispatch Status": "Pending",
                                "Purchase Order Number": "",
                                "Advance Amount": 0,
                                "Measurement Status": "Pending",
                                "Document Submission": "Pending",
                                "Material Receiving": "Pending",
                                "Invoice Status": "Pending",
                                "Installation Invoice": "Pending",
                                "Operational Notes": q_notes
                            }
                            df_o_updated = pd.concat([df_o_existing, pd.DataFrame([auto_order])], ignore_index=True)
                            conn.update(worksheet="Process Order", data=df_o_updated)
                            st.info("🚀 Quotation Approved! Automatically moved to Process Order Execution stage.")
                            
                        st.success(f"Quotation updated successfully for Client ID: **{q_client_id}**")

    with tab_followup:
        df_followup = load_sheet("Quotation Follow Up Tracker")
        st.dataframe(df_followup, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 3: PROCESS ORDER EXECUTION
# ---------------------------------------------------------
elif menu == "⚙️ Stage 3: Process Order Execution":
    render_header("⚙️ Stage 3: Order Execution & Operations")
    
    with st.expander("🔄 Update Operational Status (Production/Payment/Dispatch)", expanded=True):
        with st.form("process_order_form"):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                o_client_id = st.text_input("Client ID *")
                po_number = st.text_input("Purchase Order Number")
                advance_amt = st.number_input("Advance Amount (₹)", min_value=0, step=1000)
            with c2:
                payment_status = st.selectbox("Payment Status", ["Pending", "Advance Received", "Full Done"])
                drawing_status = st.selectbox("Drawing Status", ["Pending", "In Review", "Done"])
                measurement_status = st.selectbox("Measurement", ["Pending", "Done"])
            with c3:
                production_status = st.selectbox("Production Status", ["Pending", "In Progress", "Done"])
                dispatch_status = st.selectbox("Dispatch Status", ["Pending", "Dispatched", "Delivered"])
                doc_sub = st.selectbox("Document Submission", ["Pending", "Done"])
            with c4:
                mat_rec = st.selectbox("Material Receiving", ["Pending", "Done"])
                invoice_status = st.selectbox("Invoice Status", ["Pending", "Generated"])
                install_inv = st.selectbox("Installation Invoice", ["Pending", "Generated"])
                
            final_remarks = st.text_area("Operational Notes")
            
            submit_order = st.form_submit_button("💾 Save Operational Status")
            
            if submit_order:
                if not o_client_id:
                    st.error("Client ID is required to save operational status.")
                else:
                    conn = get_connection()
                    if conn:
                        df_orders_existing = load_sheet("Process Order")
                        
                        order_data = {
                            "Client ID": o_client_id,
                            "Purchase Order Number": po_number,
                            "Advance Amount": advance_amt,
                            "Payment Status": payment_status,
                            "Drawing Status": drawing_status,
                            "Measurement Status": measurement_status,
                            "Production Status": production_status,
                            "Dispatch Status": dispatch_status,
                            "Document Submission": doc_sub,
                            "Material Receiving": mat_rec,
                            "Invoice Status": invoice_status,
                            "Installation Invoice": install_inv,
                            "Operational Notes": final_remarks,
                            "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        # Update row if Client ID exists, otherwise append
                        if not df_orders_existing.empty and "Client ID" in df_orders_existing.columns and o_client_id in df_orders_existing["Client ID"].values:
                            idx = df_orders_existing[df_orders_existing["Client ID"] == o_client_id].index[0]
                            for key, val in order_data.items():
                                df_orders_existing.loc[idx, key] = val
                            df_orders_updated = df_orders_existing
                        else:
                            df_orders_updated = pd.concat([df_orders_existing, pd.DataFrame([order_data])], ignore_index=True)
                            
                        conn.update(worksheet="Process Order", data=df_orders_updated)
                        st.success(f"✅ Operational progress saved to Google Sheets for Client ID: **{o_client_id}**")

    df_orders = load_sheet("Process Order")
    st.subheader("📦 Active Operational Orders Master Tracker")
    st.dataframe(df_orders, use_container_width=True, hide_index=True)
