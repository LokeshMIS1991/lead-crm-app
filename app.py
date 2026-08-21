import streamlit as st
import pandas as pd

# Page Configuration (Wide view, Custom Title)
st.set_page_config(
    page_title="Pro CRM - Modern Lead Workspace",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Odoo/Zoho Look & Feel
st.markdown("""
    <style>
    /* Main Background & Clean Font */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Custom Navigation Styling */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        color: white;
    }
    
    /* Modern Card Container */
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-card h4 {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card h2 {
        color: #0f172a;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }
    
    /* Action Buttons Styling */
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    </style>
""", unsafe_allow_html=True)

# Dummy Data for Dashboard Preview (Phase-1)
data = {
    "Lead Name": ["Aarav Sharma", "Rohan Mehta", "Priya Verma", "Neha Gupta"],
    "Company": ["TechCorp", "Designify", "GrowthMedia", "InnoLab"],
    "Source": ["Website", "LinkedIn", "Referral", "Call"],
    "Stage": ["New Lead", "Contacted", "Proposal Sent", "Closed Won"],
    "Value (₹)": [50000, 120000, 85000, 200000]
}
df = pd.DataFrame(data)

# Sidebar Navigation (Odoo/Zoho Style)
with st.sidebar:
    st.markdown("<h2 style='color: white; text-align: center;'>⚡ Pro CRM</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio(
        "NAVIGATION",
        ["📊 Dashboard", "🎯 Kanban Board", "📋 All Leads", "➕ Add New Lead", "⚙️ Settings"]
    )

# Page 1: Dashboard View
if menu == "📊 Dashboard":
    st.title("🎯 Lead Overview")
    st.caption("Welcome back! Here is what's happening with your sales pipeline today.")
    st.markdown("<br>", unsafe_allow_html=True)

    # Key Metrics Cards Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-card"><h4>Total Leads</h4><h2>4</h2></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><h4>Active Deals</h4><h2>3</h2></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><h4>Pipeline Value</h4><h2>₹4.55L</h2></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><h4>Win Rate</h4><h2>25%</h2></div>', unsafe_allow_html=True)

    st.markdown("<br><hr>", unsafe_allow_html=True)

    # Recent Activity / Quick Data Table
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("🔥 High Priority Leads")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    with col_right:
        st.subheader("⚡ Quick Actions")
        st.button("➕ Create Quick Lead", use_container_width=True)
        st.button("📥 Import Data", use_container_width=True)
        st.button("📊 Export Reports", use_container_width=True)