import os
from pprint import pprint
import json
import requests
import time
from datetime import datetime, date
import pandas as pd

from nhl_utils import load_instructions, add_instruction, print_status
from nhl_classes import Team

# Description: Writes data to a file in a player directory
#
# Note:
#
# Input:
#
# Output:
#
def write_player_data(players_dir, player_id, data, file_name):
    newpath = players_dir + str(player_id) + "/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    with open(newpath + file_name, "w+") as f:
        json.dump(data, f, indent=4)

# Description: Gets current active teams in the nhl
#
# Note:
#
# Input:
#
# Output: List of active teams
#
def download_active_teams(verbose=False):
    teams = {}

    url = "https://statsapi.web.nhl.com/api/v1/teams"
    data = requests.get(url).json()

    for team in data["teams"]:
        # if team["active"]:
        new_team = Team(team["name"],
                        team["abbreviation"],
                        team["id"])
        teams[new_team.info["abbreviation"]] = new_team

    return teams

# Description: Downloads player info and season stats and stores the
# information in a folder with the player ID as its name.
#
# Note:
#
# Input: Player ID in NHL API, path to players directory
#
# Output: -
#
def download_player(player_id, players_dir, verbose=False):
    # Downloading info
    url = ("https://statsapi.web.nhl.com/api/v1/people/"
            + str(player_id))
    try:
        player_info = requests.get(url).json()["people"][0]
        # Adding update date to player info
        player_info["last_update"] = date.today().strftime("%d/%m/%Y")
        # Writing files to directory
        write_player_data(players_dir, player_id, player_info,
                "info.json")
    except:
        if verbose:
            print("\nERROR: Failed to get info for player id {}.".format(
                player_id))
            print("ERROR: Aborting player download.\n")
        return

    # Downloading season stats
    url = ("https://statsapi.web.nhl.com/api/v1/people/" +
            str(player_id) +
            "/stats?expand=person.stats&stats=yearByYear")
    try:
        seasons = requests.get(url).json()["stats"][0]["splits"]
        write_player_data(players_dir, player_id, seasons, "seasons.json")
    except:
        if verbose:
            print("\nERROR: Failed to get seasons stats for player id " +
                "{}.".format( player_id))
            print("Downloaded info for {}".format(player_info["fullName"]))

        return

    if verbose:
        print("Downloaded info and seasons stats for {}".format(
            player_info["fullName"]))

# Description: Checks if a player is already stored in data folder
#
# Note:
#
# Input: Player ID in NHL API, path to players directory
#
# Output: -
#
def player_in_db(player_id, players_dir, verbose=False):
    player_dir = players_dir + str(player_id)
    player_info_file = player_dir + "/info.json"
    player_seasons_file = player_dir + "/seasons.json"

    if os.path.exists(player_dir):
        return True
    else:
        return False
