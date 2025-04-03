import streamlit as st
import pandas as pd
import joblib

# Load model and feature list
model = joblib.load("../src/rf_batch_classifier.pkl")
features = joblib.load("../src/model_features.joblib")

st.title("Batch Pass/Fail Prediction Dashboard")

# --- Sidebar Inputs ---
st.sidebar.header("Batch Input Features")

user_input = {}
for feature in features:
    user_input[feature] = st.sidebar.number_input(
        f"{feature}", value=0.0, format="%.2f"
    )

# Convert input to DataFrame
input_df = pd.DataFrame([user_input])

# --- Prediction ---
if st.button("Predict Batch Status"):
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)[0]

    st.subheader("Prediction Result")
    if prediction == 0:
        st.success(f"✅ Likely to Pass (Confidence: {prediction_proba[0]*100:.2f}%)")
    else:
        st.error(f"❌ Likely to Fail (Confidence: {prediction_proba[1]*100:.2f}%)")

    # Optional: show probability chart
    st.subheader("Prediction Probability")
    st.bar_chart({"Pass": prediction_proba[0], "Fail": prediction_proba[1]})
