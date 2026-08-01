
import pandas as pd
from scripts.utils import load_data, save_data

def build_players_avg_age(df):
    df_players = df.copy()

    # Add avg_age (not per position)
    df_players["avg_age"] = (
        df_players
        .groupby(["year", "team"])["age"]
        .transform("mean")
    )

    # Group by pos
    df_players_age = (
        df_players
        .groupby(["year", "team", "position"], as_index=False)
        .agg(
            avg_age_p_pos=("age", "mean"),
            avg_age=("avg_age", "first")
        )
    )

    return df_players_age

def main():
    df = load_data("data/processed/players.csv")
    df = build_players_avg_age(df)
    save_data(df, "data/processed/players_avg_age.csv")

if __name__ == "__main__":
    main()
