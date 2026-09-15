<!-- ... existing code ... -->
# ---------------------------------------------------------
# BRAND STYLING & OVAL LOGO CONTAINER (SIDHARTH BRAND PALETTE)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Global Background & Typography */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Left Panel Oval Logo Container Styling */
    .sidebar-oval-logo {
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        border: 2px solid #164194;
        border-radius: 60px / 35px;
        padding: 14px;
        box-shadow: 0 8px 20px rgba(22, 65, 148, 0.25);
        text-align: center;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .sidebar-oval-logo:hover {
        transform: scale(1.02);
    }
    
    .sidebar-oval-logo img {
        max-width: 90%;
        border-radius: 30px;
    }

    /* Main Page Title Banner */
    .main-header {
        font-size: 28px;
        font-weight: 800;
        color: #164194;
        margin-bottom: 12px;
        border-bottom: 4px solid #00A859;
        padding-bottom: 10px;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Top Right Header Logo Container */
    .top-right-logo {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding-bottom: 10px;
    }
    
    /* Form Labels & Section Headers in Brand Blue Color */
    label, div[data-testid="stMarkdownContainer"] p strong, .stWidgetLabel label p {
        color: #164194 !important;
        font-weight: 700 !important;
    }

    /* Form Input Fields Styling */
    .stTextInput > label, .stSelectbox > label, .stNumberInput > label, .stTextArea > label, .stDateInput > label {
        color: #164194 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stNumberInput input, .stTextArea textarea {
        border-radius: 8px !important;
        border: 1.5px solid #cbd5e1 !important;
        transition: all 0.2s ease-in-out !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #00A859 !important;
        box-shadow: 0 0 0 3px rgba(0, 168, 89, 0.15) !important;
    }

    /* KPI Glassmorphism Cards */
    .kpi-card {
        background: #ffffff;
        padding: 22px 18px;
        border-radius: 14px;
        border-left: 6px solid #164194;
        border-right: 1px solid #e2e8f0;
        border-top: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px -5px rgba(22, 65, 148, 0.08);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 30px -5px rgba(22, 65, 148, 0.15);
    }
    
    .kpi-card-green {
        border-left: 6px solid #00A859;
    }

    .kpi-card h5 {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }
    
    .kpi-card h2 {
        color: #164194;
        font-size: 30px;
        font-weight: 800;
        margin: 0;
    }

    /* Primary Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #164194 0%, #0e2d6b 100%) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 12px rgba(22, 65, 148, 0.25) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #00A859 0%, #008244 100%) !important;
        box-shadow: 0 6px 18px rgba(0, 168, 89, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Subheaders and Titles */
    h3, h4, h5 {
        color: #164194 !important;
        font-weight: 700 !important;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #ffffff;
        border-radius: 8px 8px 0 0;
        padding: 0 20px;
        border: 1px solid #e2e8f0;
        border-bottom: none;
        color: #64748b;
        font-weight: 600;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #164194 !important;
        background-color: #ffffff !important;
        border-bottom: 3px solid #00A859 !important;
        font-weight: 800 !important;
    }
    
    /* Expanders Styling */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        color: #164194 !important;
        font-weight: 700 !important;
        border: 1px solid #e2e8f0 !important;
    }
    </style>
""", unsafe_allow_html=True)
<!-- ... existing code ... -->
```

### Summary of Enhancements Made:
1. **Brand Palette Cohesion**: Enhanced the primary Navy (`#164194`) and Green accent (`#00A859`) across all forms, fields, tabs, hover states, and primary submit buttons.
2. **Elevated UI Cards (KPIs)**: Added micro-interactions with hover translate effects, box shadows, and updated spacing.
3. **Improved Form Fields**: Styled input labels with uppercase tracking and highlighted input active/focused borders with brand green accents.
4. **Interactive Tab Bar**: Clean tab pill design with border highlights to make active tabs easily distinguishable.
