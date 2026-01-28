import streamlit as st
import pickle
from utils.ui_helpers import set_disease_background, disease_sidebar, mainmenu

# -------------------------------------------------
# Page setup
# -------------------------------------------------
st.set_page_config(page_title="Fatty Liver Prediction", page_icon="🧬", layout="wide")
set_disease_background("Image/Liver.png")
disease_sidebar("Fatty Liver")
mainmenu()

st.title("🧬 Fatty Liver Prediction")

# -------------------------------------------------
# Load model
# -------------------------------------------------
with open("Models/fatty_liver.pkl", "rb") as f:
    model = pickle.load(f)

# -------------------------------------------------
# Input fields
# -------------------------------------------------
features = ["age", "gender", "weight", "height"]
inputs = []
cols = st.columns(3)

for i, feat in enumerate(features):
    with cols[i % 3]:
        if feat == "gender":
            gender = st.selectbox("Gender", ["Female", "Male"])
            gender_value = 0 if gender == "Female" else 1
            inputs.append(gender_value)
        else:
            placeholder = ""
            if feat == "age":
                placeholder = "Years"
            elif feat == "weight":
                placeholder = "Kilograms"
            elif feat == "height":
                placeholder = "Centimeters"

            value = st.text_input(feat.capitalize(), placeholder=placeholder)
            inputs.append(value)

# -------------------------------------------------
# Prediction
# -------------------------------------------------
if st.button("🔍 Predict"):
    try:
        # Validate non-gender fields
        non_gender_inputs = [
            inputs[i] for i, f in enumerate(features) if f != "gender"
        ]

        if any(val.strip() == "" for val in non_gender_inputs):
            st.error("Please fill in all the fields.")
        else:
            final_data = []
            for i, val in enumerate(inputs):
                if features[i] == "gender":
                    final_data.append(int(val))
                elif features[i] == "age":
                    final_data.append(int(val))
                else:
                    final_data.append(float(val))

            prediction = model.predict([final_data])[0]

            # Store ONLY what chatbot needs
            st.session_state["selected_disease"] = "Fatty Liver"
            st.session_state["prediction_result"] = prediction

    except ValueError:
        st.error("Please enter valid numeric values only.")

# -------------------------------------------------
# Result display (inline)
# -------------------------------------------------
if "prediction_result" in st.session_state and st.session_state.get("selected_disease") == "Fatty Liver":
    st.markdown("---")
    st.subheader("🧾 Prediction Result")

    if st.session_state["prediction_result"] == 1:
        st.error("🔴 Likely **Fatty Liver Disease**")
    else:
        st.success("🟢 Likely **No Fatty Liver Disease**")

    if st.button("💬 Talk to AI Assistant"):
        st.switch_page("pages/chatbot.py")

# -------------------------------------------------
# Navigation
# -------------------------------------------------
if st.button("🏠 Back to Home"):
    st.switch_page("app.py")
