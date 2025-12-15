import pandas as pd
import os

DATA_PATH = "data/reviews.csv"

def init_storage():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_PATH):
        df = pd.DataFrame(columns=[
            "timestamp",
            "rating",
            "review",
            "ai_response",
            "ai_summary",
            "ai_action"
        ])
        df.to_csv(DATA_PATH, index=False)

def save_entry(entry):
    df = pd.read_csv(DATA_PATH)
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

def load_entries():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)
