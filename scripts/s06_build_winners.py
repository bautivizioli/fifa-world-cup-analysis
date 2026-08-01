import pandas as pd
from scripts.utils import load_data, save_data

def build_confederations(df):
    
    winners = df[df["tournament_name"].str.contains("FIFA Men's World Cup",)].copy()
    winners["year"] = winners["tournament_name"].str[0:4]
    winners = winners[["year", "team_name", "position"]]
    winners = winners.rename(columns={"team_name": "team"})
    
    return winners

def main():
    df = load_data("data/raw/tournament_standings_curated.csv")
    df = build_confederations(df)
    save_data(df, "data/processed/winners.csv")

if __name__ == "__main__":
    main()
