import streamlit as st
from streamlit_gsheets import GSheetsConnection
st.info("Something coming soon with a very cool concept. Stay tuned! 😉")
conn = st.connection("gsheets", type=GSheetsConnection)
existing = conn.read(worksheet="Sheet1", ttl=0)
