import streamlit as st
import pandas as pd
import io
from streamlit_gsheets import GSheetsConnection
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# ---------------- 1. SERVICE ACCOUNT SETUP ----------------
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

# ---------------- 2. UI STYLING ----------------
st.set_page_config(page_title="EDIPREX PRO", page_icon="🎬", layout="wide")
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #FF4B4B, #FF8080); color: white; font-weight: bold; height: 3.5em; border: none; }
    .header-text { font-size: 55px; font-weight: 900; color: #FF4B4B; text-align: center; }
    .sub-text { text-align: center; color: #808495; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

try:
    drive_service = get_google_services()
    PARENT_FOLDER_ID = st.secrets["general"]["PARENT_FOLDER_ID"]
except Exception as e:
    st.error(f"System Error: {e}"); st.stop()

# ---------------- 3. AUTH & REGISTRATION ----------------
if "user_id" not in st.session_state:
    st.markdown('<div class="header-text">🎬 EDIPREX</div>', unsafe_allow_html=True)
    tab_log, tab_reg = st.tabs(["🔐 Login", "📝 Register"])
    conn = st.connection("gsheets", type=GSheetsConnection)

    with tab_reg:
        new_id = st.text_input("Choose Unique EDP ID").strip()
        if st.button("Register"):
            if new_id:
                try:
                    logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
                    if new_id in logins["Random_EDP_ID"].astype(str).values:
                        st.error("ID already taken!")
                    else:
                        conn.update(spreadsheet="Ediprex_Logins", worksheet="Sheet1", data=pd.concat([logins, pd.DataFrame([{"Random_EDP_ID": new_id}])]))
                        # Create Folder normally (Inheritance is the key)
                        folder_meta = {"name": new_id, "mimeType": "application/vnd.google-apps.folder", "parents": [PARENT_FOLDER_ID]}
                        drive_service.files().create(body=folder_meta, supportsAllDrives=True).execute()
                        st.success("Registration Successful!")
                        st.balloons()
                except Exception as e: st.error(f"Reg Error: {e}")

    with tab_log:
        uid = st.text_input("Enter EDP ID").strip()
        if st.button("Login"):
            logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
            if uid in logins["Random_EDP_ID"].astype(str).values:
                st.session_state["user_id"] = uid
                st.rerun()
            else: st.error("ID not found.")

# ---------------- 4. DASHBOARD & UPLOAD ----------------
else:
    st.sidebar.title(f"👤 {st.session_state['user_id']}")
    if st.sidebar.button("Logout"): del st.session_state["user_id"]; st.rerun()

    with st.form("order_form", clear_on_submit=True):
        phone = st.text_input("WhatsApp Number")
        raw_file = st.file_uploader("Upload Footage", type=['mp4', 'mov', 'zip', 'jpg', 'png'])
        desc = st.text_area("Instructions")
        if st.form_submit_button("Submit"):
            if raw_file and phone and desc:
                try:
                    with st.spinner("Uploading..."):
                        q = f"name='{st.session_state['user_id']}' and mimeType='application/vnd.google-apps.folder' and '{PARENT_FOLDER_ID}' in parents"
                        res = drive_service.files().list(q=q, supportsAllDrives=True).execute()
                        f_id = res['files'][0]['id']
                        
                        media = MediaIoBaseUpload(io.BytesIO(raw_file.read()), mimetype=raw_file.type, resumable=True)
                        # CRITICAL: We create the file inside the folder that you already own (the parent)
                        # This forces the quota to be checked against the folder hierarchy you set up.
                        drive_service.files().create(
                            body={'name': raw_file.name, 'parents': [f_id]},
                            media_body=media,
                            fields='id',
                            supportsAllDrives=True
                        ).execute()
                    
                    conn_ord = st.connection("gsheets", type=GSheetsConnection)
                    orders = conn_ord.read(spreadsheet="Ediprex_Orders", worksheet="Sheet1", ttl=0)
                    conn_ord.update(spreadsheet="Ediprex_Orders", worksheet="Sheet1", data=pd.concat([orders, pd.DataFrame([{"User_Id": st.session_state["user_id"], "Phone": phone, "ORDER": desc}])]))
                    st.success("✅ Order Placed!")
                    st.balloons()
                except Exception as e: st.error(f"Error: {e}")
                    
