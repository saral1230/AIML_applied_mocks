from fastapi import FastAPI
import joblib

app = FastAPI()
model = joblib.load("../data/trained_models/xgboost_model.pkl")  # Load model

@app.post("/predict_failure")
def predict(temperature: float, pressure: float, vibration: float):
    prediction = model.predict([[temperature, pressure, vibration]])
    return {"failure_risk": bool(prediction[0])}