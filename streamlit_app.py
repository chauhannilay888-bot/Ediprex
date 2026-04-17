import streamlit as st
st.info("Something coming soon with a very cool concept. Stay tuned! 😉")
conn = st.connection("gsheets", type="gspread")

# Read "Sheet1" into a DataFrame
file_path = conn.read(worksheet="Sheet1")

# Display in Streamlit
st.dataframe(file_path)
