import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_penalty_shoot-outs"

HEADERS = {
    "User-Agent": (
        "wc-analysis/1.0 "
        "(Academic research project; Python Requests)"
    ),
    "Accept": "text/html",
    "Accept-Language": "en-US,en;q=0.9",
}


def _parse_penalties(cell, year, round_, winner, loser, team):
    records = []

    penalties = cell.find_all(
        "span",
        class_="nowrap",
        recursive=False,
    )

    for order, penalty in enumerate(penalties, start=1):

        player = penalty.find("a")
        if player is None:
            continue

        icon = penalty.find("span", title=True)
        if icon is None:
            continue

        records.append(
            {
                "year": year,
                "round": round_,
                "winner": winner,
                "loser": loser,
                "team": team,
                "taker": player.get_text(strip=True),
                "penalty_order": order,
                "scored": icon["title"] == "Penalty scored",
                "first_taker": (
                    penalty.find(
                        "span",
                        style=lambda s: s and "#C3C3C3" in s,
                    )
                    is not None
                ),
            }
        )

    return records


def scrape_penalty_shootouts():
    """Scrape FIFA World Cup penalty shoot-outs from Wikipedia."""

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="wikitable")

    records = []

    current_year = None
    current_round = None

    for row in table.find_all("tr")[2:]:

        cells = row.find_all("td")

        if len(cells) == 16:

            current_year = int(cells[0].get_text(strip=True)[:4])
            current_round = cells[1].get_text(strip=True)

            winner = cells[2].get_text(strip=True)
            loser = cells[4].get_text(strip=True)

            winner_cell = cells[9]
            loser_cell = cells[10]

        elif len(cells) == 15:

            current_round = cells[0].get_text(strip=True)

            winner = cells[1].get_text(strip=True)
            loser = cells[3].get_text(strip=True)

            winner_cell = cells[8]
            loser_cell = cells[9]

        elif len(cells) == 14:

            winner = cells[0].get_text(strip=True)
            loser = cells[2].get_text(strip=True)

            winner_cell = cells[7]
            loser_cell = cells[8]

        else:
            continue

        records.extend(
            _parse_penalties(
                winner_cell,
                current_year,
                current_round,
                winner,
                loser,
                winner,
            )
        )

        records.extend(
            _parse_penalties(
                loser_cell,
                current_year,
                current_round,
                winner,
                loser,
                loser,
            )
        )

    return pd.DataFrame(records)


def main():
    df = scrape_penalty_shootouts()
    df.to_csv(
        "data/processed/penalty_shootouts.csv",
        index=False,
    )


if __name__ == "__main__":
    main()