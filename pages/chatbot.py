import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from utils.prompt_templates import MEDICAL_ADVICE_PROMPT
from utils.ui_helpers import mainmenu, set_disease_background

# -------------------------------------------------
# Page setup
# -------------------------------------------------
st.set_page_config(page_title="AI Health Assistant", page_icon="🤖", layout="wide")
set_disease_background("Image/chatbot.png")
mainmenu()

st.title("🤖 AI Health Assistant")
st.subheader("Personalized health advice based on your profile")

# -------------------------------------------------
# Guard: chatbot only after prediction
# -------------------------------------------------
if "prediction_result" not in st.session_state or "selected_disease" not in st.session_state:
    st.warning("Please complete a disease prediction first.")
    st.stop()

disease = st.session_state["selected_disease"]
prediction = "Positive" if st.session_state["prediction_result"] == 1 else "Negative"

# -------------------------------------------------
# Sidebar – Gemini API Key + Patient Profile
# -------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/883/883407.png", width=60)

    st.markdown("### 🔑 Gemini API Key")
    api_key = st.text_input(
        "Enter your Gemini API Key",
        type="password",
        help="Key is stored only for this session"
    )

    if api_key:
        st.session_state["GEMINI_API_KEY"] = api_key

    st.markdown("---")
    st.header("🧑‍⚕️ Patient Profile")

    with st.form("patient_form"):
        alcohol_status = st.selectbox(
            "Alcohol Consumption",
            ["Alcoholic", "Non-Alcoholic"]
        )
        junk_food_frequency = st.selectbox(
            "Junk Food Consumption",
            ["Regular", "Few days in a week", "No"]
        )
        physical_activity_level = st.selectbox(
            "Physical Activity",
            ["Regular", "Few days in a week", "No"]
        )
        area_type = st.selectbox(
            "Living Area",
            ["Urban", "Rural"]
        )
        pollution_level = st.selectbox(
            "Pollution Level in Area",
            ["High", "Medium", "Low"]
        )

        submitted = st.form_submit_button("Get Health Advice")

# -------------------------------------------------
# Context display
# -------------------------------------------------
st.markdown("### 🩺 Prediction Context")
st.write(f"**Disease:** {disease}")
st.write(f"**Prediction Result:** {prediction}")

# -------------------------------------------------
# Generate advice (dynamic prompt)
# -------------------------------------------------
if submitted:
    if "GEMINI_API_KEY" not in st.session_state:
        st.error("Please enter your Gemini API key in the sidebar.")
        st.stop()

    patient_data = {
        "disease": disease,
        "prediction_result": prediction,
        "alcohol_status": alcohol_status,
        "junk_food_frequency": junk_food_frequency,
        "physical_activity_level": physical_activity_level,
        "mental_wellness_activity": "Not specified",
        "area_type": area_type,
        "pollution_level": pollution_level
    }

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.4,
        google_api_key=st.session_state["GEMINI_API_KEY"]
    )

    prompt = PromptTemplate.from_template(MEDICAL_ADVICE_PROMPT)

    with st.spinner("Generating personalized health advice..."):
        try:
            response = llm.invoke(prompt.format(**patient_data))
            st.chat_message("assistant").markdown(response.content)
        except Exception as e:
            st.error(f"Failed to generate advice: {e}")

# -------------------------------------------------
# Navigation
# -------------------------------------------------
if st.button("🏠 Back to Home"):
    st.switch_page("app.py")
