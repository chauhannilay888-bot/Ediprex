import streamlit as st
import pandas as pd
import requests
from streamlit_gsheets import GSheetsConnection
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import time

# ---------------- PAGE CONFIG & THEME ----------------
st.set_page_config(
    page_title="EDIPREX - Pro Video & Photo Edits",
    page_icon="🎬",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; background-color: #FF4B4B; color: white; height: 3em; }
    .stTextInput>div>div>input { border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# ---------------- CORE SERVICES ----------------
def get_drive_service():
    creds_info = st.secrets["connections"]["gsheets"]
    creds = Credentials.from_service_account_info(creds_info)
    return build('drive', 'v3', credentials=creds)

drive_service = get_drive_service()
# Main folder link: https://drive.google.com/drive/folders/1cbr28a9N7YcW-r0Lv5i99YJEh1KAYFbr
PARENT_FOLDER_ID = st.secrets["general"]["PARENT_FOLDER_ID"]

# ---------------- AUTH SYSTEM ----------------
if "user_id" not in st.session_state:
    st.title("Welcome to EDIPREX")
    st.caption("A Masterpiece Project by Nilay & Team")
    
    tab_login, tab_reg = st.tabs(["🔐 Login", "📝 Register"])
    conn = st.connection("gsheets", type=GSheetsConnection)

    with tab_reg:
        new_id = st.text_input("Create your EDIPREX ID", placeholder="e.g., nilay123").strip()
        if st.button("Register"):
            if new_id:
                try:
                    # GSheets: https://docs.google.com/spreadsheets/d/145oVIxTM4SOr299cdMyheSqZfWMbgBTBO1iLkBqX3Ek
                    logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
                    if new_id in logins["Random_EDP_ID"].values:
                        st.error("ID already exists! Try a different one.")
                    else:
                        # 1. Update Sheet
                        new_row = pd.DataFrame([{"Random_EDP_ID": new_id}])
                        updated = pd.concat([logins, new_row], ignore_index=True)
                        conn.update(spreadsheet="Ediprex_Logins", worksheet="Sheet1", data=updated)
                        
                        # 2. Create User Folder in Drive
                        drive_service.files().create(
                            body={"name": new_id, "mimeType": "application/vnd.google-apps.folder", "parents": [PARENT_FOLDER_ID]}
                        ).execute()
                        
                        st.success("Registration Successful! Now go to Login tab.")
                        st.balloons()
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter an ID.")

    with tab_login:
        old_id = st.text_input("Enter your EDP ID", key="login_id").strip()
        if st.button("Access Portal"):
            logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
            if old_id in logins["Random_EDP_ID"].values:
                st.session_state["user_id"] = old_id
                st.rerun()
            else:
                st.error("ID not found. Please register first.")

# ---------------- MAIN DASHBOARD ----------------
else:
    st.sidebar.title(f"👤 {st.session_state['user_id']}")
    nav = st.sidebar.radio("Navigation", ["Dashboard & Orders", "My Deliveries", "Samples"])
    
    if st.sidebar.button("Logout"):
        del st.session_state["user_id"]
        st.rerun()

    # SECTION 1: DASHBOARD & ORDERS
    if nav == "Dashboard & Orders":
        st.header("🚀 New Order Request")
        
        with st.form("order_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                country = st.selectbox("Select Country", ["🇮🇳 India (+91)", "🇺🇸 USA (+1)"])
                phone = st.text_input("WhatsApp / Phone Number")
            with col2:
                # RAW Footage upload logic
                raw_file = st.file_uploader("Upload Raw Footage (Max 200MB)", type=['mp4', 'mov', 'avi', 'jpg', 'png'])
            
            desc = st.text_area("Edit Details", placeholder="Example: Cinematic 9:16 reel with color grading and fast cuts.")
            
            if st.form_submit_button("🚀 Submit Order"):
                if phone and desc:
                    with st.spinner("Processing your order..."):
                        # 1. Upload file to User's specific Drive folder
                        if raw_file:
                            results = drive_service.files().list(q=f"name='{st.session_state['user_id']}' and mimeType='application/vnd.google-apps.folder'").execute()
                            user_folder_id = results.get('files', [])[0]['id']
                            
                            file_metadata = {'name': f"RAW_{raw_file.name}", 'parents': [user_folder_id]}
                            media = MediaIoBaseUpload(io.BytesIO(raw_file.read()), mimetype=raw_file.type)
                            drive_service.files().create(body=file_metadata, media_body=media).execute()

                        # 2. Update Orders Sheet: https://docs.google.com/spreadsheets/d/1H7XYe3MFXrh_3VmPUAKcHDZeNYDx07tZH8x9K5VHkwU
                        orders_conn = st.connection("gsheets", type=GSheetsConnection)
                        existing_orders = orders_conn.read(spreadsheet="Ediprex_Orders", worksheet="Sheet1", ttl=0)
                        new_order_data = pd.DataFrame([{
                            "User_Id": st.session_state["user_id"], 
                            "Phone": f"{country.split()[-1]} {phone}", 
                            "ORDER": desc,
                            "Status": "Pending"
                        }])
                        updated_orders = pd.concat([existing_orders, new_order_data], ignore_index=True)
                        orders_conn.update(spreadsheet="Ediprex_Orders", worksheet="Sheet1", data=updated_orders)
                        
                        st.success("Order Placed Successfully! Your edit will be ready in 24-48 hours.")
                        st.balloons()
                else:
                    st.warning("Please fill all required fields.")

    # SECTION 2: MY DELIVERIES
    elif nav == "My Deliveries":
        st.header("📂 Your Edited Products")
        st.info("Files appearing here are processed and ready for download.")
        
        # Search for user folder
        results = drive_service.files().list(q=f"name='{st.session_state['user_id']}' and mimeType='application/vnd.google-apps.folder'").execute()
        if results.get('files'):
            u_folder_id = results['files'][0]['id']
            files = drive_service.files().list(q=f"'{u_folder_id}' in parents and name contains 'EDITED_'").execute().get('files', [])
            
            if files:
                for f in files:
                    st.write(f"✅ {f['name']}")
                    # Note: Display/Download logic can be expanded here
            else:
                st.write("No deliveries yet. We are working on your orders!")

    # SECTION 3: SAMPLES
    elif nav == "Samples":
        st.header("🎬 Our Portfolio")
        st.write("Take a look at what we can do for you.")
        # Logic to display public samples from Ediprex_main

    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 EDIPREX | Powered by Nilay")
