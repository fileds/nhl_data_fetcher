from pprint import pprint
import json
import requests
import time

class Team:
    roster = []

    def __init__(self, name, abbreviation, tid):
        self.name = name
        self.abbreviation = abbreviation
        self.id = tid

class Player:
    def __init__(self, pid, name):
        self.id = pid
        self.name = name


response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/1?expand=team.roster")
data = response.json()

# pprint(data["teams"]["roster"]["roster"])

def team_is_active(data):
    if data["teams"][0]["active"]:
        return True
    else:
        return False

n_teams = 2
teams = {}
players = []
i = 1
while len(teams) < 31:
    url = ("https://statsapi.web.nhl.com/api/v1/teams/" + str(i)
        + "?expand=team.roster")
    team_data = requests.get(url).json()
    team_abbreviation = team_data["teams"][0]["abbreviation"]
    team_name = (team_data["teams"][0]["shortName"] + " " +
            team_data["teams"][0]["teamName"])
    team_id = team_data["teams"][0]["id"]
    print(team_name)
    if team_is_active(team_data):
        teams[team_abbreviation] = Team(team_abbreviation, team_name, team_id)
        print("is active\n")
        for p in team_data["teams"][0]["roster"]["roster"]:
            teams[team_abbreviation].roster.append(p["person"]["fullName"])
            players.append(Player(p["person"]["id"], p["person"]["fullName"]))

    i = i + 1
    time.sleep(1)

for name, team in teams.items():
    print(team.abbreviation)
    for p in team.roster:
        print("\t", p)

print("Number of players: ", len(players))

print("Teams:")
for name, team in teams.items():
    print(team.abbreviation)
