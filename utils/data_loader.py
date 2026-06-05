import pandas as pd
from config import DATA_PATH


def load_data():
    df = pd.read_csv(DATA_PATH)

    df["last_update"] = pd.to_datetime(
        df["last_update"],
        errors="coerce"
    )

    return df