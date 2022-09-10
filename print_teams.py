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

if __name__ == "__main__":
    teams = get_active_teams()

    print("i\tAbbr\tID\tName")
    i = 1
    for abbr, t in teams.items():
        print(i, "\t", t.abbreviation, "\t", t.team_id, "\t", t.name)
        i = i + 1
