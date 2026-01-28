import streamlit as st
import pickle
from utils.ui_helpers import set_disease_background, disease_sidebar, mainmenu

# -------------------------------------------------
# Page setup
# -------------------------------------------------
st.set_page_config(page_title="Diabetes Prediction", page_icon="🔬", layout="wide")
set_disease_background("Image/Diabetes.png")
disease_sidebar("Diabetes")
mainmenu()

st.title("🔬 Diabetes Prediction")

# -------------------------------------------------
# Load model
# -------------------------------------------------
with open("Models/diabetes_model.pkl", "rb") as f:
    model = pickle.load(f)

# -------------------------------------------------
# Input fields
# -------------------------------------------------
features = [
    "Glucose Level", "Blood Pressure value", "Skin Thickness value",
    "Insulin Level", "BMI value", "Diabetes Pedigree Function", "Age"
]

placeholders = [
    "52.2 - 274 mg/dL", "5.9 - 115 mm Hg", "2.9 - 23.3 mm",
    "50 - 180 μU/mL", "2.61 - 41.62 kg/m²", "0.08 - 2.42", "Enter your age"
]

cols = st.columns(3)
inputs = []

gender = cols[0].selectbox("Select Gender", ["Male", "Female"])

if gender == "Female":
    preg = cols[1].text_input("Number of Pregnancies")
else:
    preg = cols[1].text_input("Number of Pregnancies", value="0", disabled=True)

inputs.append(preg)

for i, feat in enumerate(features):
    col = cols[(i + 2) % 3]
    val = col.text_input(feat, placeholder=placeholders[i])
    inputs.append(val)

# -------------------------------------------------
# Prediction
# -------------------------------------------------
if st.button("🔍 Predict"):
    if "" in inputs:
        st.error("Please fill all fields.")
    else:
        try:
            data = [float(x) for x in inputs]
            prediction = model.predict([data])[0]

            # Store for chatbot
            st.session_state["selected_disease"] = "Diabetes"
            st.session_state["prediction_result"] = prediction

        except ValueError:
            st.error("Please enter valid numeric values.")

# -------------------------------------------------
# Result display (inline)
# -------------------------------------------------
if "prediction_result" in st.session_state:
    st.markdown("---")
    st.subheader("🧾 Prediction Result")

    if st.session_state["prediction_result"] == 1:
        st.error("🔴 Likely **Diabetes Positive**")
    else:
        st.success("🟢 Likely **Not Diabetes Positive**")

    if st.button("💬 Talk to AI Assistant"):
        st.switch_page("pages/chatbot.py")

# -------------------------------------------------
# Navigation
# -------------------------------------------------
if st.button("🏠 Back to Home"):
    st.switch_page("app.py")
