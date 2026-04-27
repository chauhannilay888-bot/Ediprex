import streamlit as st
import pandas as pd
import io
import re
from streamlit_gsheets import GSheetsConnection
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# ---------------- SERVICE ACCOUNT CLEANER ----------------
def get_google_services():
    s = st.secrets["connections"]["gsheets"]
    creds_dict = {
        "type": s["type"],
        "project_id": s["project_id"],
        "private_key_id": s["private_key_id"],
        "private_key": s["private_key"].replace("\\n", "\n").strip(),
        "client_email": s["client_email"],
        "client_id": s["client_id"],
        "auth_uri": s["auth_uri"],
        "token_uri": s["token_uri"],
        "auth_provider_x509_cert_url": s["auth_provider_x509_cert_url"],
        "client_x509_cert_url": s["client_x509_cert_url"]
    }
    creds = Credentials.from_service_account_info(creds_dict)
    return build('drive', 'v3', credentials=creds)

# ---------------- UI STYLING ----------------
st.set_page_config(page_title="EDIPREX PRO", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(45deg, #FF4B4B, #FF8080);
        color: white;
        font-weight: bold;
        height: 3.5em;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(255,75,75,0.3); }
    .header-text { font-size: 50px; font-weight: 900; color: #FF4B4B; text-align: center; margin-bottom: 0px; }
    .sub-text { text-align: center; color: #808495; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# ---------------- INITIALIZATION ----------------
try:
    drive_service = get_google_services()
    PARENT_FOLDER_ID = st.secrets["general"]["PARENT_FOLDER_ID"]
except Exception as e:
    st.error(f"System Error: {e}")
    st.stop()

# ---------------- AUTH & REGISTRATION ----------------
if "user_id" not in st.session_state:
    st.markdown('<div class="header-text">🎬 EDIPREX</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Premium Video Editing Workflow</div>', unsafe_allow_html=True)
    
    tab_log, tab_reg = st.tabs(["🔐 Login", "📝 Register"])
    conn = st.connection("gsheets", type=GSheetsConnection)

    with tab_reg:
        new_id = st.text_input("Create EDP ID (e.g. nilay_pro)").strip()
        if st.button("Create Account"):
            if new_id:
                try:
                    logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
                    if new_id in logins["Random_EDP_ID"].astype(str).values:
                        st.error("ID already taken!")
                    else:
                        # 1. Update GSheet
                        new_row = pd.DataFrame([{"Random_EDP_ID": new_id}])
                        conn.update(spreadsheet="Ediprex_Logins", worksheet="Sheet1", data=pd.concat([logins, new_row]))
                        
                        # 2. Create Drive Folder (Owner will be Service Account, but inherits Parent Permissions)
                        folder_meta = {
                            "name": new_id,
                            "mimeType": "application/vnd.google-apps.folder",
                            "parents": [PARENT_FOLDER_ID]
                        }
                        drive_service.files().create(body=folder_meta, supportsAllDrives=True).execute()
                        
                        st.success("Registration Successful! Now go to Login tab.")
                        st.balloons()
                except Exception as e:
                    st.error(f"Reg Error: {e}")
            else: st.warning("Enter an ID")

    with tab_log:
        uid = st.text_input("Enter EDP ID").strip()
        if st.button("Access Dashboard"):
            logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
            if uid in logins["Random_EDP_ID"].astype(str).values:
                st.session_state["user_id"] = uid
                st.rerun()
            else: st.error("ID not found.")

# ---------------- MAIN DASHBOARD ----------------
else:
    st.sidebar.title(f"👤 {st.session_state['user_id']}")
    if st.sidebar.button("Logout"):
        del st.session_state["user_id"]
        st.rerun()

    st.header("🚀 Place New Order")
    
    with st.form("order_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("WhatsApp Number (with country code)")
            raw_file = st.file_uploader("Upload Raw Footage", type=['mp4', 'mov', 'zip', 'jpg', 'png'])
        with col2:
            desc = st.text_area("Edit Description & Style Instructions")
            
        if st.form_submit_button("Submit Order"):
            if raw_file and phone and desc:
                try:
                    with st.spinner("Uploading to EDIPREX Cloud..."):
                        # 1. Find User Folder
                        q = f"name='{st.session_state['user_id']}' and mimeType='application/vnd.google-apps.folder' and '{PARENT_FOLDER_ID}' in parents"
                        res = drive_service.files().list(q=q, supportsAllDrives=True).execute()
                        if not res['files']:
                            st.error("Folder error. Contact support.")
                            st.stop()
                        f_id = res['files'][0]['id']
                        
                        # 2. Upload with supportsAllDrives=True
                        # Note: By disabling 'Editors can change permissions' in Drive UI, 
                        # this file ownership will default to the Main Account quota.
                        media = MediaIoBaseUpload(io.BytesIO(raw_file.read()), mimetype=raw_file.type, resumable=True)
                        drive_service.files().create(
                            body={'name': raw_file.name, 'parents': [f_id]},
                            media_body=media,
                            fields='id',
                            supportsAllDrives=True
                        ).execute()
                    
                    # 3. Log to Orders Sheet
                    conn_ord = st.connection("gsheets", type=GSheetsConnection)
                    orders = conn_ord.read(spreadsheet="Ediprex_Orders", worksheet="Sheet1", ttl=0)
                    new_ord = pd.DataFrame([{"User_Id": st.session_state["user_id"], "Phone": phone, "ORDER": desc}])
                    conn_ord.update(spreadsheet="Ediprex_Orders", worksheet="Sheet1", data=pd.concat([orders, new_ord]))
                    
                    st.success("✅ Order Submitted! We'll reach out on WhatsApp.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Quota/Upload Error: {e}")
                    st.info("Check if your Main Drive storage is full or Service Account is an Editor.")
            else:
                st.warning("Please fill all details and upload a file.")

    st.markdown("---")
    st.caption("© 2026 EDIPREX | Studio Management System")
