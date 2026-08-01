import pandas as pd
import numpy as np
from scripts.utils import load_data, save_data

def build_results(df):

    df_matches = df[df["tournament_name"].str.contains("FIFA Men's World Cup",)].copy()
    
    df_matches = df_matches[["match_date", "home_team_name", "away_team_name", "home_team_win", "away_team_win", "draw"]].copy()

    # Add result
    df_matches["result"] = np.select(
        [
            df_matches["home_team_win"],
            df_matches["away_team_win"]
        ],
        [
            "Win",
            "Loss"
        ],
        default="Draw"
    )

    # Date to Year
    df_matches["year"] = (
        df_matches["match_date"]
        .str[:4]
        .astype(int)
    )
    df_matches = df_matches[["year", "home_team_name", "away_team_name", "result"]]


    # Add team confederation
    df_confederation = load_data("data/processed/confederations.csv")
    conf_map = df_confederation.set_index("team")["confederation"]

    df_matches["team_conf"] = df_matches["home_team_name"].map(conf_map)
    df_matches["opponent_conf"] = df_matches["away_team_name"].map(conf_map)

    df_matches.rename(columns={"home_team_name": "team", "away_team_name": "opponent_team"}, inplace=True)

    # Add another row per match but for the opponent_team
    home = df_matches.copy()

    away = df_matches.copy()

    away["team"] = df_matches["opponent_team"]
    away["opponent_team"] = df_matches["team"]

    away["team_conf"] = df_matches["opponent_conf"]
    away["opponent_conf"] = df_matches["team_conf"]

    away["result"] = away["result"].map({
        "Win": "Loss",
        "Loss": "Win",
        "Draw": "Draw"
    })

    df_matches_long = pd.concat(
        [home, away],
        ignore_index=True
    )

    return df_matches_long

def main():
    df = load_data("data/raw/matches_curated.csv")
    df = build_results(df)
    save_data(df, "data/processed/matches_long.csv")

if __name__ == "__main__":
    main()