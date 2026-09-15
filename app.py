import pandas as pd
import streamlit as st
from datetime import datetime

def handle_lead_submission(lead_data, conn):
    # 1. Append lead to 'Leads Data' Sheet
    df_leads = conn.read(worksheet="Leads Data")
    df_updated_leads = pd.concat([df_leads, pd.DataFrame([lead_data])], ignore_index=True)
    conn.update(worksheet="Leads Data", data=df_updated_leads)
    
    # 2. Check Trigger: If Quotation Status is "Sent", auto-populate 'Quotation Sheet'
    if lead_data.get("Quotation Status") == "Sent":
        quote_entry = {
            "Client ID": lead_data.get("Client ID"),
            "Date Stamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Client Name": lead_data.get("Client Name"),
            "Company Name": lead_data.get("Company Name"),
            "Customer Contact Number": lead_data.get("Number"),
            "Product ": lead_data.get("Product "),
            "Quantity": lead_data.get("Qty"),
            "City": lead_data.get("City"),
            "Source": lead_data.get("Source"),
            "Assigned Salesperson": lead_data.get("Assigned Salesperson"),
            "Quotation": "Sent",
            "Quotation Status": "Sent",
            "Quotation Shared By": lead_data.get("Quotation Sent By")
        }
        
        # Read existing Quotation Sheet & Append auto-populated row
        df_quotes = conn.read(worksheet="Quotation Sheet")
        df_updated_quotes = pd.concat([df_quotes, pd.DataFrame([quote_entry])], ignore_index=True)
        conn.update(worksheet="Quotation Sheet", data=df_updated_quotes)
        
        st.info("🔄 Lead saved and common data auto-transferred to Quotation Sheet!")
    else:
        st.success("✅ Lead saved successfully!")
