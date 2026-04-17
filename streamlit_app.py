import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- Load country dialing codes JSON ---
country_codes = {
    "Afghanistan": "+93",
    "Albania": "+355",
    "Algeria": "+213",
    "Andorra": "+376",
    "Angola": "+244",
    "Argentina": "+54",
    "Australia": "+61",
    "Austria": "+43",
    "Bangladesh": "+880",
    "Belgium": "+32",
    "Brazil": "+55",
    "Canada": "+1",
    "China": "+86",
    "France": "+33",
    "Germany": "+49",
    "India": "+91",
    "Italy": "+39",
    "Japan": "+81",
    "Mexico": "+52",
    "Nepal": "+977",
    "Nigeria": "+234",
    "Pakistan": "+92",
    "Russia": "+7",
    "Saudi Arabia": "+966",
    "Singapore": "+65",
    "South Africa": "+27",
    "Spain": "+34",
    "Sri Lanka": "+94",
    "United Arab Emirates": "+971",
    "United Kingdom": "+44",
    "United States": "+1",
    "Vietnam": "+84",
    "Zimbabwe": "+263"
    # ... include all countries from your JSON file
}

# --- Google Sheets connection ---
conn = st.connection("gsheets", type=GSheetsConnection)
existing = conn.read(worksheet="Sheet1", ttl=0)

# --- UI ---
st.subheader("Place Your Order")

# Country code selectbox
c = st.selectbox("Select your country code", options=list(country_codes.keys()))
selected_code = country_codes[c]

# Phone number input
r = st.text_input("Enter your phone/WhatsApp number (without country code)")

# Order description
m = st.text_area("Describe the edit you want to make in detail")

# --- Submit ---
if r and m:
    if st.button("Submit"):
        new_row = pd.DataFrame([{
            "C_c": selected_code,   # store selected country code
            "Phone": int(r),        # store phone number
            "ORDER": m.strip()      # store order description
        }])
        updated = pd.concat([existing, new_row], ignore_index=True).dropna(how='all')
        conn.update(worksheet="Sheet1", data=updated) 
        st.success("Your Order has been successfully submitted!")
        st.balloons()
else:
    st.info("Don't worry, your details are protected with Google.")
