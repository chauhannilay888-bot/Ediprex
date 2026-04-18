import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# ---------------- 2. PAGE CONFIG ----------------
st.set_page_config(
  page_title="Ediprex - Give Order For Making Impressive Edits For FREE!",
  page_icon="sZ6eW.jpg",
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
      min-height: 100vh; /* Full height for all devices */
      margin: 0;
      font-family: 'Poppins', sans-serif;
      text-align: center;
      padding: 1rem;
    }

    h1 {
      font-size: clamp(2rem, 5vw, 4rem); /* Flexible font size */
      color: #fff;
      text-transform: uppercase;
      letter-spacing: 0.2em;
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
      word-wrap: break-word;
    }

    @keyframes float {
      0%, 100% { transform: translateY(0) rotateX(0deg); }
      50% { transform: translateY(-10px) rotateX(5deg); }
    }

    /* Media queries for extra fine-tuning */
    @media (max-width: 768px) {
      h1 {
        font-size: clamp(1.5rem, 6vw, 3rem);
        letter-spacing: 0.1em;
      }
    }

    @media (max-width: 480px) {
      h1 {
        font-size: clamp(1.2rem, 8vw, 2.5rem);
        letter-spacing: 0.05em;
      }
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

# --- Country dialing codes (shortened for demo, expand with full JSON) ---
country_codes = {
    "Afghanistan": "+93",
    "Albania": "+355",
    "Algeria": "+213",
    "Andorra": "+376",
    "Angola": "+244",
    "Argentina": "+54",
    "Armenia": "+374",
    "Australia": "+61",
    "Austria": "+43",
    "Azerbaijan": "+994",
    "Bahamas": "+1-242",
    "Bahrain": "+973",
    "Bangladesh": "+880",
    "Barbados": "+1-246",
    "Belarus": "+375",
    "Belgium": "+32",
    "Belize": "+501",
    "Benin": "+229",
    "Bhutan": "+975",
    "Bolivia": "+591",
    "Bosnia and Herzegovina": "+387",
    "Botswana": "+267",
    "Brazil": "+55",
    "Brunei": "+673",
    "Bulgaria": "+359",
    "Burkina Faso": "+226",
    "Burundi": "+257",
    "Cambodia": "+855",
    "Cameroon": "+237",
    "Canada": "+1",
    "Chad": "+235",
    "Chile": "+56",
    "China": "+86",
    "Colombia": "+57",
    "Costa Rica": "+506",
    "Croatia": "+385",
    "Cuba": "+53",
    "Cyprus": "+357",
    "Czech Republic": "+420",
    "Denmark": "+45",
    "Dominican Republic": "+1-809",
    "Ecuador": "+593",
    "Egypt": "+20",
    "El Salvador": "+503",
    "Estonia": "+372",
    "Ethiopia": "+251",
    "Fiji": "+679",
    "Finland": "+358",
    "France": "+33",
    "Gabon": "+241",
    "Gambia": "+220",
    "Georgia": "+995",
    "Germany": "+49",
    "Ghana": "+233",
    "Greece": "+30",
    "Guatemala": "+502",
    "Honduras": "+504",
    "Hong Kong": "+852",
    "Hungary": "+36",
    "Iceland": "+354",
    "India": "+91",
    "Indonesia": "+62",
    "Iran": "+98",
    "Iraq": "+964",
    "Ireland": "+353",
    "Israel": "+972",
    "Italy": "+39",
    "Jamaica": "+1-876",
    "Japan": "+81",
    "Jordan": "+962",
    "Kazakhstan": "+7",
    "Kenya": "+254",
    "Kuwait": "+965",
    "Kyrgyzstan": "+996",
    "Laos": "+856",
    "Latvia": "+371",
    "Lebanon": "+961",
    "Lesotho": "+266",
    "Liberia": "+231",
    "Libya": "+218",
    "Lithuania": "+370",
    "Luxembourg": "+352",
    "Macau": "+853",
    "Madagascar": "+261",
    "Malawi": "+265",
    "Malaysia": "+60",
    "Maldives": "+960",
    "Mali": "+223",
    "Malta": "+356",
    "Mauritania": "+222",
    "Mauritius": "+230",
    "Mexico": "+52",
    "Moldova": "+373",
    "Monaco": "+377",
    "Mongolia": "+976",
    "Montenegro": "+382",
    "Morocco": "+212",
    "Mozambique": "+258",
    "Myanmar": "+95",
    "Namibia": "+264",
    "Nepal": "+977",
    "Netherlands": "+31",
    "New Zealand": "+64",
    "Nicaragua": "+505",
    "Niger": "+227",
    "Nigeria": "+234",
    "North Korea": "+850",
    "Norway": "+47",
    "Oman": "+968",
    "Pakistan": "+92",
    "Panama": "+507",
    "Paraguay": "+595",
    "Peru": "+51",
    "Philippines": "+63",
    "Poland": "+48",
    "Portugal": "+351",
    "Qatar": "+974",
    "Romania": "+40",
    "Russia": "+7",
    "Rwanda": "+250",
    "Saudi Arabia": "+966",
    "Senegal": "+221",
    "Serbia": "+381",
    "Singapore": "+65",
    "Slovakia": "+421",
    "Slovenia": "+386",
    "Somalia": "+252",
    "South Africa": "+27",
    "South Korea": "+82",
    "Spain": "+34",
    "Sri Lanka": "+94",
    "Sudan": "+249",
    "Sweden": "+46",
    "Switzerland": "+41",
    "Syria": "+963",
    "Taiwan": "+886",
    "Tajikistan": "+992",
    "Tanzania": "+255",
    "Thailand": "+66",
    "Tunisia": "+216",
    "Turkey": "+90",
    "Uganda": "+256",
    "Ukraine": "+380",
    "United Arab Emirates": "+971",
    "United Kingdom": "+44",
    "United States": "+1",
    "Uruguay": "+598",
    "Uzbekistan": "+998",
    "Venezuela": "+58",
    "Vietnam": "+84",
    "Yemen": "+967",
    "Zambia": "+260",
    "Zimbabwe": "+263"
}

# --- Google Sheets connection ---
conn = st.connection("gsheets", type=GSheetsConnection)
existing = conn.read(worksheet="Sheet1", ttl=0)

# --- Order form ---
st.subheader("Place Your Order")

# Country code selectbox
c = st.selectbox("Select your country", options=list(country_codes.keys()))
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
        st.info("Your Edit will soon be delivered in 24 - 28 hrs via your number. ")
        st.balloons()
else:
    st.info("Don't worry, your details are protected with Google.")
