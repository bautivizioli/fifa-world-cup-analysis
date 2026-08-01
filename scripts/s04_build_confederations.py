import pandas as pd
from scripts.utils import load_data, save_data

def build_confederations(df):
    df_confederation = df[["team_name", "confederation_code"]].copy()
    df_confederation = df_confederation.rename(columns={"team_name": "team", "confederation_code": "confederation"})

    return df_confederation

def main():
    df = load_data("data/raw/teams_curated.csv")
    df = build_confederations(df)
    save_data(df, "data/processed/confederations.csv")

if __name__ == "__main__":
    main()
