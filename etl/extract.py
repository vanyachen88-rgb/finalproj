import pandas as pd
from pathlib import Path

RAW_PATH = Path("C:/Project/finalproj/data/raw")

TABLES = [
    "Dim_Date",
    "Customers",
    "Marketing_Campaigns",
    "Leads",
    "Machines",
    "Rentals",
    "Payments",
    "Maintenance"
]

def extract_data():
    data = {}

    for table in TABLES:
        file_path = RAW_PATH / f"{table}.csv"

        df = pd.read_csv(file_path)
        data[table] = df

        print(f"{table}: {df.shape}")

    return data