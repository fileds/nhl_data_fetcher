from pprint import pprint
import json
import requests
import time
import pandas as pd


# Classes
class Team:
    roster = {}

    def __init__(self,
                 name,
                 abbreviation,
                 team_id):
        self.name = name
        self.abbreviation = abbreviation
        self.team_id = team_id

class Player:
    def __init__(self,
                 player_id,
                 name,
                 pos_general,
                 pos_specific,
                 pos_abbreviation,
                 team,
                 link):
        self.player_id = player_id
        self.name = name
        self.pos_general = pos_general
        self.pos_specific = pos_specific
        self.pos_abbreviation = pos_abbreviation
        self.team = team
        self.link = link

    def as_list(self):
        return [self.player_id,
                self.name,
                self.team,
                self.pos_abbreviation,
                self.pos_general,
                self.pos_specific,
                self.link]

    def as_list_for_fantasy(self):
        return [self.name,
                self.pos_general[0],
                self.team]

# Functions
def get_active_teams():
    teams = {}

    url = "https://statsapi.web.nhl.com/api/v1/teams"
    data = requests.get(url).json()

    for team in data["teams"]:
        new_team = Team(team["name"],
                        team["abbreviation"],
                        team["id"])
        teams[new_team.abbreviation] = new_team

    return teams

def download_rosters(teams, verbose=False):
    players = []
    i = 1
    for abbr, team in teams.items():
        url = ("https://statsapi.web.nhl.com/api/v1/teams/" + str(team.team_id)
            + "?expand=team.roster")
        if verbose:
            print("Downloading ", team.name, "...", end = "\t")

        for p in team_data["teams"][0]["roster"]["roster"]:
            player_id = p["person"]["id"]
            player_name = p["person"]["fullName"]
            player_pos_general = p["position"]["type"]
            player_pos_specific = p["position"]["name"]
            player_pos_abbreviation = p["position"]["abbreviation"]
            player_team = team.name
            player_link = p["person"]["link"]
            new_player = Player(player_id,
                    player_name,
                    player_pos_general,
                    player_pos_specific,
                    player_pos_abbreviation,
                    player_team,
                    player_link)
            players.append(new_player)

            teams.roster[player_id] = new_player

        if verbose:
            print("Done")

        time.sleep(1)

    if verbose:
        print("Finished downloading players for", len(teams), "teams\n")

    return (players)

def create_players_df(players, for_fantasy=False, verbose=False):
    if verbose:
        print("Creating player DataFrame...", path, end="\t")

    if for_fantasy:
        df = pd.DataFrame(columns = ["Name", "Pos", "Team"])
    else:
        df = pd.DataFrame(columns = ["id", "name", "team", "pos_a",
            "pos_g", "pos_s", "link"])

    for i, p in enumerate(players):
        if for_fantasy:
            df.loc[i] = p.as_list_for_fantasy()
        else:
            df.loc[i] = p.as_list()

    if verbose:
        print("Done\n")

    return df

def print_player_df_to_csv(df, path, verbose=False):
    if verbose:
        print("Writing player database to", path, end="\t")
    df.to_csv(path_or_buf=path, sep=";", index=False)

    if verbose:
        print("Done\n")

if __name__ == "__main__":
    path = "./data/player_db.csv"
    teams = get_active_teams()
    players = download_rosters(teams, verbose=True)

    df = create_players_df(players, verbose=True)
    print_player_df_to_csv(df, path, verbose=True)

    # For fantasy
    fantasy_path = "./data/fantasy_player_db.csv"
    df_fantasy = create_players_df(players, for_fantasy=True, verbose=True)
    print_player_df_to_csv(df_fantasy, fantasy_path, verbose=True)
