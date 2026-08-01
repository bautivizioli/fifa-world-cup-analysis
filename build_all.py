from scripts.s01_build_players import main as build_players
from scripts.s02_build_players_avg_age import main as build_players_avg_age
from scripts.s03_build_standings import main as build_standings
from scripts.s04_build_confederations import main as build_confederations
from scripts.s05_build_matches_results import main as build_matches_results
from scripts.s06_build_winners import main as build_winners
from scripts.scrap_penalty_shootouts import main as scrap_penalty_shootouts

def main():
    build_players()
    build_players_avg_age()
    build_standings()
    build_confederations()
    build_matches_results()
    build_winners()
    scrap_penalty_shootouts()
    
if __name__ == "__main__":
    main()