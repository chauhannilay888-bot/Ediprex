import streamlit as st
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ediprex - Give Order For Making Impressive Edits For FREE!",
    page_icon="sZ6eW.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- PREMIUM HERO SECTION ----------------
st.markdown("""
<style>
    .hero {
        background: linear-gradient(135deg, #0f172a, #1e2937);
        padding: 70px 20px;
        text-align: center;
        border-radius: 20px;
        margin-bottom: 30px;
    }
    .main-title {
        font-size: clamp(2.8rem, 8vw, 5rem);
        font-weight: 900;
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.35rem;
        color: #cbd5e1;
        max-width: 720px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1 class="main-title">EDIPREX</h1>
    <p class="subtitle">
        Professional Video & Photo Edits — Fast, Creative & Delivered in 24-48 Hours
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- FULL COUNTRY LIST WITH FLAGS ----------------
country_codes = {
    "🇮🇳 India": "+91",
    "🇺🇸 United States": "+1",
    "🇬🇧 United Kingdom": "+44",
    "🇨🇦 Canada": "+1",
    "🇦🇺 Australia": "+61",
    "🇩🇪 Germany": "+49",
    "🇫🇷 France": "+33",
    "🇯🇵 Japan": "+81",
    "🇨🇳 China": "+86",
    "🇵🇰 Pakistan": "+92",
    "🇧🇩 Bangladesh": "+880",
    "🇧🇷 Brazil": "+55",
    "🇲🇽 Mexico": "+52",
    "🇷🇺 Russia": "+7",
    "🇮🇹 Italy": "+39",
    "🇪🇸 Spain": "+34",
    "🇳🇬 Nigeria": "+234",
    "🇰🇪 Kenya": "+254",
    "🇿🇦 South Africa": "+27",
    "🇹🇷 Turkey": "+90",
    "🇸🇦 Saudi Arabia": "+966",
    "🇦🇪 United Arab Emirates": "+971",
    "🇮🇷 Iran": "+98",
    "🇮🇩 Indonesia": "+62",
    "🇵🇭 Philippines": "+63",
    "🇻🇳 Vietnam": "+84",
    "🇹🇭 Thailand": "+66",
    "🇲🇾 Malaysia": "+60",
    "🇸🇬 Singapore": "+65",
    "🇰🇷 South Korea": "+82",
    "🇭🇰 Hong Kong": "+852",
    "🇹🇼 Taiwan": "+886",
    "🇦🇫 Afghanistan": "+93",
    "🇦🇱 Albania": "+355",
    "🇩🇿 Algeria": "+213",
    "🇦🇴 Angola": "+244",
    "🇦🇷 Argentina": "+54",
    "🇦🇲 Armenia": "+374",
    "🇦🇹 Austria": "+43",
    "🇦🇿 Azerbaijan": "+994",
    "🇧🇭 Bahrain": "+973",
    "🇧🇪 Belgium": "+32",
    "🇧🇴 Bolivia": "+591",
    "🇧🇦 Bosnia": "+387",
    "🇧🇼 Botswana": "+267",
    "🇧🇬 Bulgaria": "+359",
    "🇰🇭 Cambodia": "+855",
    "🇨🇲 Cameroon": "+237",
    "🇨🇱 Chile": "+56",
    "🇨🇴 Colombia": "+57",
    "🇨🇷 Costa Rica": "+506",
    "🇭🇷 Croatia": "+385",
    "🇨🇺 Cuba": "+53",
    "🇨🇾 Cyprus": "+357",
    "🇨🇿 Czech Republic": "+420",
    "🇩🇰 Denmark": "+45",
    "🇩🇴 Dominican Republic": "+1-809",
    "🇪🇨 Ecuador": "+593",
    "🇪🇬 Egypt": "+20",
    "🇸🇻 El Salvador": "+503",
    "🇪🇪 Estonia": "+372",
    "🇪🇹 Ethiopia": "+251",
    "🇫🇮 Finland": "+358",
    "🇬🇦 Gabon": "+241",
    "🇬🇲 Gambia": "+220",
    "🇬🇪 Georgia": "+995",
    "🇬🇭 Ghana": "+233",
    "🇬🇷 Greece": "+30",
    "🇬🇹 Guatemala": "+502",
    "🇭🇳 Honduras": "+504",
    "🇭🇺 Hungary": "+36",
    "🇮🇸 Iceland": "+354",
    "🇮🇪 Ireland": "+353",
    "🇮🇱 Israel": "+972",
    "🇯🇴 Jordan": "+962",
    "🇰🇿 Kazakhstan": "+7",
    "🇰🇼 Kuwait": "+965",
    "🇰🇬 Kyrgyzstan": "+996",
    "🇱🇧 Lebanon": "+961",
    "🇱🇹 Lithuania": "+370",
    "🇱🇺 Luxembourg": "+352",
    "🇲🇬 Madagascar": "+261",
    "🇲🇼 Malawi": "+265",
    "🇲🇻 Maldives": "+960",
    "🇲🇱 Mali": "+223",
    "🇲🇹 Malta": "+356",
    "🇲🇷 Mauritania": "+222",
    "🇲🇺 Mauritius": "+230",
    "🇲🇩 Moldova": "+373",
    "🇲🇳 Mongolia": "+976",
    "🇲🇦 Morocco": "+212",
    "🇲🇿 Mozambique": "+258",
    "🇲🇲 Myanmar": "+95",
    "🇳🇵 Nepal": "+977",
    "🇳🇱 Netherlands": "+31",
    "🇳🇿 New Zealand": "+64",
    "🇳🇮 Nicaragua": "+505",
    "🇳🇴 Norway": "+47",
    "🇴🇲 Oman": "+968",
    "🇵🇦 Panama": "+507",
    "🇵🇾 Paraguay": "+595",
    "🇵🇪 Peru": "+51",
    "🇵🇱 Poland": "+48",
    "🇵🇹 Portugal": "+351",
    "🇶🇦 Qatar": "+974",
    "🇷🇴 Romania": "+40",
    "🇷🇼 Rwanda": "+250",
    "🇸🇳 Senegal": "+221",
    "🇷🇸 Serbia": "+381",
    "🇸🇰 Slovakia": "+421",
    "🇸🇮 Slovenia": "+386",
    "🇱🇰 Sri Lanka": "+94",
    "🇸🇩 Sudan": "+249",
    "🇸🇪 Sweden": "+46",
    "🇨🇭 Switzerland": "+41",
    "🇸🇾 Syria": "+963",
    "🇹🇯 Tajikistan": "+992",
    "🇹🇿 Tanzania": "+255",
    "🇹🇳 Tunisia": "+216",
    "🇺🇬 Uganda": "+256",
    "🇺🇦 Ukraine": "+380",
    "🇺🇾 Uruguay": "+598",
    "🇺🇿 Uzbekistan": "+998",
    "🇻🇪 Venezuela": "+58",
    "🇾🇪 Yemen": "+967",
    "🇿🇲 Zambia": "+260",
    "🇿🇼 Zimbabwe": "+263"
}

option = st.radio("Select an option", 
                  options=["Place Order for Edit", "Check Samples"], 
                  horizontal=True)

if option == "Check Samples":
    st.subheader("🎬 Take a look at some of our recent impressive edits")
    folder_path = "SAMPLES"
    
    if os.path.exists(folder_path):
        video_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
        if video_files:
            for i in range(0, len(video_files), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(video_files):
                        video_path = os.path.join(folder_path, video_files[i + j])
                        with col:
                            st.video(video_path)
        else:
            st.info("No samples available yet.")
    else:
        st.warning("Samples folder not found.")

else:  # Place Order
    st.subheader("🚀 Place Your Order")
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    try:
        existing = conn.read(worksheet="Sheet1", ttl=0)
    except:
        existing = pd.DataFrame(columns=["C_c", "Phone", "ORDER"])

    # Country with Flag
    c = st.selectbox("🌍 Select your country", options=list(country_codes.keys()))
    selected_code = country_codes[c]
    
    r = st.text_input("📱 Enter your WhatsApp / Phone number (without country code)", 
                      placeholder="9876543210")

    m = st.text_area("✍️ Describe the edit you want in detail", 
                     placeholder="Example: Make a cinematic reel from my raw footage with smooth transitions, trending music, text overlays and end screen...",
                     height=150)

    if st.button("🚀 Submit Order", type="primary", use_container_width=True):
        if not r or not m.strip():
            st.warning("Please fill both phone number and edit description.")
        else:
            try:
                new_row = pd.DataFrame([{
                    "C_c": selected_code,
                    "Phone": r.strip(),
                    "ORDER": m.strip()
                }])
                
                updated = pd.concat([existing, new_row], ignore_index=True).dropna(how='all')
                conn.update(worksheet="Sheet1", data=updated)
                
                st.success("🎉 Order Submitted Successfully!")
                st.info("Your edit will be delivered in 24-48 hours on your WhatsApp number.")
                st.balloons()
            except Exception as e:
                st.error(f"Error submitting order: {e}")

st.caption("Made with passion by Nilay & his best friend")
