import pandas as pd
from scripts.utils import load_data, save_data

def build_standings(df):
    # Filter only Men's WC
    df_team_matches = (
        df[
            df["tournament_name"].str.contains(
                "FIFA Men's World Cup",
                na=False
            )
        ]
        .copy()
    )

    # Extract year
    df_team_matches["year"] = (
        df_team_matches["tournament_name"]
        .str[:4]
        .astype(int)
    )

    # Old WC had different formats, so a mapping has to be done
    stage_rank = {
        "group stage": 1,
        "first group stage": 1,

        "second group stage": 2,
        "round of 16": 2,

        "quarter-finals": 3,

        "semi-finals": 4,
        "third-place match": 4,

        "final": 5,
        "final round": 5
    }

    df_team_matches["stage_score"] = (
        df_team_matches["stage_name"]
        .map(stage_rank)
    )

    # Obtain max stage reached
    df_team_stage = (
        df_team_matches
        .groupby(
            ["year", "team_name"],
            as_index=False
        )
        .agg(
            stage_score=("stage_score", "max")
        )
        .rename(columns={
            "team_name": "team"
        })
    )

    df_team_stage["final_position"] = (
        df_team_stage["stage_score"]
        .map({
            1: "Group Stage",
            2: "Round of 16",
            3: "Quarter-finals",
            4: "Semi-finals",
            5: "Final"
        })
    )

    df_team_stage = df_team_stage[["year", "team", "stage_score", "final_position"]].copy()

    return df_team_stage

def main():
    df = load_data("data/raw/team_appearances_curated.csv")
    df = build_standings(df)
    save_data(df, "data/processed/standings.csv")

if __name__ == "__main__":
    main()