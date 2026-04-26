import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# ---------------- BRAHMASTRA CONNECTIVITY & QUOTA FIX ----------------
def get_google_services():
    # Secrets se credentials uthana
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

# ---------------- PREMIUM UI STYLING ----------------
st.set_page_config(page_title="EDIPREX PRO", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-image: linear-gradient(to right, #FF4B4B, #FF8080);
        color: white;
        height: 3em;
        font-weight: bold;
        border: none;
    }
    .stTextInput>div>div>input { border-radius: 10px; }
    .header-text {
        font-size: 50px;
        font-weight: 800;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-text {
        text-align: center;
        color: #808495;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- INITIALIZE SYSTEM ----------------
try:
    drive_service = get_google_services()
    PARENT_FOLDER_ID = st.secrets["general"]["PARENT_FOLDER_ID"]
except Exception as e:
    st.error(f"⚠️ Connection Error: {e}")
    st.stop()

# ---------------- AUTH SYSTEM ----------------
if "user_id" not in st.session_state:
    st.markdown('<div class="header-text">🎬 EDIPREX</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">High-End Video Editing for Professionals</div>', unsafe_allow_html=True)
    
    tab_log, tab_reg = st.tabs(["🔐 Secure Login", "📝 Register Account"])
    conn = st.connection("gsheets", type=GSheetsConnection)

    with tab_reg:
        new_id = st.text_input("Choose Your Unique EDP ID", placeholder="e.g. nilay_01").strip()
        if st.button("Create My Account"):
            if new_id:
                try:
                    logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
                    if new_id in logins["Random_EDP_ID"].astype(str).values:
                        st.error("This ID is already taken!")
                    else:
                        # Update Sheet
                        new_row = pd.DataFrame([{"Random_EDP_ID": new_id}])
                        conn.update(spreadsheet="Ediprex_Logins", worksheet="Sheet1", data=pd.concat([logins, new_row]))
                        # Create Drive Folder (Supports Quota Fix)
                        drive_service.files().create(body={
                            "name": new_id, 
                            "mimeType": "application/vnd.google-apps.folder", 
                            "parents": [PARENT_FOLDER_ID]
                        }, supportsAllDrives=True).execute()
                        st.success("Registration Successful! Now Login.")
                        st.balloons()
                except Exception as e:
                    st.error(f"Reg Error: {e}")
            else: st.warning("Please enter an ID")

    with tab_log:
        uid = st.text_input("Enter EDP ID", key="login_id").strip()
        if st.button("Unlock Dashboard"):
            logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
            if uid in logins["Random_EDP_ID"].astype(str).values:
                st.session_state["user_id"] = uid
                st.rerun()
            else: st.error("ID not found. Please register.")

# ---------------- DASHBOARD ----------------
else:
    st.sidebar.title(f"👤 {st.session_state['user_id']}")
    st.sidebar.info("EDIPREX Pro Membership Active")
    if st.sidebar.button("🚪 Logout"):
        del st.session_state["user_id"]
        st.rerun()

    st.header("🚀 Start New Project")
    
    with st.container():
        with st.form("order_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                phone = st.text_input("WhatsApp Number (with country code)")
                raw_file = st.file_uploader("Upload Your Footage", type=['mp4', 'mov', 'png', 'jpg', 'zip'])
            with col2:
                desc = st.text_area("Editing Instructions", placeholder="Describe your vision, music, and style...")
            
            submit = st.form_submit_button("🚀 Submit Order & Upload")
            
            if submit:
                if raw_file and phone and desc:
                    try:
                        with st.spinner("Uploading to EDIPREX Cloud..."):
                            # 1. Find User Folder
                            query = f"name='{st.session_state['user_id']}' and mimeType='application/vnd.google-apps.folder' and '{PARENT_FOLDER_ID}' in parents"
                            res = drive_service.files().list(q=query, supportsAllDrives=True).execute()
                            f_id = res['files'][0]['id']
                            
                            # 2. Upload with supportsAllDrives=True (Quota Fix)
                            media = MediaIoBaseUpload(io.BytesIO(raw_file.read()), mimetype=raw_file.type)
                            drive_service.files().create(
                                body={'name': raw_file.name, 'parents': [f_id]},
                                media_body=media,
                                fields='id',
                                supportsAllDrives=True 
                            ).execute()
                        
                        # 3. Log to Sheet
                        conn_orders = st.connection("gsheets", type=GSheetsConnection)
                        orders = conn_orders.read(spreadsheet="Ediprex_Orders", worksheet="Sheet1", ttl=0)
                        new_ord = pd.DataFrame([{"User_Id": st.session_state["user_id"], "Phone": phone, "ORDER": desc}])
                        conn_orders.update(spreadsheet="Ediprex_Orders", worksheet="Sheet1", data=pd.concat([orders, new_ord]))
                        
                        st.success("✅ Order Placed! Our editors will contact you soon.")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please provide WhatsApp number, footage, and instructions.")

    st.markdown("---")
    st.caption("© 2026 EDIPREX | Powered by Nilay's Master Engine")
