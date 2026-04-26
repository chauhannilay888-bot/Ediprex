import streamlit as st
import pandas as pd
import requests
from streamlit_gsheets import GSheetsConnection
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ediprex - Professional Video & Photo Edits",
    page_icon="sZ6eW.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOGIN SYSTEM ----------------
if "user_id" not in st.session_state:
    st.title("Welcome to EDIPREX")
    choice = st.radio("Are you a new or old user?", ["New", "Old"])

    conn = st.connection("gsheets", type=GSheetsConnection)

    # Load existing logins
    try:
        logins = conn.read(spreadsheet="Ediprex_Logins", worksheet="Sheet1", ttl=0)
    except:
        logins = pd.DataFrame(columns=["Random_EDP_ID"])

    creds = Credentials.from_service_account_info(st.secrets["connections"]["gsheets"])
    drive_service = build('drive', 'v3', credentials=creds)
    parent_folder_id = "1cbr28a9N7YcW-r0Lv5i99YJEh1KAYFbr"  # Ediprex_main folder ID

    if choice == "New":
        new_id = st.text_input("Create your EDIPREX ID (example: nilay123450)")
        if st.button("Register"):
            if new_id.strip() == "":
                st.warning("Please enter a valid ID.")
            elif new_id in logins["Random_EDP_ID"].values:
                st.error("This ID already exists. Please choose another.")
            else:
                # Append new ID
                new_row = pd.DataFrame([{"Random_EDP_ID": new_id.strip()}])
                updated = pd.concat([logins, new_row], ignore_index=True)
                conn.update(spreadsheet="Ediprex_Logins", worksheet="Sheet1", data=updated)

                # Create subfolder in Drive
                drive_service.files().create(
                    body={"name": new_id.strip(), "mimeType": "application/vnd.google-apps.folder", "parents": [parent_folder_id]}
                ).execute()

                st.session_state["user_id"] = new_id.strip()
                st.success(f"Account created! Your ID: {new_id.strip()}")

    elif choice == "Old":
        old_id = st.text_input("Enter your EDIPREX ID")
        if st.button("Login"):
            if old_id in logins["Random_EDP_ID"].values:
                st.session_state["user_id"] = old_id
                st.success(f"Welcome back, {old_id}!")
            else:
                st.error("ID not found. Please try again or register as new.")

# ---------------- MAIN APP ----------------
if "user_id" in st.session_state:
    sidebar_choice = st.sidebar.radio("Navigation", ["Home", "My Products"])

    # ---------------- MY PRODUCTS ----------------
    if sidebar_choice == "My Products":
        st.subheader(f"📂 My Products ({st.session_state['user_id']})")

        # Find the user’s personal folder inside Ediprex_main
        results = drive_service.files().list(
            q=f"'{parent_folder_id}' in parents and name='{st.session_state['user_id']}' and mimeType='application/vnd.google-apps.folder'"
        ).execute()
        user_folders = results.get('files', [])

        if user_folders:
            user_folder_id = user_folders[0]["id"]
            user_files = drive_service.files().list(q=f"'{user_folder_id}' in parents").execute().get('files', [])

            if user_files:
                for file in user_files:
                    file_id = file["id"]
                    file_name = file["name"]
                    file_url = f"https://drive.google.com/uc?id={file_id}"

                    st.write(f"🎬 {file_name}")
                    st.video(file_url)
                    st.download_button(
                        label="⬇️ Download MP4",
                        data=requests.get(file_url).content,
                        file_name=file_name,
                        mime="video/mp4"
                    )
            else:
                st.info("Your folder is empty. Your edits will appear here within 24-48 hours.")
        else:
            st.warning("Your personal folder was not found. Please contact support.")

    # ---------------- HOME (Orders + Samples) ----------------
    else:
        option = st.radio("Select an option", 
                          options=["Place Order for Edit", "Check Samples"], 
                          horizontal=True)

        # ---------------- CHECK SAMPLES ----------------
        if option == "Check Samples":
            st.subheader("🎬 Take a look at some of our recent impressive edits")

            results = drive_service.files().list(q=f"'{parent_folder_id}' in parents").execute()
            files = results.get('files', [])

            if files:
                video_files = [f for f in files if f["name"].lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
                if video_files:
                    for i in range(0, len(video_files), 3):
                        cols = st.columns(3)
                        for j, col in enumerate(cols):
                            if i + j < len(video_files):
                                file = video_files[i + j]
                                file_id = file["id"]
                                video_url = f"https://drive.google.com/uc?id={file_id}"
                                with col:
                                    st.video(video_url)
                else:
                    st.info("No video samples available yet.")
            else:
                st.warning("No files found in the Drive folder.")

        # ---------------- PLACE ORDER ----------------
        else:
            st.subheader("🚀 Place Your Order")

            conn = st.connection("gsheets", type=GSheetsConnection)

            try:
                existing = conn.read(spreadsheet="EDIPREX_ORDERS", worksheet="Sheet1", ttl=0)
            except:
                existing = pd.DataFrame(columns=["User_Id", "C_c", "Phone", "ORDER"])

            selected_country = st.selectbox("🌍 Select your country", options=["🇮🇳 India (+91)", "🇺🇸 United States (+1)"])
            selected_code = selected_country.split()[-1]

            r = st.text_input("📱 Enter your WhatsApp / Phone number (without country code)", placeholder="9876543210")
            m = st.text_area("✍️ Describe the edit you want in detail", 
                             placeholder="Example: Make a cinematic reel from my raw footage with smooth transitions, trending music...",
                             height=150)

            if st.button("🚀 Submit Order", type="primary", use_container_width=True):
                if not r or not m.strip():
                    st.warning("Please fill both phone number and edit description.")
                else:
                    try:
                        new_row = pd.DataFrame([{
                            "User_Id": st.session_state["user_id"],
                            "C_c": selected_code,
                            "Phone": r.strip(),
                            "ORDER": m.strip()
                        }])

                        updated = pd.concat([existing, new_row], ignore_index=True).dropna(how='all')
                        conn.update(spreadsheet="EDIPREX_ORDERS", worksheet="Sheet1", data=updated)

                        st.success("🎉 Order Submitted Successfully!")
                        st.info("Your edit will be delivered in 24-48 hours in your 'My Products' section.")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error submitting order: {e}")

    st.caption("Made with passion by Nilay & his best friend")
