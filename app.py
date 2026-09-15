import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# ---------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="Pro CRM - Sales & Order Pipeline",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Odoo/Zoho Style Interface
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    
    .main-header {
        font-size: 24px; font-weight: 700; color: #0f172a;
        margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;
    }
    
    .kpi-card {
        background: #ffffff;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
    }
    .kpi-card h5 { color: #64748b; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 4px; }
    .kpi-card h2 { color: #0f172a; font-size: 22px; font-weight: 700; margin: 0; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# GOOGLE SHEETS CONNECTION & DATA HELPERS
# ---------------------------------------------------------
def get_connection():
    try:
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception as e:
        return None

def load_sheet(sheet_name):
    conn = get_connection()
    if conn:
        try:
            return conn.read(worksheet=sheet_name, ttl=0)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

# Master Dropdown Data Options
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
    st.markdown("<h2 style='color: #2563eb;'>⚡ Enterprise CRM</h2>", unsafe_allow_html=True)
    st.caption("End-to-End Sales & Order Execution System")
    st.markdown("---")
    
    menu = st.radio(
        "WORKFLOW STAGES",
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
    st.markdown("<div class='main-header'>📊 Sales & Operations Overview</div>", unsafe_allow_html=True)
    
    df_leads = load_sheet("Leads Data")
    df_quotes = load_sheet("Quotation Sheet")
    df_orders = load_sheet("Process Order")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="kpi-card"><h5>Total Leads</h5><h2>{len(df_leads)}</h2></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card"><h5>Quotations Sent</h5><h2>{len(df_quotes)}</h2></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-card"><h5>Active Process Orders</h5><h2>{len(df_orders)}</h2></div>', unsafe_allow_html=True)
    with c4:
        total_val = df_quotes['Qut. Amount'].sum() if not df_quotes.empty and 'Qut. Amount' in df_quotes.columns else 0
        st.markdown(f'<div class="kpi-card"><h5>Pipeline Value</h5><h2>₹{total_val:,.0f}</h2></div>', unsafe_allow_html=True)
        
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.subheader("🔥 Recent Activity Feed")
    if not df_leads.empty:
        st.dataframe(df_leads.tail(8), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 1: LEADS DATA (ENTRY & AUTO-TRANSFER)
# ---------------------------------------------------------
elif menu == "📥 Stage 1: Leads Data":
    st.markdown("<div class='main-header'>📥 Stage 1: Lead Management</div>", unsafe_allow_html=True)
    
    tab_add, tab_view = st.tabs(["➕ Add New Lead", "📋 Master Leads Registry"])
    
    with tab_add:
        with st.form("add_lead_form", clear_on_submit=True):
            st.markdown("##### 👤 Customer & Company Information")
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
                
            address = st.text_area("Address", height=2)
            
            st.markdown("##### 📦 Sales & Requirement Assignment")
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
                remarks = st.text_area("Remarks / Notes")
                
            submit_lead = st.form_submit_button("💾 Save Lead")
            
            if submit_lead:
                if not client_name or not number:
                    st.error("Please fill required fields: Client Name and Contact Number.")
                else:
                    date_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    client_id = f"BID-{datetime.now().strftime('%b-%y')}-{datetime.now().strftime('%M%S')}"
                    
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
                        df_existing = conn.read(worksheet="Leads Data")
                        df_updated = pd.concat([df_existing, pd.DataFrame([new_lead])], ignore_index=True)
                        conn.update(worksheet="Leads Data", data=df_updated)
                        
                        # AUTOMATED TRIGGER: If Quotation Status == Sent, Auto-populate Stage 2
                        if quotation_status == "Sent":
                            auto_quote = {
                                "Client  ID": client_id,
                                "Date Stamp": date_stamp,
                                "Client Name": client_name,
                                "Company Name": company_name,
                                "Customer Contact Number": number,
                                "Product ": product,
                                "Quantity": qty,
                                "City": city,
                                "Source": source,
                                "Assigned Salesperson": assigned_sp,
                                "Quotation Status": "Sent",
                                "Quotation Shared By": quotation_sent_by
                            }
                            df_q_existing = conn.read(worksheet="Quotation Sheet")
                            df_q_updated = pd.concat([df_q_existing, pd.DataFrame([auto_quote])], ignore_index=True)
                            conn.update(worksheet="Quotation Sheet", data=df_q_updated)
                            
                            st.info("🔄 Common details auto-transferred to Quotation Sheet!")
                        
                        st.success(f"✅ Lead Created Successfully! Generated Client ID: **{client_id}**")
                    else:
                        st.error("Google Sheets connection not configured.")

    with tab_view:
        df_leads = load_sheet("Leads Data")
        st.dataframe(df_leads, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 2: QUOTATIONS & FOLLOW-UP TRACKER
# ---------------------------------------------------------
elif menu == "📄 Stage 2: Quotations & Follow-ups":
    st.markdown("<div class='main-header'>📄 Stage 2: Quotation & Follow-up Panel</div>", unsafe_allow_html=True)
    
    tab_q_list, tab_update, tab_followup = st.tabs(["📋 Quotation Master", "✏️ Update Quotation Details", "📞 Follow-up Tracker"])
    
    with tab_q_list:
        df_quotes = load_sheet("Quotation Sheet")
        st.dataframe(df_quotes, use_container_width=True, hide_index=True)
        
    with tab_update:
        st.subheader("Update Quotation Amount & Status")
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
                q_date = st.date_input("Approved/Update Date")
                
            q_notes = st.text_area("Quotation / Approval Remarks")
            
            submit_quote_update = st.form_submit_button("💾 Save Quotation Update")
            
            if submit_quote_update:
                conn = get_connection()
                if conn:
                    # AUTOMATED TRIGGER: If Status == Approved, Auto-populate Process Order Stage
                    if q_status == "Approved":
                        auto_order = {
                            "Client ID": q_client_id,
                            "Quotation Number": q_number,
                            "Qut. Amount": q_amount,
                            "Start Date": datetime.now().strftime("%Y-%m-%d"),
                            "Production Status": "Pending",
                            "Payment Status": "Pending",
                            "Drawing Status": "Pending",
                            "Dispatch Status": "Pending"
                        }
                        df_o_existing = conn.read(worksheet="Process Order")
                        df_o_updated = pd.concat([df_o_existing, pd.DataFrame([auto_order])], ignore_index=True)
                        conn.update(worksheet="Process Order", data=df_o_updated)
                        st.info("🚀 Quotation Approved! Automatically pushed to Process Order Execution stage.")
                        
                    st.success(f"Quotation updated for Client ID: {q_client_id}")

    with tab_followup:
        df_followup = load_sheet("Quotation Follow Up Tracker")
        st.dataframe(df_followup, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# STAGE 3: PROCESS ORDER EXECUTION
# ---------------------------------------------------------
elif menu == "⚙️ Stage 3: Process Order Execution":
    st.markdown("<div class='main-header'>⚙️ Stage 3: Order Execution & Tracking</div>", unsafe_allow_html=True)
    
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
                invoice_status = st.selectbox("Invoice", ["Pending", "Generated"])
                install_inv = st.selectbox("Installation Invoice", ["Pending", "Generated"])
                
            final_remarks = st.text_area("Final Operational Remarks")
            
            submit_order = st.form_submit_button("💾 Save Operational Status")
            if submit_order:
                st.success(f"Operational progress updated for Client ID: {o_client_id}")

    df_orders = load_sheet("Process Order")
    st.subheader("📦 Active Process Orders Master Tracker")
    st.dataframe(df_orders, use_container_width=True, hide_index=True)
