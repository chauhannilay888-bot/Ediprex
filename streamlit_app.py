import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Google Drive Service
@st.cache_resource
def get_drive_service():
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    return build('drive', 'v3', credentials=creds)

def folder_exists(service, folder_name, parent_id):
    query = f"name='{folder_name}' and '{parent_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields='files(id)').execute()
    return len(results.get('files', [])) > 0

def create_folder(service, folder_name, parent_id):
    file_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [parent_id]}
    service.files().create(body=file_metadata).execute()

st.set_page_config(page_title="EDIPREX PRO", layout="wide")

# Session State for User
if "user_id" not in st.session_state:
    st.title("🎬 EDIPREX PRO")
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Signup"])
    conn_log = st.connection("gsheets_logins", type=GSheetsConnection)

    with tab2: # Signup
        new_id = st.text_input("Choose Unique ID")
        if st.button("Signup"):
            df = conn_log.read(worksheet="Sheet1")
            if new_id in df["Random_EDP_ID"].values:
                st.error("ID already exists!")
            else:
                # Sheet update
                conn_log.update(worksheet="Sheet1", data=pd.concat([df, pd.DataFrame([{"Random_EDP_ID": new_id}])], ignore_index=True))
                # Drive folder check & create
                service = get_drive_service()
                parent = st.secrets["general"]["MAIN_FOLDER_ID"]
                if not folder_exists(service, new_id, parent):
                    create_folder(service, new_id, parent)
                st.success("Account created and folder ready! Now login.")
                
    with tab1: # Login
        uid = st.text_input("Enter your ID")
        if st.button("Login"):
            df = conn_log.read(worksheet="Sheet1")
            if uid in df["Random_EDP_ID"].values:
                st.session_state["user_id"] = uid
                st.rerun()
            else: st.error("ID not found.")

else: # Dashboard
    st.sidebar.write(f"👤 {st.session_state['user_id']}")
    if st.sidebar.button("Logout"): st.session_state.clear(); st.rerun()

    st.header("🚀 Place Order")
    with st.form("order_form"):
        phone = st.text_input("Phone Number")
        desc = st.text_area("ORDER Description")
        if st.form_submit_button("Submit Order"):
            conn_ord = st.connection("gsheets_orders", type=GSheetsConnection)
            df = conn_ord.read(worksheet="Sheet1")
            new_row = pd.DataFrame([{"Phone": phone, "ORDER": desc, "User_ID": st.session_state["user_id"]}])
            conn_ord.update(worksheet="Sheet1", data=pd.concat([df, new_row], ignore_index=True))
            st.success("✅ Order submitted!")
