import streamlit as st
from utils.ui_helpers import get_base64_of_bin_file

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Disease Prediction Home",
    page_icon="⚕️",
    layout="wide"
)

# -------------------------------------------------
# Hide sidebar & Streamlit chrome
# -------------------------------------------------
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
#MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# FIXED Spline background (IMPORTANT)
# -------------------------------------------------
st.markdown("""
<style>
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
}

/* Spline background */
#spline-bg {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    border: none;
    z-index: -1;
    pointer-events: none;
}

/* Streamlit app transparency */
.stApp {
    background: transparent;
}

/* Allow scrolling (CRITICAL FIX) */
body {
    overflow-x: hidden;
    overflow-y: auto;
}
</style>

<iframe
    id="spline-bg"
    src="https://my.spline.design/pillanddnaanimation-oHEADbdOIaEQNS23hH4hTNQZ/"
></iframe>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Content layout & button styling (unchanged look, stable width)
# -------------------------------------------------
st.markdown("""
<style>
.block-container {
    max-width: 1200px;
    padding-top: 6rem;
    padding-bottom: 4rem;
    margin-left: auto;
    margin-right: auto;
}

.stButton>button {
    width: 100% !important;
    height: 3.5rem;
    font-size: 1.2rem;
    font-weight: bolder;
    padding: 0.75rem 1.25rem;
    margin: 0.75rem 0;
    text-align: center;
    border-radius: 12px;
    color: #000000;
    background-color: rgba(255, 255, 255, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(8px);
    transition: 0.3s ease;
}

.stButton>button:hover {
    background-color: rgba(255, 255, 255, 0.35);
    color: #000000;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Logo (unchanged, correct)
# -------------------------------------------------
logo_base64 = get_base64_of_bin_file("Image/logo1.png")

st.markdown(
    f"""
    <style>
        .logo-container {{
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 100;
        }}
        .logo-container img {{
            height: 60px;
        }}
    </style>
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Main content
# -------------------------------------------------
st.title("🧠 Disease Prediction System")
st.subheader("Choose a prediction module")

col1, col2 = st.columns(2, gap="large")

with col1:
    if st.button("🔬 Diabetes Prediction"):
        st.switch_page("pages/diabetes.py")
    if st.button("🫀 Heart Disease Prediction"):
        st.switch_page("pages/heart.py")

with col2:
    if st.button("🧬 Fatty Liver Prediction"):
        st.switch_page("pages/fattyliver.py")
    if st.button("📰 Health Blog"):
        st.switch_page("pages/blog.py")