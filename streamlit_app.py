import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# ---------------- BRAHMASTRA SERVICE ACCOUNT CLEANER ----------------
def get_google_services():
    # Secrets se credentials uthana
    creds_info = dict(st.secrets["connections"]["gsheets"])
    
    # PEM Error Fix: \n aur hidden slashes ko force-clean karna
    raw_key = creds_info["private_key"]
    clean_key = raw_key.replace("\\n", "\n").replace("\\\\n", "\n").strip()
    creds_info["private_key"] = clean_key
    
    creds = Credentials.from_service_account_info(creds_info)
    
    # Drive aur Sheets dono ke liye service return karna
    drive = build('drive', 'v3', credentials=creds)
    return drive

# ---------------- PAGE CONFIG & UI ----------------
st.set_page_config(
    page_title="EDIPREX - Professional Edits",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; background-color: #FF4B4B; color: white; height: 3em; font-weight: bold; }
    .stTextInput>div>div>input { border-radius: 8px; }
    .main-header { font-size: 45px; font-weight: 800; color: #FF4B4B; text-align: center; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Services
try:
    drive_service = get_google_services()
    PARENT_FOLDER_ID = st.secrets["general"]["PARENT_FOLDER_ID"]
except Exception as e:
    st.error(f"⚠️ System Connection Error: {e}")
    st.stop()

# ---------------- AUTH SYSTEM ----------------
if "user_id" not in st.session_state:
    st.markdown('<div class="main-header">🎬 EDIPREX</div>', unsafe_allow_html=True)
    st.caption("<center>Your Vision, Our Masterpiece</center>", unsafe_allow_html=True)
    
    tab_login, tab_reg = st.tabs(["🔐 Login Portal", "📝 New Registration"])
    conn = st.connection("gsheets", type=GSheetsConnection)

    with tab_reg:
        new_id = st.text_input("Create a Unique EDP ID", placeholder="e.g., nilay_edits").strip()
        if st.button("Register Now"):
            if new_id:
                try:
                    logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
                    if new_id in logins["Random_EDP_ID"].astype(str).values:
                        st.error("This ID is already taken. Try another!")
                    else:
                        # 1. Update GSheet
                        new_row = pd.DataFrame([{"Random_EDP_ID": new_id}])
                        updated = pd.concat([logins, new_row], ignore_index=True)
                        conn.update(spreadsheet="Ediprex_Logins", worksheet="Sheet1", data=updated)
                        
                        # 2. Create Personal Folder in Drive
                        folder_metadata = {
                            'name': new_id,
                            'mimeType': 'application/vnd.google-apps.folder',
                            'parents': [PARENT_FOLDER_ID]
                        }
                        drive_service.files().create(body=folder_metadata).execute()
                        
                        st.success(f"Successfully Registered! Your ID: {new_id}")
                        st.balloons()
                except Exception as e:
                    st.error(f"Registration Failed: {e}")
            else:
                st.warning("Please enter an ID to register.")

    with tab_login:
        user_input = st.text_input("Enter your EDP ID to Access", key="login_box").strip()
        if st.button("Enter Dashboard"):
            logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
            if user_input in logins["Random_EDP_ID"].astype(str).values:
                st.session_state["user_id"] = user_input
                st.rerun()
            else:
                st.error("ID not found. Please register first.")

# ---------------- MAIN DASHBOARD ----------------
else:
    st.sidebar.title(f"👤 {st.session_state['user_id']}")
    nav = st.sidebar.radio("Menu", ["🚀 Place Order", "📂 My Products", "🌟 Portfolio"])
    
    if st.sidebar.button("🚪 Logout"):
        del st.session_state["user_id"]
        st.rerun()

    # SECTION 1: PLACE ORDER
    if nav == "🚀 Place Order":
        st.header("Create New Order")
        with st.form("order_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                country_code = st.selectbox("Code", ["+91 (India)", "+1 (USA)", "+44 (UK)"])
                phone = st.text_input("WhatsApp Number")
            with col2:
                # BRAHMASTRA: Direct Drive Upload
                raw_file = st.file_uploader("Upload Raw Footage (Max 200MB)", type=['mp4', 'mov', 'avi', 'jpg', 'png'])
            
            desc = st.text_area("Edit Description", placeholder="Describe transitions, music, and style...")
            
            if st.form_submit_button("Submit Order"):
                if phone and desc:
                    with st.spinner("Processing your order and uploading files..."):
                        try:
                            # 1. Find User's Folder ID
                            query = f"name='{st.session_state['user_id']}' and mimeType='application/vnd.google-apps.folder' and '{PARENT_FOLDER_ID}' in parents"
                            res = drive_service.files().list(q=query).execute()
                            u_folder_id = res['files'][0]['id']
                            
                            # 2. Upload File if provided
                            if raw_file:
                                file_metadata = {'name': f"RAW_{raw_file.name}", 'parents': [u_folder_id]}
                                media = MediaIoBaseUpload(io.BytesIO(raw_file.read()), mimetype=raw_file.type)
                                drive_service.files().create(body=file_metadata, media_body=media).execute()
                            
                            # 3. Log Order in Sheet
                            ord_conn = st.connection("gsheets", type=GSheetsConnection)
                            existing_orders = ord_conn.read(spreadsheet="EDIPREX_ORDERS", worksheet="Sheet1", ttl=0)
                            new_ord = pd.DataFrame([{
                                "User_Id": st.session_state["user_id"],
                                "Phone": f"{country_code.split()[0]} {phone}",
                                "ORDER": desc
                            }])
                            updated_ord = pd.concat([existing_orders, new_ord], ignore_index=True)
                            ord_conn.update(spreadsheet="EDIPREX_ORDERS", worksheet="Sheet1", data=updated_ord)
                            
                            st.success("✅ Order Placed! We will notify you on WhatsApp.")
                            st.balloons()
                        except Exception as e:
                            st.error(f"Submission Error: {e}")
                else:
                    st.warning("Please fill WhatsApp number and Order description.")

    # SECTION 2: MY PRODUCTS (Delivery logic)
    elif nav == "📂 My Products":
        st.header("Your Edited Deliveries")
        st.info("Download your final files from here.")
        # Logic to list files starting with 'EDITED_' from user folder
        st.write("Checking for new deliveries...")

    # SECTION 3: SAMPLES
    elif nav == "🌟 Portfolio":
        st.header("Our Recent Work")
        st.write("Take a look at our professional editing samples.")

    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 EDIPREX | Powered by Nilay")
