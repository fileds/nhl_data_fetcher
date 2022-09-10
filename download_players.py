import os
from pprint import pprint
import json
import requests
import time
from datetime import datetime, date
import numpy as np
import pandas as pd

def download_player(player_id, verbose = True):
    # Downloading info
    url = ("https://statsapi.web.nhl.com/api/v1/people/"
            + str(player_id))
    try:
        info_json = requests.get(url).json()["people"][0]
        info_df = pd.DataFrame([info_json])
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
        seasons_json = requests.get(url).json()["stats"][0]["splits"]
        seasons_df_list = []
        for s in seasons_json:
            s["league"] = s["league"]["name"]
            s["team"] = s["team"]["name"]
            stat = s["stat"]
            s.pop("stat")
            s.update(stat)
            seasons_df_list.append(pd.DataFrame([s]))

        seasons_df = pd.concat(seasons_df_list)
    except:
        if verbose:
            print("\nERROR: Failed to get seasons stats for player id " +
                "{}.".format( player_id))
            print("Downloaded info for {}".format(info_json["fullName"]))

        return

    if verbose:
        print("Downloaded info and seasons stats for {}".format(
            info_json["fullName"]))

    dir_path = ("./data/player_data/" + info_json["fullName"] + "-"
                + str(info_json["id"]))
    if not os.path.isdir(dir_path): os.mkdir(dir_path)

    info_df.to_csv(dir_path + "/" + "info.csv", sep = ",")
    seasons_df.to_csv(dir_path + "/" + "seasons.csv", sep = ",")


if __name__ == "__main__":
    players = pd.read_csv("data/player_list.csv")
    for pid in players.id:
      download_player(pid)
