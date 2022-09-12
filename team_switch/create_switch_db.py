import numpy as np
import pandas as pd
import os
from pprint import pprint

def load_player_info(path):
    return pd.read_csv(path + "/info.csv")

def load_player_seasons(path):
    return pd.read_csv(path + "/seasons.csv")

def get_team_switches(path):
    idf = load_player_info(path)
    sdf = load_player_seasons(path)
    sdf = sdf[sdf["league"] == "National Hockey League"]
    if not sdf.empty:
        pprint(sdf)
        sdf["team_switch"] = (sdf["team"].shift(1, fill_value =
                sdf["team"].head(1)) != sdf["team"])
        pprint(sdf["team_switch"])




if __name__ == "__main__":
    data_dir = "/home/fileds/data/NHL/player_data/data/"
    player_dirs = os.listdir(data_dir)
    seasons = []
    for d in player_dirs:
        path = data_dir + d
        get_team_switches(path)
