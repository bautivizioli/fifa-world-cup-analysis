import pandas as pd
import numpy as np
from scripts.utils import load_data, save_data

def build_players(df):
    df_players = df[df["male"]==True]
    df_players = df_players[["family_name", "player_id", "birth_date", "goal_keeper", "defender", "midfielder", "forward", "list_tournaments"]]

    # Split players who played more than one tournament
    df_players["list_tournaments"] = df_players["list_tournaments"].str.split(", ")
    df_players = df_players.explode("list_tournaments")
    df_players["list_tournaments"] = df_players["list_tournaments"].astype(int)

    # Get player age at WC
    df_players['birth_date'] = pd.to_datetime(df_players['birth_date'])

    df_players["age"] = df_players["list_tournaments"] - df_players["birth_date"].dt.year
    df_players = df_players.drop('birth_date', axis=1)

    # Add team to players
    df_squads = load_data("data/raw/squads_curated.csv")

    df_players = df_players.merge(df_squads[["player_id", "team_name"]], on="player_id")

    # Transform position into one column
    # Some players (7%) have more then one position in the same world cup, so it will be assigned according the this hierarchy: Goalkeeper > Defender > Midfielder > Forward
    position_cols = [
        "goal_keeper",
        "defender",
        "midfielder",
        "forward"
    ]

    multi_position_players = df_players[
        df_players[position_cols].sum(axis=1) > 1
    ]

    df_players["position"] = np.select(
        [
            df_players["goal_keeper"],
            df_players["defender"],
            df_players["midfielder"],
            df_players["forward"],
        ],
        [
            "Goalkeeper",
            "Defender",
            "Midfielder",
            "Forward",
        ],
        default="Unknown"
    )

    df_players = df_players.drop_duplicates()

    df_players = df_players.rename(columns={"list_tournaments": "year", "team_name": "team"})

    df_players = df_players[["player_id", "year", "team", "position", "age"]]

    return df_players

def main():
    df = load_data("data/raw/players_curated.csv")
    df = build_players(df)
    save_data(df, "data/processed/players.csv")

if __name__ == "__main__":
    main()
