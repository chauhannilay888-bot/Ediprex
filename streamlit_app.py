import streamlit as st
from streamlit_gsheets import GSheetsConnection
st.info("Something coming soon with a very cool concept. Stay tuned! 😉")
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
  st.info("Don't worry, your details are protected with google. )

