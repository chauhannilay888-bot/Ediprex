import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
st.markdown("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Welcome Text</title>
<style>
    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        font-family: 'Poppins', sans-serif;
    }

    h1 {
        font-size: 3.5rem;
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 3px;
        position: relative;
        animation: float 3s ease-in-out infinite;
        
        /* 3D depth using multiple shadows */
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

    /* Floating animation */
    @keyframes float {
        0%, 100% {
            transform: translateY(0) rotateX(0deg);
        }
        50% {
            transform: translateY(-10px) rotateX(5deg);
        }
    }
</style>
</head>
<body>

<h1>Welcome To Ediprex !</h1>

</body>
</html>
""", allow_unsafe_html = True)

conn = st.connection("gsheets", type=GSheetsConnection)
existing = conn.read(worksheet="Sheet1", ttl=0)
r = st.text_input("Enter your phone/whatsapp number")
m = st.text_area("Describe the edit you want to make in detail")
if r and m:
  if st.button("Submit"):
    new_row = pd.DataFrame([{"Phone": int(r), "ORDER": m.strip()}])
    updated = pd.concat([existing, new_row], ignore_index=True).dropna(how='all')
    conn.update(worksheet="Sheet1", data=updated) 
    st.success("Your Order is successfully submited! ")
    st.balloons()
else:
  st.info("Don't worry, your details are protected with google. ")

