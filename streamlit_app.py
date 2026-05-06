import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# ---------------- 1. SERVICE ACCOUNT & DRIVE SETUP ----------------
@st.cache_resource
def get_google_services():
    s = st.secrets["connections"]["gsheets"]
    creds_dict = {
        "type": s["type"], "project_id": s["project_id"], "private_key_id": s["private_key_id"],
        "private_key": s["private_key"].replace("\\n", "\n").strip(),
        "client_email": s["client_email"], "client_id": s["client_id"],
        "auth_uri": s["auth_uri"], "token_uri": s["token_uri"],
        "auth_provider_x509_cert_url": s["auth_provider_x509_cert_url"],
        "client_x509_cert_url": s["client_x509_cert_url"]
    }
    creds = Credentials.from_service_account_info(creds_dict)
    return build('drive', 'v3', credentials=creds)

def get_or_create_user_folder(service, user_id, parent_id):
    query = f"name='{user_id}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    if not items:
        file_metadata = {'name': user_id, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [parent_id]}
        folder = service.files().create(body=file_metadata, fields='id', supportsAllDrives=True).execute()
        return folder.get('id')
    return items[0].get('id')

# ---------------- 2. UI & STYLE CONFIG ----------------
st.set_page_config(page_title="EDIPREX PRO", page_icon="🎬", layout="wide")
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #FF4B4B, #FF8080); color: white; font-weight: bold; height: 3.5em; border: none; }
    .header-text { font-size: 50px; font-weight: 900; color: #FF4B4B; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# ---------------- 3. SYSTEM CONFIG ----------------
try:
    drive_service = get_google_services()
    MAIN_FOLDER_ID = st.secrets["general"]["MAIN_FOLDER_ID"]
except Exception as e:
    st.error(f"System Error: {e}"); st.stop()

# ---------------- 4. AUTH & NAVIGATION ----------------
if "user_id" not in st.session_state:
    st.markdown('<div class="header-text">🎬 EDIPREX PRO</div>', unsafe_allow_html=True)
    tab_log, tab_reg = st.tabs(["🔐 Login", "📝 Register"])
    
    # Login/Register Logic
    with tab_reg:
        conn_log = st.connection("gsheets_logins", type=GSheetsConnection)
        new_id = st.text_input("Choose Unique EDP ID").strip()
        if st.button("Create Account"):
            logins = conn_log.read(spreadsheet="https://docs.google.com/spreadsheets/d/145oVIxTM4SOr299cdMyheSqZfWMbgBTBO1iLkBqX3Ek/edit?gid=0#gid=0", worksheet="Sheet1")
            if new_id in logins["Random_EDP_ID"].astype(str).values:
                st.error("Ye ID pehle se li hui hai!")
            else:
                new_row = pd.DataFrame([{"Random_EDP_ID": new_id}])
                updated_logins = pd.concat([logins, new_row], ignore_index=True)
                conn_log.update(worksheet="Sheet1", data=updated_logins)
                get_or_create_user_folder(drive_service, new_id, MAIN_FOLDER_ID)
                st.success("Registration Done! Ab Login tab mein jao."); st.balloons()

    with tab_log:
        uid = st.text_input("Enter your EDP ID").strip()
        if st.button("Login"):
            logins = conn_log.read(spreadsheet="https://docs.google.com/spreadsheets/d/145oVIxTM4SOr299cdMyheSqZfWMbgBTBO1iLkBqX3Ek/edit?gid=0#gid=0", worksheet="Sheet1")
            if uid in logins["Random_EDP_ID"].astype(str).values:
                st.session_state["user_id"] = uid; st.rerun()
            else: st.error("ID nahi mili.")

# ---------------- 5. MAIN DASHBOARD ----------------
else:
    st.sidebar.title(f"👤 {st.session_state['user_id']}")
    if st.sidebar.button("Logout"): st.session_state.clear(); st.rerun()

    st.header("🚀 New Order Submission")
    st.info("Uploads ka jhanjhat khatam. Details WhatsApp par share karo.")
    
    with st.form("order_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            phone = st.text_input("WhatsApp Number")
        with col2:
            desc = st.text_area("ORDER (Editing Instructions)")
        
        if st.form_submit_button("Submit Order"):
            if phone and desc:
                # Target the Ediprex_Orders sheet specifically
                conn_ord = st.connection("gsheets_orders", type=GSheetsConnection)
                orders = conn_ord.read(spreadsheet="https://docs.google.com/spreadsheets/d/1H7XYe3MFXrh_3VmPUAKcHDZeNYDx07tZH8x9K5VHkwU/edit?gid=0#gid=0", worksheet="Sheet1")
                
                # Maintain exact header columns: Phone, ORDER, User_ID
                new_ord = pd.DataFrame([{
                    "Phone": phone, 
                    "ORDER": desc,
                    "User_ID": st.session_state["user_id"]
                }])
                
                updated_orders = pd.concat([orders, new_ord], ignore_index=True)
                conn_ord.update(worksheet="Sheet1", data=updated_orders)
                st.success("✅ Order Placed successfully!"); st.balloons()
            else:
                st.warning("Saari details fill karo.")

st.markdown("---")
st.caption("© 2026 EDIPREX | Professional Editing Workflow")
