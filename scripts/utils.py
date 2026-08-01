
import pandas as pd

def load_data(path):
    df = pd.read_csv(path)
    return df

def save_data(df, path):
    df.to_csv(path, index=False)
