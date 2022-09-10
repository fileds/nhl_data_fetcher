# from pprint import pprint
import json
import requests
# import time

class Player:
    def __init__(self, pid, name):
        self.id = pid
        self.name = name


n_teams = 32
players = []
ntp = 1
i = 1
while ntp < n_teams:
    url = ("https://statsapi.web.nhl.com/api/v1/teams/" + str(i)
        + "?expand=team.roster")
    data = requests.get(url).json()
    if data["teams"][0]["active"]:
        print("Processing ", data["teams"][0]["abbreviation"])
        for p in data["teams"][0]["roster"]["roster"]:
            players.append(Player(p["person"]["id"], p["person"]["fullName"]))

        ntp = ntp + 1
    i += 1

with open("data/player_list.csv", "w") as file:
    file.write("name,id\n")
    for p in players:
        file.write(p.name + "," + str(p.id) + "\n")
