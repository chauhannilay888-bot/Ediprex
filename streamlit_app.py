import streamlit as st
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection
from PIL import Image

# ---------------- 2. PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ediprex - Give Order For Making Impressive Edits For FREE!",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom HTML welcome banner ---
welcome_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="google-site-verification" content="zINnwjOarj-lAgHmEFrOPaihJvA5iwrmzhapCKGuqj0" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
      font-family: 'Poppins', sans-serif;
      text-align: center;
      padding: 1rem;
    }
    h1 {
      font-size: clamp(2rem, 5vw, 4rem);
      color: #fff;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      position: relative;
      animation: float 3s ease-in-out infinite;
      text-shadow: 1px 1px 0 #ccc, 2px 2px 0 #bbb, 3px 3px 0 #aaa,
                   4px 4px 0 #999, 5px 5px 0 #888, 6px 6px 0 #777,
                   7px 7px 0 #666, 8px 8px 15px rgba(0,0,0,0.6);
      word-wrap: break-word;
    }
    @keyframes float {
      0%, 100% { transform: translateY(0) rotateX(0deg); }
      50% { transform: translateY(-10px) rotateX(5deg); }
    }
    @media (max-width: 768px) {
      h1 { font-size: clamp(1.5rem, 6vw, 3rem); letter-spacing: 0.1em; }
    }
    @media (max-width: 480px) {
      h1 { font-size: clamp(1.2rem, 8vw, 2.5rem); letter-spacing: 0.05em; }
    }
  </style>
</head>
<body>
  <h1>Welcome to Ediprex!</h1>
</body>
</html>
"""
st.components.v1.html(welcome_html, height=200)

# --- Country dialing codes ---
country_codes = {
    "India": "+91", "United States": "+1", "United Kingdom": "+44",
    "Canada": "+1", "Australia": "+61", "Germany": "+49", "France": "+33",
    "Japan": "+81", "China": "+86", "Pakistan": "+92", "Bangladesh": "+880",
    # ... agar aur countries add karne hain toh yahan daal sakta hai
}

option = st.radio("Select an option", options=["Place Order", "Check Samples"])

if option == "Check Samples":
    st.subheader("Take a look at some of our previous edits!")
    folder_path = "SAMPLES"
    
    if os.path.exists(folder_path):
        video_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
        
        cols_per_row = 4
        for i in range(0, len(video_files), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(video_files):
                    video_path = os.path.join(folder_path, video_files[i + j])
                    with col:
                        st.video(video_path)
    else:
        st.warning("Samples folder not found.")

else:  # Place Order
    st.subheader("Place Your Order")
    
    # Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    try:
        existing = conn.read(worksheet="Sheet1", ttl=0)
    except:
        existing = pd.DataFrame(columns=["C_c", "Phone", "ORDER"])
    
    # Country code
    c = st.selectbox("Select your country", options=list(country_codes.keys()))
    selected_code = country_codes[c]
    
    # Phone number
    r = st.text_input("Enter your phone/WhatsApp number (without country code)")
    
    # Order description
    m = st.text_area("Describe the edit you want to make in detail", 
                     placeholder="Be as detailed as possible...")
    
    # Submit
    if st.button("Submit Order"):
        if not r or not m.strip():
            st.warning("Please fill both phone number and order description.")
        else:
            try:
                new_row = pd.DataFrame([{
                    "C_c": selected_code,
                    "Phone": r.strip(),
                    "ORDER": m.strip()
                }])
                
                updated = pd.concat([existing, new_row], ignore_index=True).dropna(how='all')
                conn.update(worksheet="Sheet1", data=updated)
                
                st.success("✅ Your Order has been successfully submitted!")
                st.info("Your Edit will soon be delivered in 24 - 48 hrs via your number.")
                st.balloons()
            except Exception as e:
                st.error(f"Error submitting order: {e}")

    else:
        st.info("Don't worry, your details are protected with Google.")
