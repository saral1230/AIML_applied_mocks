import pandas as pd
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import joblib

# Jupyter Notebook select_classifier.ipynb explored Random Forest and A/B test simulation

def train_and_save_model(data_path):
    df = pd.read_csv(data_path)
    X, y = df[["temperature", "pressure", "vibration"]], df["failure"]
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model = XGBClassifier()
    model.fit(X_train, y_train)
    joblib.dump(model, "../data/trained_models/xgboost_model.pkl")



if __name__ == "__main__":
    data_path ="../data/synthetic_data.csv"
    train_and_save_model(data_path)

    print("✅ Trained and saved a model.")