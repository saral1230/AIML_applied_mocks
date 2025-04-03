import pandas as pd
import numpy as np
from datetime import datetime, timedelta




def generate_synthetic_data(num_machines, days, samples_per_hour, failure_prob):


    # Time setup
    start_time = datetime.now() - timedelta(days=days)
    total_samples = days * 24 * samples_per_hour

    data = []

    for machine_id in range(1, num_machines + 1):
        for sample in range(total_samples):
            time = start_time + timedelta(minutes=10 * sample)

            # Basic normal sensor readings
            temp = np.random.normal(90, 5)
            pressure = np.random.normal(100, 10)
            vibration = np.random.normal(2, 0.5)

            # Decide if this point will be part of a degrading failure
            in_degradation_zone = sample > 0.7 * total_samples
            will_fail = np.random.rand() < failure_prob if in_degradation_zone else False

            # Apply degradation if failing
            if will_fail:
                progress = (sample - 0.7 * total_samples) / (0.3 * total_samples)
                temp += 20 * progress + np.random.normal(0, 1)
                pressure += 15 * progress + np.random.normal(0, 2)
                vibration += 1.5 * progress + np.random.normal(0, 0.2)

            # Inject random hard anomalies (optional, even in normal data)
            if np.random.rand() < 0.01:  # 1% chance
                temp += np.random.normal(30, 10)
                pressure += np.random.normal(25, 5)
                vibration += np.random.normal(3, 1)

            # Label failure (you can define a window for upcoming failure detection)
            failure = int(will_fail)

            data.append([
                machine_id,
                time,
                temp,
                pressure,
                vibration,
                failure
            ])

    columns=["machine_id", "timestamp", "temperature", "pressure", "vibration", "failure"]
    return pd.DataFrame(data, columns=columns)



if __name__ == "__main__":
    
    # --- Set Parameters ---
    n_machines = 3
    days_of_data = 30
    samples_per_hour = 6  # Every 10 minutes
    failure_prob = 0.10


    df = generate_synthetic_data(n_machines, days_of_data, samples_per_hour, failure_prob)

    # Save to CSV
    output_path="../data/synthetic_data.csv"
    df.to_csv(output_path, index=False)
    print("Synthetic data generated!")