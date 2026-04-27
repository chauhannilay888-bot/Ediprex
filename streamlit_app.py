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

# ---------------- 2. UI STYLING ----------------
st.set_page_config(page_title="EDIPREX PRO", page_icon="🎬", layout="wide")
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(45deg, #FF4B4B, #FF8080);
        color: white;
        font-weight: bold;
        height: 3.5em;
        border: none;
    }
    .header-text { font-size: 55px; font-weight: 900; color: #FF4B4B; text-align: center; margin-bottom: 0px; }
    .sub-text { text-align: center; color: #808495; margin-bottom: 30px; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# ---------------- 3. SYSTEM CONFIG ----------------
try:
    drive_service = get_google_services()
    PARENT_FOLDER_ID = st.secrets["general"]["PARENT_FOLDER_ID"]
    MY_MAIN_EMAIL = "chauhannilay888@gmail.com" # Teri ID fix kar di hai
except Exception as e:
    st.error(f"System Error: {e}"); st.stop()

# ---------------- 4. AUTH & REGISTRATION ----------------
if "user_id" not in st.session_state:
    st.markdown('<div class="header-text">🎬 EDIPREX</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Professional Video Editing Hub</div>', unsafe_allow_html=True)
    
    tab_log, tab_reg = st.tabs(["🔐 Secure Login", "📝 New Registration"])
    conn = st.connection("gsheets", type=GSheetsConnection)

    with tab_reg:
        new_id = st.text_input("Create Your Unique EDP ID").strip()
        if st.button("Register & Create Workspace"):
            if new_id:
                try:
                    logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
                    if new_id in logins["Random_EDP_ID"].astype(str).values:
                        st.error("ID already taken!")
                    else:
                        # 1. Update GSheet
                        new_row = pd.DataFrame([{"Random_EDP_ID": new_id}])
                        conn.update(spreadsheet="Ediprex_Logins", worksheet="Sheet1", data=pd.concat([logins, new_row]))
                        
                        # 2. Create Folder
                        folder_meta = {
                            "name": new_id,
                            "mimeType": "application/vnd.google-apps.folder",
                            "parents": [PARENT_FOLDER_ID]
                        }
                        folder = drive_service.files().create(body=folder_meta, supportsAllDrives=True, fields='id').execute()
                        
                        # 3. TRANSFER OWNERSHIP (The Quota Fix)
                        # Isse folder ki storage teri email account se count hogi
                        new_permission = {
                            'type': 'user',
                            'role': 'owner',
                            'emailAddress': MY_MAIN_EMAIL
                        }
                        drive_service.permissions().create(
                            fileId=folder['id'],
                            body=new_permission,
                            transferOwnership=True,
                            supportsAllDrives=True
                        ).execute()
                        
                        st.success(f"Registered! Folder created and owned by {MY_MAIN_EMAIL}")
                        st.balloons()
                except Exception as e:
                    st.error(f"Registration Failed: {e}")
            else: st.warning("Please enter an ID")

    with tab_log:
        uid = st.text_input("Enter EDP ID").strip()
        if st.button("Login to Dashboard"):
            logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
            if uid in logins["Random_EDP_ID"].astype(str).values:
                st.session_state["user_id"] = uid
                st.rerun()
            else: st.error("ID not found. Please register first.")

# ---------------- 5. MAIN DASHBOARD ----------------
else:
    st.sidebar.title(f"👤 {st.session_state['user_id']}")
    if st.sidebar.button("Logout"):
        del st.session_state["user_id"]
        st.rerun()

    st.header("🚀 Start New Project")
    with st.form("order_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("WhatsApp Number")
            raw_file = st.file_uploader("Upload Footage", type=['mp4', 'mov', 'zip', 'jpg', 'png'])
        with col2:
            desc = st.text_area("Editing Instructions")
            
        if st.form_submit_button("🚀 Submit & Upload"):
            if raw_file and phone and desc:
                try:
                    with st.spinner("Uploading to Secure Cloud..."):
                        # Find User Folder
                        q = f"name='{st.session_state['user_id']}' and mimeType='application/vnd.google-apps.folder' and '{PARENT_FOLDER_ID}' in parents"
                        res = drive_service.files().list(q=q, supportsAllDrives=True).execute()
                        f_id = res['files'][0]['id']
                        
                        # Upload File
                        media = MediaIoBaseUpload(io.BytesIO(raw_file.read()), mimetype=raw_file.type, resumable=True)
                        drive_service.files().create(
                            body={'name': raw_file.name, 'parents': [f_id]},
                            media_body=media,
                            fields='id',
                            supportsAllDrives=True
                        ).execute()
                    
                    # Log to GSheet
                    conn_ord = st.connection("gsheets", type=GSheetsConnection)
                    orders = conn_ord.read(spreadsheet="Ediprex_Orders", worksheet="Sheet1", ttl=0)
                    new_ord = pd.DataFrame([{"User_Id": st.session_state["user_id"], "Phone": phone, "ORDER": desc}])
                    conn_ord.update(spreadsheet="Ediprex_Orders", worksheet="Sheet1", data=pd.concat([orders, new_ord]))
                    
                    st.success("✅ Order Placed Successfully!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Quota/Upload Error: {e}")
            else:
                st.warning("Please provide all details.")

    st.markdown("---")
    st.caption("© 2026 EDIPREX | Studio Management System")
