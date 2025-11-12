import time
import pandas as pd
from sklearn.ensemble import IsolationForest
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host=,
        database=,
        user=,
        password=
    )

def train_model(df):
    features = [
        "DL_Traffic_Volume_MB",
        "UL_Traffic_Volume_MB",
        "Avg_Active_User_LTE",
        "Avg_Connected_User_LTE",
        "DL_Cell_Throughput_kbpsKbps",
        "UL_Cell_Throughput_kbpsKbps"
    ]
    X = df[features].fillna(0)
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)
    return model

# --- Process CSV file 
def process_csv(file_path):
    print(f"\nNew file detected: {file_path}")
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} records from {os.path.basename(file_path)}")

    model = train_model(df)
    X = df[[
        "DL_Traffic_Volume_MB",
        "UL_Traffic_Volume_MB",
        "Avg_Active_User_LTE",
        "Avg_Connected_User_LTE",
        "DL_Cell_Throughput_kbpsKbps",
        "UL_Cell_Throughput_kbpsKbps"
    ]].fillna(0)

    df["anomaly_score"] = model.decision_function(X)
    df["Spike_Flag"] = model.predict(X)
    df["Spike_Flag"] = df["Spike_Flag"].apply(lambda x: 1 if x == -1 else 0)

    df["Spike_Severity_Score"] = df["anomaly_score"]
    df["Spike_Severity_Level"] = pd.cut(
        df["Spike_Severity_Score"],
        bins=[-float('inf'), -0.25, -0.15, 0],
        labels=["Severe Spike", "Moderate Spike", "Mild Spike"]
    ).astype(str)
    df["Spike_Severity_Level"] = df["Spike_Severity_Level"].fillna("Normal")

    con = get_connection()
    cursor = con.cursor()
    insert_query = """
    INSERT INTO lte_spike_detection (
        time, cell_name, metric_name, metric_value,
        is_spike, model_name, score, severity_score, severity_level
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    spike_rows = df[df["Spike_Flag"] == 1]
    print(f"Inserting {len(spike_rows)} spikes into database...")

    for _, row in spike_rows.iterrows():
        cursor.execute(insert_query, (
            row.get("Time"),
            row.get("Cell_Name"),
            "Total_Traffic_MB",
            row.get("DL_Traffic_Volume_MB"),
            True,
            "IsolationForest",
            row.get("Spike_Flag"),
            float(row.get("Spike_Severity_Score", 0)),
            row.get("Spike_Severity_Level")
        ))

    con.commit()
    cursor.close()
    con.close()
    print(f"Done! Inserted {len(spike_rows)} spike records.\n")

class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".csv"):
            process_csv(event.src_path)

if __name__ == "__main__":
    watch_folder = "/home/my/Desktop/lte-spike-detection/new_data"
    print(f"Watching folder: {watch_folder}")

    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_folder, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
