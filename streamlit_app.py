import streamlit as st
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ediprex - Professional Video & Photo Edits",
    page_icon="sZ6eW.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hero Section (same rakha)
st.markdown("""
<style>
    .hero { background: linear-gradient(135deg, #0f172a, #1e2937); padding: 70px 20px; 
            text-align: center; border-radius: 20px; margin-bottom: 30px; }
    .main-title { font-size: clamp(2.8rem, 8vw, 5rem); font-weight: 900; 
                  background: linear-gradient(90deg, #4facfe, #00f2fe); 
                  -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .subtitle { font-size: 1.35rem; color: #cbd5e1; max-width: 720px; margin: 0 auto; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1 class="main-title">EDIPREX</h1>
    <p class="subtitle">Professional Video & Photo Edits — Fast, Creative & Delivered in 24-48 Hours</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FULL COUNTRY LIST WITH FLAGS (Fixed for better visibility) ----------------
country_list = {
    "🇮🇳 India (+91)": "+91",
    "🇺🇸 United States (+1)": "+1",
    "🇬🇧 United Kingdom (+44)": "+44",
    "🇨🇦 Canada (+1)": "+1",
    "🇦🇺 Australia (+61)": "+61",
    "🇩🇪 Germany (+49)": "+49",
    "🇫🇷 France (+33)": "+33",
    "🇯🇵 Japan (+81)": "+81",
    "🇨🇳 China (+86)": "+86",
    "🇵🇰 Pakistan (+92)": "+92",
    "🇧🇩 Bangladesh (+880)": "+880",
    "🇧🇷 Brazil (+55)": "+55",
    "🇲🇽 Mexico (+52)": "+52",
    "🇷🇺 Russia (+7)": "+7",
    "🇮🇹 Italy (+39)": "+39",
    "🇪🇸 Spain (+34)": "+34",
    "🇳🇬 Nigeria (+234)": "+234",
    "🇰🇪 Kenya (+254)": "+254",
    "🇿🇦 South Africa (+27)": "+27",
    "🇹🇷 Turkey (+90)": "+90",
    "🇸🇦 Saudi Arabia (+966)": "+966",
    "🇦🇪 UAE (+971)": "+971",
    "🇮🇷 Iran (+98)": "+98",
    "🇮🇩 Indonesia (+62)": "+62",
    "🇵🇭 Philippines (+63)": "+63",
    "🇻🇳 Vietnam (+84)": "+84",
    "🇹🇭 Thailand (+66)": "+66",
    "🇲🇾 Malaysia (+60)": "+60",
    "🇸🇬 Singapore (+65)": "+65",
    "🇰🇷 South Korea (+82)": "+82",
    "🇭🇰 Hong Kong (+852)": "+852",
    "🇹🇼 Taiwan (+886)": "+886",
    "🇦🇫 Afghanistan (+93)": "+93",
    "🇦🇱 Albania (+355)": "+355",
    "🇩🇿 Algeria (+213)": "+213",
    "🇦🇴 Angola (+244)": "+244",
    "🇦🇷 Argentina (+54)": "+54",
    "🇦🇲 Armenia (+374)": "+374",
    "🇦🇹 Austria (+43)": "+43",
    "🇦🇿 Azerbaijan (+994)": "+994",
    "🇧🇭 Bahrain (+973)": "+973",
    "🇧🇪 Belgium (+32)": "+32",
    "🇧🇴 Bolivia (+591)": "+591",
    "🇧🇦 Bosnia (+387)": "+387",
    "🇧🇼 Botswana (+267)": "+267",
    "🇧🇬 Bulgaria (+359)": "+359",
    "🇰🇭 Cambodia (+855)": "+855",
    "🇨🇲 Cameroon (+237)": "+237",
    "🇨🇱 Chile (+56)": "+56",
    "🇨🇴 Colombia (+57)": "+57",
    "🇨🇷 Costa Rica (+506)": "+506",
    "🇭🇷 Croatia (+385)": "+385",
    "🇨🇺 Cuba (+53)": "+53",
    "🇨🇾 Cyprus (+357)": "+357",
    "🇨🇿 Czech Republic (+420)": "+420",
    "🇩🇰 Denmark (+45)": "+45",
    "🇩🇴 Dominican Republic (+1-809)": "+1-809",
    "🇪🇨 Ecuador (+593)": "+593",
    "🇪🇬 Egypt (+20)": "+20",
    "🇸🇻 El Salvador (+503)": "+503",
    "🇪🇪 Estonia (+372)": "+372",
    "🇪🇹 Ethiopia (+251)": "+251",
    "🇫🇮 Finland (+358)": "+358",
    "🇬🇦 Gabon (+241)": "+241",
    "🇬🇲 Gambia (+220)": "+220",
    "🇬🇪 Georgia (+995)": "+995",
    "🇬🇭 Ghana (+233)": "+233",
    "🇬🇷 Greece (+30)": "+30",
    "🇬🇹 Guatemala (+502)": "+502",
    "🇭🇳 Honduras (+504)": "+504",
    "🇭🇺 Hungary (+36)": "+36",
    "🇮🇸 Iceland (+354)": "+354",
    "🇮🇪 Ireland (+353)": "+353",
    "🇮🇱 Israel (+972)": "+972",
    "🇯🇴 Jordan (+962)": "+962",
    "🇰🇿 Kazakhstan (+7)": "+7",
    "🇰🇼 Kuwait (+965)": "+965",
    "🇰🇬 Kyrgyzstan (+996)": "+996",
    "🇱🇧 Lebanon (+961)": "+961",
    "🇱🇹 Lithuania (+370)": "+370",
    "🇱🇺 Luxembourg (+352)": "+352",
    "🇲🇬 Madagascar (+261)": "+261",
    "🇲🇼 Malawi (+265)": "+265",
    "🇲🇻 Maldives (+960)": "+960",
    "🇲🇱 Mali (+223)": "+223",
    "🇲🇹 Malta (+356)": "+356",
    "🇲🇷 Mauritania (+222)": "+222",
    "🇲🇺 Mauritius (+230)": "+230",
    "🇲🇩 Moldova (+373)": "+373",
    "🇲🇳 Mongolia (+976)": "+976",
    "🇲🇦 Morocco (+212)": "+212",
    "🇲🇿 Mozambique (+258)": "+258",
    "🇲🇲 Myanmar (+95)": "+95",
    "🇳🇵 Nepal (+977)": "+977",
    "🇳🇱 Netherlands (+31)": "+31",
    "🇳🇿 New Zealand (+64)": "+64",
    "🇳🇮 Nicaragua (+505)": "+505",
    "🇳🇴 Norway (+47)": "+47",
    "🇴🇲 Oman (+968)": "+968",
    "🇵🇦 Panama (+507)": "+507",
    "🇵🇾 Paraguay (+595)": "+595",
    "🇵🇪 Peru (+51)": "+51",
    "🇵🇱 Poland (+48)": "+48",
    "🇵🇹 Portugal (+351)": "+351",
    "🇶🇦 Qatar (+974)": "+974",
    "🇷🇴 Romania (+40)": "+40",
    "🇷🇼 Rwanda (+250)": "+250",
    "🇸🇳 Senegal (+221)": "+221",
    "🇷🇸 Serbia (+381)": "+381",
    "🇸🇰 Slovakia (+421)": "+421",
    "🇸🇮 Slovenia (+386)": "+386",
    "🇱🇰 Sri Lanka (+94)": "+94",
    "🇸🇩 Sudan (+249)": "+249",
    "🇸🇪 Sweden (+46)": "+46",
    "🇨🇭 Switzerland (+41)": "+41",
    "🇸🇾 Syria (+963)": "+963",
    "🇹🇯 Tajikistan (+992)": "+992",
    "🇹🇿 Tanzania (+255)": "+255",
    "🇹🇳 Tunisia (+216)": "+216",
    "🇹🇷 Turkey (+90)": "+90",
    "🇺🇬 Uganda (+256)": "+256",
    "🇺🇦 Ukraine (+380)": "+380",
    "🇺🇾 Uruguay (+598)": "+598",
    "🇺🇿 Uzbekistan (+998)": "+998",
    "🇻🇪 Venezuela (+58)": "+58",
    "🇻🇳 Vietnam (+84)": "+84",
    "🇾🇪 Yemen (+967)": "+967",
    "🇿🇲 Zambia (+260)": "+260",
    "🇿🇼 Zimbabwe (+263)": "+263"
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

    # Country with Flag (Clean & Visible)
    selected_country = st.selectbox("🌍 Select your country", 
                                    options=list(country_list.keys()))
    selected_code = country_list[selected_country]
    
    r = st.text_input("📱 Enter your WhatsApp / Phone number (without country code)", 
                      placeholder="9876543210")

    m = st.text_area("✍️ Describe the edit you want in detail", 
                     placeholder="Example: Make a cinematic reel from my raw footage with smooth transitions, trending music...",
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
