import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- Custom HTML welcome banner ---
welcome_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    body {
      background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
      display: flex;
      justify-content: center;
      align-items: center;
      height: 30vh;
      margin: 0;
      font-family: 'Poppins', sans-serif;
    }
    h1 {
      font-size: 3rem;
      color: #fff;
      text-transform: uppercase;
      letter-spacing: 3px;
      position: relative;
      animation: float 3s ease-in-out infinite;
      text-shadow:
        1px 1px 0 #ccc,
        2px 2px 0 #bbb,
        3px 3px 0 #aaa,
        4px 4px 0 #999,
        5px 5px 0 #888,
        6px 6px 0 #777,
        7px 7px 0 #666,
        8px 8px 15px rgba(0,0,0,0.6);
    }
    @keyframes float {
      0%, 100% { transform: translateY(0) rotateX(0deg); }
      50% { transform: translateY(-10px) rotateX(5deg); }
    }
  </style>
</head>
<body>
  <h1>Welcome to Ediprex!</h1>
</body>
</html>
"""

# Render the HTML banner at the top of the Streamlit app
st.components.v1.html(welcome_html, height=200)

# --- Google Sheets connection ---
conn = st.connection("gsheets", type=GSheetsConnection)
existing = conn.read(worksheet="Sheet1", ttl=0)

# --- Order form ---
st.subheader("Place Your Order")
r = st.text_input("Enter your phone/WhatsApp number")
m = st.text_area("Describe the edit you want to make in detail")

if r and m:
    if st.button("Submit"):
        new_row = pd.DataFrame([{"Phone": int(r), "ORDER": m.strip()}])
        updated = pd.concat([existing, new_row], ignore_index=True).dropna(how='all')
        conn.update(worksheet="Sheet1", data=updated) 
        st.success("Your Order has been successfully submitted!")
        st.balloons()
else:
    st.info("Don't worry, your details are protected with Google.")
