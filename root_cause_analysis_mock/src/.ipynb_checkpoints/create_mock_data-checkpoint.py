import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# Simulate BatchRecord
def create_batchreord(batch_ids, products, status_choices, defect_types):


    batch_data = []
    for batch_id in batch_ids:
        start_time = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 60), hours=random.randint(5, 9))
        end_time = start_time + timedelta(hours=random.randint(4, 12))
        status = random.choices(status_choices, weights=[0.7, 0.3])[0]
        defect = random.choice(defect_types) if status == "Fail" else None
        batch_data.append([
            batch_id, random.choice(products), start_time, end_time,
            f"OP_{random.randint(1, 5)}", f"EQ_{random.randint(1, 3)}",
            status, defect, random.randint(1, 5) if defect else None])

    columns=[
        "batch_id", "product_id", "start_time", "end_time", "operator_id",
        "equipment_id", "status", "defect_type", "defect_severity"
        ]
    return pd.DataFrame(batch_data, columns=columns)

# Simulate ProcessData
def create_process_data(batch_df, process_steps, parameters, readings_per_param):

    process_data = []
    for _, row in batch_df.iterrows():
        batch_id = row["batch_id"]
        start_time = row["start_time"]
        end_time = row["end_time"]

        total_intervals = len(process_steps) * len(parameters) * readings_per_param
        time_delta = (end_time - start_time) / total_intervals
        current_time = start_time

        for step in process_steps:
            for param in parameters:
                for _ in range(readings_per_param):
                    # Generate parameter value based on type
                    if param == "Temperature":
                        value = round(np.random.normal(37, 2), 2)
                    elif param == "pH":
                        value = round(np.random.normal(7, 0.5), 2)
                    elif param == "Pressure":
                        value = round(np.random.normal(1.0, 0.1), 2)

                    # Append process record with timestamp in order
                    process_data.append([
                        batch_id, step, param, value, current_time
                    ])
                    current_time += time_delta

    columns=[
        "batch_id", "step_name", "parameter_name", "parameter_value", "timestamp"
    ]
    return pd.DataFrame(process_data, columns=columns)

# Simulate QCResults
def create_qc_data(batch_ids, qc_tests):
    qc_data = []
    for batch_id in batch_ids:
        for test in qc_tests:
            result = round(np.random.normal(95, 2), 2) if test == "API Concentration" else (
                     round(np.random.normal(0.5, 0.2), 2) if test == "Impurity" else
                     random.choice(["Pass", "Fail"]))
            spec_min, spec_max = (90, 100) if test == "API Concentration" else (
                                 (0.0, 1.0) if test == "Impurity" else (None, None))
            unit = "%" if test in ["API Concentration", "Impurity"] else "Result"
            pass_fail = (spec_min <= result <= spec_max) if isinstance(result, float) else (result == "Pass")
            qc_data.append([
                batch_id, test, result, spec_min, spec_max, unit, pass_fail
            ])

    columns=[
        "batch_id", "test_name", "test_result", "spec_min", "spec_max", "test_unit", "pass_fail"
    ]
    return pd.DataFrame(qc_data, columns=columns)

# Simulate QAEvents
def create_qaevents(batch_ids):
    qa_events = []
    for batch_id in random.sample(batch_ids, 10):  # only some batches have QA events
        qa_events.append([
            batch_id, random.choice(["Deviation", "CAPA", "Audit Finding"]),
            "Description of QA event", datetime.now() - timedelta(days=random.randint(0, 30)),
            random.randint(1, 5)
        ])

    columns=[
        "batch_id", "event_type", "description", "event_time", "severity"
    ]
    return pd.DataFrame(qa_events, columns=columns)

# Simulate SupplyChainInfo

def create_supply_data(batch_ids, materials, suppliers):
    supply_data = []
    for batch_id in batch_ids:
        for material in materials:
            supply_data.append([
                batch_id, material, random.choice(suppliers),
                f"LOT_{random.randint(100, 999)}",
                datetime(2023, 1, 1) + timedelta(days=random.randint(0, 30)),
                random.choice(["Room Temp", "Refrigerated"]),
                round(np.random.uniform(80, 100), 1)
            ])

    columns=[
        "batch_id", "material_name", "supplier_id", "lot_number",
        "delivery_date", "storage_condition", "material_quality_score"
    ]
    return pd.DataFrame(supply_data, columns=columns)

if __name__ == "__main__":
    batch_ids = [f"BATCH_{i:03d}" for i in range(1, 51)]
    products = ["Product_A", "Product_B"]
    defect_types = [None, "pH Out-of-Spec", "Low Yield", "Contamination"]
    status_choices = ["Pass", "Fail"]

    batch_df = create_batchreord(batch_ids, products, status_choices, defect_types)
    batch_df.to_csv("BatchRecord.csv", index=False)

    process_steps = ["Mixing", "Heating", "Cooling"]
    parameters = ["Temperature", "pH", "Pressure"]
    readings_per_param = 3

    process_df = create_process_data(batch_df, process_steps, parameters, readings_per_param)
    process_df.to_csv("ProcessData.csv", index=False)

    qc_tests = ["API Concentration", "Impurity", "Sterility"]
    qc_df = create_qc_data(batch_ids, qc_tests)
    qc_df.to_csv("QCResults.csv", index=False)

    qa_df = create_qaevents(batch_ids)
    qa_df.to_csv("QAEvents.csv", index=False)

    materials = ["API", "Solvent", "Excipient"]
    suppliers = ["Supplier_X", "Supplier_Y", "Supplier_Z"]

    supply_df = create_supply_data(batch_ids, materials, suppliers)
    supply_df.to_csv("SupplyChainInfo.csv", index=False)

