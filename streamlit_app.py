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
st.markdown("""<style>.stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #FF4B4B, #FF8080); color: white; font-weight: bold; height: 3.5em; border: none; }</style>""", unsafe_allow_html=True)

try:
    drive_service = get_google_services()
    PARENT_FOLDER_ID = st.secrets["general"]["PARENT_FOLDER_ID"]
except Exception as e:
    st.error(f"System Error: {e}"); st.stop()

# ---------------- 3. AUTH & REGISTRATION ----------------
if "user_id" not in st.session_state:
    st.title("🎬 EDIPREX PRO")
    tab_log, tab_reg = st.tabs(["🔐 Login", "📝 Register"])
    conn = st.connection("gsheets", type=GSheetsConnection)

    with tab_reg:
        new_id = st.text_input("Choose Unique EDP ID").strip()
        if st.button("Register"):
            if new_id:
                try:
                    logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
                    if new_id in logins["Random_EDP_ID"].astype(str).values:
                        st.error("ID taken!")
                    else:
                        conn.update(spreadsheet="Ediprex_Logins", worksheet="Sheet1", data=pd.concat([logins, pd.DataFrame([{"Random_EDP_ID": new_id}])]))
                        
                        # FOLDER CREATION
                        folder_meta = {"name": new_id, "mimeType": "application/vnd.google-apps.folder", "parents": [PARENT_FOLDER_ID]}
                        # supportsAllDrives true rakhna zaroori hai
                        drive_service.files().create(body=folder_meta, supportsAllDrives=True).execute()
                        st.success("Registered! Ab login karo.")
                except Exception as e: st.error(f"Reg Error: {e}")

    with tab_log:
        uid = st.text_input("Enter EDP ID").strip()
        if st.button("Login"):
            logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
            if uid in logins["Random_EDP_ID"].astype(str).values:
                st.session_state["user_id"] = uid
                st.rerun()
            else: st.error("ID not found.")

# ---------------- 4. DASHBOARD & UPLOAD FIX ----------------
else:
    st.sidebar.title(f"👤 {st.session_state['user_id']}")
    if st.sidebar.button("Logout"): del st.session_state["user_id"]; st.rerun()

    with st.form("order_form", clear_on_submit=True):
        st.header("🚀 Start Project")
        phone = st.text_input("WhatsApp")
        raw_file = st.file_uploader("Upload Footage", type=['mp4', 'mov', 'zip', 'jpg', 'png'])
        desc = st.text_area("Instructions")
        
        if st.form_submit_button("Submit Order"):
            if raw_file and phone and desc:
                try:
                    with st.spinner("Uploading..."):
                        # FIND USER FOLDER
                        q = f"name='{st.session_state['user_id']}' and mimeType='application/vnd.google-apps.folder' and '{PARENT_FOLDER_ID}' in parents"
                        res = drive_service.files().list(q=q, supportsAllDrives=True).execute()
                        f_id = res['files'][0]['id']
                        
                        # THE QUOTA BYPASS UPLOAD
                        # Hum file metadata mein specific ownership nahi mangenge
                        file_metadata = {'name': raw_file.name, 'parents': [f_id]}
                        media = MediaIoBaseUpload(io.BytesIO(raw_file.read()), mimetype=raw_file.type, resumable=True)
                        
                        # YAHAN HAI FIX: supportsAllDrives=True ke sath fields='id'
                        drive_service.files().create(
                            body=file_metadata,
                            media_body=media,
                            fields='id',
                            supportsAllDrives=True,
                            supportsTeamDrives=True # Dono true rakho force karne ke liye
                        ).execute()
                    
                    # LOG ORDER
                    conn_ord = st.connection("gsheets", type=GSheetsConnection)
                    orders = conn_ord.read(spreadsheet="Ediprex_Orders", worksheet="Sheet1", ttl=0)
                    new_ord = pd.DataFrame([{"User_Id": st.session_state["user_id"], "Phone": phone, "ORDER": desc}])
                    conn_ord.update(spreadsheet="Ediprex_Orders", worksheet="Sheet1", data=pd.concat([orders, new_ord]))
                    st.success("✅ Done!")
                except Exception as e:
                    # Agar abhi bhi error aaye, toh error msg print karo details ke sath
                    st.error(f"Quota Error Detail: {e}")
