import streamlit as st
import pandas as pd
import os
import io
from streamlit_gsheets import GSheetsConnection
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ediprex - Professional Video & Photo Edits",
    page_icon="sZ6eW.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- PREMIUM UI STYLING ----------------
st.markdown("""
<style>
    .hero {
        background: linear-gradient(135deg, #0f172a, #1e2937);
        padding: 70px 20px;
        text-align: center;
        border-radius: 20px;
        margin-bottom: 30px;
    }
    .main-title {
        font-size: clamp(2.8rem, 8vw, 5rem);
        font-weight: 900;
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        font-size: 1.35rem;
        color: #cbd5e1;
        max-width: 720px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1 class="main-title">EDIPREX</h1>
    <p class="subtitle">Professional Video & Photo Edits — Fast, Creative & Delivered in 24-48 Hours</p>
</div>
""", unsafe_allow_html=True)

# ---------------- GOOGLE DRIVE SERVICE ----------------
def get_drive_service():
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

try:
    drive_service = get_drive_service()
    PARENT_FOLDER_ID = st.secrets["general"]["PARENT_FOLDER_ID"]
except Exception as e:
    st.error(f"⚠️ Connection Error: {e}")
    st.stop()

# ---------------- MAIN APP ----------------
st.header("🚀 Start New Project")

with st.form("order_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        phone = st.text_input("WhatsApp Number (with country code)", placeholder="+91 9876543210")
        raw_file = st.file_uploader("Upload Your Raw Footage", 
                                    type=['mp4', 'mov', 'avi', 'mkv', 'png', 'jpg', 'zip'])
    
    with col2:
        desc = st.text_area("Editing Instructions", 
                            placeholder="Describe your vision: cuts, music, text overlays, style, duration etc...",
                            height=180)

    submit = st.form_submit_button("🚀 Submit Order & Upload", use_container_width=True)

    if submit:
        if raw_file and phone and desc:
            try:
                with st.spinner("Uploading to EDIPREX Cloud..."):
                    # Find user's folder
                    query = f"name='{st.session_state.get('user_id', 'guest')}' and mimeType='application/vnd.google-apps.folder' and '{PARENT_FOLDER_ID}' in parents"
                    res = drive_service.files().list(q=query, supportsAllDrives=True).execute()
                    
                    if not res.get('files'):
                        st.error("User folder not found. Please contact support.")
                    else:
                        folder_id = res['files'][0]['id']
                        
                        # Upload file
                        file_metadata = {
                            'name': raw_file.name,
                            'parents': [folder_id]
                        }
                        media = MediaIoBaseUpload(io.BytesIO(raw_file.getvalue()), 
                                                  mimetype=raw_file.type, 
                                                  resumable=True)
                        
                        drive_service.files().create(
                            body=file_metadata,
                            media_body=media,
                            fields='id',
                            supportsAllDrives=True
                        ).execute()

                # Log order to GSheets
                conn = st.connection("gsheets", type=GSheetsConnection)
                orders = conn.read(spreadsheet="Ediprex_Orders", worksheet="Sheet1", ttl=0)
                new_ord = pd.DataFrame([{
                    "User_Id": st.session_state.get("user_id", "guest"),
                    "Phone": phone,
                    "ORDER": desc
                }])
                conn.update(spreadsheet="Ediprex_Orders", worksheet="Sheet1", data=pd.concat([orders, new_ord]))

                st.success("✅ Order Placed Successfully! Our editors will start shortly.")
                st.balloons()

            except Exception as e:
                st.error(f"Upload Error: {e}")
        else:
            st.warning("Please fill all fields and upload a file.")

st.caption("© 2026 EDIPREX | Professional Studio Workflow")
