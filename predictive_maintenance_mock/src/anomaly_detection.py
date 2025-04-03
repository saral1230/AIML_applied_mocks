import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

# One-Class SVM and Autoencoder were tested in Jupyter Notebook

def detect_anomalies(data_path):
    # Load data
    df = pd.read_csv(data_path)

    # Use only sensor readings (no labels for unsupervised learning)
    X = df[['temperature', 'pressure', 'vibration']]

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train Isolation Forest
    iso_forest = IsolationForest(
        n_estimators=1000,
        contamination=0.05,  # Expected % of anomalies
        random_state=42
    )
    iso_forest.fit(X_scaled)

    # Predict anomalies (-1 = anomaly, 1 = normal)
    iso_pred = iso_forest.predict(X_scaled)
    df['iso_forest_anomaly'] = np.where(iso_pred == -1, 1, 0)
    anomalies = df[df.iso_forest_anomaly == 1]
    return anomalies

if __name__ == "__main__":
    data_path = "../data/synthetic_data.csv"
    anomalies = detect_anomalies(data_path)
    print(anomalies)

