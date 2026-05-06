import streamlit as st
import pandas as pd
import io
import phonenumbers
from streamlit_gsheets import GSheetsConnection
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# ---------------- 1. SERVICE ACCOUNT SETUP ----------------
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

# ---------------- 2. UI & DRIVE HELPERS ----------------
st.set_page_config(page_title="EDIPREX PRO", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #FF4B4B, #FF8080); color: white; font-weight: bold; height: 3.5em; border: none; }
    .header-text { font-size: 50px; font-weight: 900; color: #FF4B4B; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

def get_country_codes():
    codes = []
    for region in phonenumbers.SUPPORTED_REGIONS:
        country_code = phonenumbers.country_code_for_region(region)
        codes.append(f"+{country_code} ({region})")
    return sorted(list(set(codes)))

def get_unique_filename(drive_service, folder_id, filename):
    query = f"name = '{filename}' and '{folder_id}' in parents and trashed = false"
    results = drive_service.files().list(q=query, fields="files(name)", spaces='drive').execute()
    existing_files = [f['name'] for f in results.get('files', [])]
    if filename not in existing_files: return filename
    base_name, extension = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    counter = 1
    while True:
        new_name = f"{base_name}({counter}).{extension}" if extension else f"{base_name}({counter})"
        if new_name not in existing_files: return new_name
        counter += 1

def get_or_create_user_folder(service, user_id, parent_id):
    query = f"name='{user_id}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    if not items:
        file_metadata = {'name': user_id, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [parent_id]}
        folder = service.files().create(body=file_metadata, fields='id', supportsAllDrives=True).execute()
        return folder.get('id')
    return items[0].get('id')

def get_files_from_folder(service, folder_id):
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name, webViewLink)').execute()
    return results.get('files', [])

# ---------------- 3. SYSTEM CONFIG ----------------
try:
    drive_service = get_google_services()
    MAIN_FOLDER_ID = st.secrets["general"]["MAIN_FOLDER_ID"]
    TEMPLATE_FOLDER_ID = st.secrets["general"]["TEMPLATE_FOLDER_ID"]
except Exception as e:
    st.error(f"System Error: {e}"); st.stop()

# ---------------- 4. AUTH & NAVIGATION ----------------
if "user_id" not in st.session_state:
    st.markdown('<div class="header-text">🎬 EDIPREX PRO</div>', unsafe_allow_html=True)
    tab_log, tab_reg = st.tabs(["🔐 Login", "📝 Register"])
    conn = st.connection("gsheets", type=GSheetsConnection)

    with tab_reg:
        new_id = st.text_input("Choose Unique EDP ID").strip()
        if st.button("Create Account"):
            if new_id:
                logins = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/145oVIxTM4SOr299cdMyheSqZfWMbgBTBO1iLkBqX3Ek/edit?gid=0#gid=0", worksheet="Sheet1", ttl=0)
                if new_id in logins["Random_EDP_ID"].astype(str).values:
                    st.error("Bhai, ye ID pehle se li hui hai!")
                else:
                    new_row = pd.DataFrame([{"Random_EDP_ID": new_id}])
                    conn.update(worksheet="Sheet1", data=pd.concat([logins, new_row]))
                    with st.spinner("Setting up your workspace..."):
                        get_or_create_user_folder(drive_service, new_id, MAIN_FOLDER_ID)
                    st.success("Registration Done! Ab Login tab mein jao.")
                    st.balloons()

    with tab_log:
        uid = st.text_input("Enter your EDP ID").strip()
        if st.button("Login to Dashboard"):
            logins = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/145oVIxTM4SOr299cdMyheSqZfWMbgBTBO1iLkBqX3Ek/edit?gid=0#gid=0", worksheet="Sheet1", ttl=0)
            if uid in logins["Random_EDP_ID"].astype(str).values:
                st.session_state["user_id"] = uid
                st.rerun()
            else: st.error("ID nahi mili. Register karlo pehle.")

# ---------------- 5. MAIN DASHBOARD ----------------
else:
    st.sidebar.title(f"👤 {st.session_state['user_id']}")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📦 My Orders (Edits)")
    
    user_folder_id = get_or_create_user_folder(drive_service, st.session_state["user_id"], MAIN_FOLDER_ID)
    user_files = get_files_from_folder(drive_service, user_folder_id)
    
    if user_files:
        for f in user_files:
            st.sidebar.markdown(f"🔗 [{f['name']}]({f['webViewLink']})")
    else:
        st.sidebar.info("Abhi tak koi final edit upload nahi hua hai.")
        
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"): 
        st.session_state.clear()
        st.rerun()

    st.header("🚀 New Order & Upload")
    with st.form("order_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            country_list = get_country_codes()
            default_ix = country_list.index("+91 (IN)") if "+91 (IN)" in country_list else 0
            c_code = st.selectbox("Select Country Code", options=country_list, index=default_ix)
            phone = st.text_input("WhatsApp Number")
            raw_file = st.file_uploader("Choose Video/Photo", type=['mp4', 'mov', 'zip', 'jpg', 'png'])
        with col2:
            desc = st.text_area("Editing Instructions", height=180)
            
        if st.form_submit_button("Submit & Start Upload"):
            if raw_file and phone and desc:
                try:
                    full_phone = f"{c_code.split(' ')[0]} {phone}"
                    with st.spinner("Uploading to EDIPREX Cloud..."):
                        final_name = get_unique_filename(drive_service, TEMPLATE_FOLDER_ID, f"{st.session_state['user_id']}_{raw_file.name}")
                        media = MediaIoBaseUpload(io.BytesIO(raw_file.read()), mimetype=raw_file.type, resumable=True)
                        drive_service.files().create(
                            body={'name': final_name, 'parents': [TEMPLATE_FOLDER_ID]},
                            media_body=media, fields='id', supportsAllDrives=True
                        ).execute()
                    
                    conn_ord = st.connection("gsheets", type=GSheetsConnection)
                    orders = conn_ord.read(spreadsheet="https://docs.google.com/spreadsheets/d/1H7XYe3MFXrh_3VmPUAKcHDZeNYDx07tZH8x9K5VHkwU/edit?gid=0#gid=0", worksheet="Sheet1", ttl=0)
                    new_ord = pd.DataFrame([{"User_ID": st.session_state["user_id"], "Phone": full_phone, "ORDER_DESCRIPTION": f"File: {final_name} | {desc}"}])
                    conn_ord.update(worksheet="Sheet1", data=pd.concat([orders, new_ord]))
                    st.success(f"✅ Order Placed! File saved as: {final_name}")
                    st.balloons()
                except Exception as e:
                    st.error(f"Panga ho gaya: {e}")
            else:
                st.warning("Bhai, saari details fill kar.")

st.markdown("---")
st.caption("© 2026 EDIPREX | Professional Editing Workflow")
