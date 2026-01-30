# equipment/utils.py
import pandas as pd

def analyze_csv(file):
    df = pd.read_csv(file)

    return {
        "total_equipment": len(df),
        "avg_flowrate": df["Flowrate"].mean(),
        "avg_pressure": df["Pressure"].mean(),
        "avg_temperature": df["Temperature"].mean(),
        "type_distribution": df["Type"].value_counts().to_dict()
    }
