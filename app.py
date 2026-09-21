import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sidharth CRM", layout="wide", page_icon="🏗️")

# --- 1. AUTHENTICATION SYSTEM ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.full_name = None

if not st.session_state.authenticated:
    st.title("🛡️ Sidharth Shutter & Automation - CRM Portal")
    with st.form("login_form"):
        username = st.text_input("Username").lower().strip()
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if username in st.secrets["passwords"] and st.secrets["passwords"][username] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = st.secrets["roles"][username]
                st.session_state.full_name = st.secrets["names"][username]
                st.rerun()
            else:
                st.error("Invalid Username or Password")
    st.stop()

# --- 2. DATA CONNECTION & CACHING ---
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=15)
def load_data():
    df = conn.read(worksheet="Sheet1")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title(f"👤 {st.session_state.full_name}")
st.sidebar.caption(f"Role: **{st.session_state.role}**")
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()

# --- 4. PROFILE WORKSPACES ---

# ==========================================
# PROFILE A: LEAD INTAKE EXECUTIVE (e.g., Pooja)
# ==========================================
if st.session_state.role == "Lead Intake Executive":
    st.title("➕ New Lead Entry Workspace")
    
    with st.form("new_lead_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        c_name = col1.text_input("Client Name *")
        comp_name = col2.text_input("Company Name")
        phone = col1.text_input("Phone Number *")
        email = col2.text_input("Email Address")
        address = col1.text_area("Address")
        city = col2.text_input("City")
        state = col1.text_input("State")
        
        product = col2.selectbox("Product", ["Automatic Rolling Shutters", "Motors", "Boom Barriers", "Sliding Gates", "Other"])
        qty = col1.number_input("Quantity", min_value=1, value=1)
        source = col2.selectbox("Source", ["WhatsApp", "IndiaMart", "Marketing Team", "Phone Call", "Enquiry Email"])
        c_type = col1.selectbox("Client Type", ["New Buy", "Service"])
        
        assigned_rep = col2.selectbox("Assign Salesperson", ["Albert", "Mansingh Rathore", "Deepak Sethiya", "Jeevan Sharma"])
        
        if st.form_submit_button("Create & Route Lead"):
            if not c_name or not phone:
                st.error("Client Name and Phone are required!")
            else:
                new_id = f"BID-{datetime.now().strftime('%b-%y')}-{len(df)+1:04d}"
                new_entry = pd.DataFrame([{
                    "client_id": new_id,
                    "date_stamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "client_name": c_name, "company_name": comp_name, "phone": phone, "email": email,
                    "address": address, "city": city, "state": state, "product": product, "qty": qty,
                    "source": source, "client_type": c_type, "assigned_salesperson": assigned_rep,
                    "quotation_status": "Pending", "quotation_final_status": "Pending",
                    "approved_date": "", "drive_url": "", "final_status": "Pending", "remarks": "Lead created by Intake."
                }])
                updated_df = pd.concat([df, new_entry], ignore_index=True)
                conn.update(worksheet="Sheet1", data=updated_df)
                st.success(f"Lead Created! Assigned to {assigned_rep} with ID: {new_id}")
                st.cache_data.clear()

# ==========================================
# PROFILE B: SALES REPRESENTATIVE (e.g., Albert)
# ==========================================
elif st.session_state.role == "Sales Representative":
    st.title(f"📊 My Sales Portal - {st.session_state.full_name}")
    
    # Filter rep's specific data
    my_leads = df[df['assigned_salesperson'] == st.session_state.full_name]
    
    # Performance Metrics
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    tot = len(my_leads)
    done = len(my_leads[my_leads['final_status'] == 'Done'])
    drop = len(my_leads[my_leads['final_status'] == 'Cancled'])
    conv = round((done / tot * 100), 1) if tot > 0 else 0
    
    kpi1.metric("Total Assigned", tot)
    kpi2.metric("Closed / Done", done)
    kpi3.metric("Dropped", drop)
    kpi4.metric("Conversion Rate", f"{conv}%")
    
    st.markdown("---")
    st.subheader("🔔 My Active Task Queue")
    
    active_tasks = my_leads[~my_leads['final_status'].isin(['Done', 'Cancled'])]
    
    for idx, row in active_tasks.iterrows():
        badge = "🔴 HOT" if row['final_status'] == "In Discussion" else "🟡 PENDING"
        with st.expander(f"{badge} | {row['client_id']} - {row['client_name']} ({row['company_name']})"):
            st.write(f"**Phone:** {row['phone']} | **Location:** {row['city']}, {row['state']}")
            st.write(f"**Requirement:** {row['product']} (Qty: {row['qty']})")
            st.write(f"**Quote Status:** {row['quotation_status']} | **Folder:** {row['drive_url']}")
            
            with st.form(key=f"rep_form_{row['client_id']}"):
                f_status = st.selectbox("Update Final Status", ["Pending", "In Discussion", "CallBack", "Done", "Cancled"], index=0)
                rem = st.text_area("Add Call Notes / Remarks", value=str(row['remarks']))
                
                if st.form_submit_button("Update Task"):
                    df.loc[df['client_id'] == row['client_id'], 'final_status'] = f_status
                    df.loc[df['client_id'] == row['client_id'], 'remarks'] = rem
                    conn.update(worksheet="Sheet1", data=df)
                    st.success("Task updated!")
                    st.cache_data.clear()

# ==========================================
# PROFILE C: QUOTATION OFFICER (e.g., Kirti)
# ==========================================
elif st.session_state.role == "Quotation Officer":
    st.title("📄 Quotation Dispatch Queue")
    
    quote_queue = df[df['quotation_status'].isin(['Pending', 'In Progress'])]
    st.caption(f"Pending Quotation Requests: **{len(quote_queue)}**")
    
    for idx, row in quote_queue.iterrows():
        with st.expander(f"📋 Quote Request for {row['client_id']} - {row['company_name']}"):
            st.write(f"**Client:** {row['client_name']} | **Product:** {row['product']} (Qty: {row['qty']})")
            st.write(f"**Assigned Rep:** {row['assigned_salesperson']}")
            
            with st.form(key=f"quote_form_{row['client_id']}"):
                q_status = st.selectbox("Quotation Status", ["Pending", "Sent", "Approved", "Not Sent"])
                drive_link = st.text_input("Google Drive Folder/PDF URL", value=str(row['drive_url']))
                
                if st.form_submit_button("Submit Quotation"):
                    df.loc[df['client_id'] == row['client_id'], 'quotation_status'] = q_status
                    df.loc[df['client_id'] == row['client_id'], 'drive_url'] = drive_link
                    if q_status == "Approved":
                        df.loc[df['client_id'] == row['client_id'], 'approved_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    conn.update(worksheet="Sheet1", data=df)
                    st.success("Quotation updated and attached!")
                    st.cache_data.clear()

# ==========================================
# PROFILE D: ADMIN / MANAGER (Sidharth Jain)
# ==========================================
elif st.session_state.role == "Sales Manager / Admin":
    st.title("🛡️ Master Executive Control")
    
    st.subheader("System KPIs")
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Total System Leads", len(df))
    a2.metric("Total Revenue Deals", len(df[df['final_status'] == 'Done']))
    a3.metric("Pending Quotes", len(df[df['quotation_status'] == 'Pending']))
    a4.metric("Active Reps", df['assigned_salesperson'].nunique())
    
    st.markdown("---")
    st.subheader("🔁 Bulk Lead Reassignment")
    c1, c2, c3 = st.columns(3)
    from_r = c1.selectbox("From Rep", df['assigned_salesperson'].dropna().unique())
    to_r = c2.selectbox("To Rep", df['assigned_salesperson'].dropna().unique())
    if c3.button("Reassign All Leads"):
        df.loc[df['assigned_salesperson'] == from_r, 'assigned_salesperson'] = to_r
        conn.update(worksheet="Sheet1", data=df)
        st.success(f"Reassigned all leads from {from_r} to {to_r}!")
        st.cache_data.clear()
        
    st.markdown("---")
    st.subheader("📋 Master Data Editor (All 20 Columns)")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    if st.button("💾 Save All Master Edits"):
        conn.update(worksheet="Sheet1", data=edited_df)
        st.success("Master Google Sheet updated!")
        st.cache_data.clear()
