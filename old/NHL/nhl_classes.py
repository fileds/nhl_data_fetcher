import os
import numpy as np
import json
from pprint import pprint
from datetime import datetime

from nhl_printing import print_season, print_fantasy_season
from nhl_utils import convert_time_stat

def convert_season_to_float(season):
    season["stat"]["games"] = int(season["stat"]["games"])
    for cat, score in season["stat"].items():
        if "TimeOn" in cat or "timeOn" in cat:
            season["stat"][cat] = convert_time_stat(score)
        else:
            season["stat"][cat] = float(score)

    return season

# Classes
class Team:
    def __init__(self,
                 name,
                 abbreviation,
                 team_id):
        self.info = {}
        self.info["name"] = name
        self.info["abbreviation"] = abbreviation
        self.info["id"] = team_id

    def get_name(self):
        return self.info["name"]

    def get_abbriviation(self):
        return self.info["abbriviation"]

    def get_id(self):
        return self.info["id"]

class Player:
    def __init__(self, player_path, load_seasons=False):
        self.has_float_stat = False
        self.has_fantasy_seasons = False
        self.has_prediction = False

        info_path = player_path + "info.json"
        with open(info_path, "r") as f:
            self.info = json.load(f)
        self.info["path"] = player_path

        if load_seasons:
            self.load_seasons()

    def is_active(self):
        if "active" in self.info:
            return bool(self.info["active"])

    def get_name(self):
        if "fullName" in self.info:
            return self.info["fullName"]
        else:
            return ""

    def get_id(self):
        if "id" in self.info:
            return int(self.info["id"])
        else:
            return 0

    def get_team_name(self):
        if "currentTeam" in self.info:
            return self.info["currentTeam"]["name"]
        else:
            return ""

    def get_team_id(self):
        if "currentTeam" in self.info:
            return int(self.info["currentTeam"]["id"])
        else:
            return ""

    def get_last_update(self):
        if "last_update" in self.info.keys():
            return datetime.strptime(self.info["last_update"], "%d/%m/%Y")
        else:
            return datetime.min

    def get_position_type(self):
        return self.info["primaryPosition"]["type"][0]

    def get_position_fantasy(self):
        p = self.info["primaryPosition"]["abbreviation"]
        if p == "RW" or p == "LW":
            return "W"
        else:
            return p

    def get_nhl_seasons(self):
        return seasons.keys()

    def get_season(self, year):
        if year in self.seasons.keys():
            return self.seasons[year]

    def get_fantasy_season(self, year):
        if year in self.seasons.keys():
            if "fantasy" in self.seasons[year].keys():
                return self.seasons[year]["fantasy"]

    def who_am_i(self, verbose=True):
        print("I am {}, id: {}, playing as a {} for the {}.".format(
            self.get_name(),
            self.get_id(),
            self.get_position_fantasy(),
            self.get_team_name()))


    def load_seasons(self, only_nhl=True):
        with open(self.info["path"] + "seasons.json", "r") as f:
            seasons_data = json.load(f)

        self.seasons = {}
        previous_season = ""
        for season in seasons_data:
            if season["league"]["name"] == "National Hockey League":
                # Check if player played for multiple teams
                if season["season"] == previous_season:
                    season_tmp = convert_season_to_float(season)
                    # Merge seasons in which player played for multiple teams
                    for cat, score in season_tmp["stat"].items():
                        if cat in self.seasons[season["season"]]["stat"]:
                            self.seasons[season["season"]]["stat"][cat] += (
                                    score)
                        else:
                            self.seasons[season["season"]]["stat"][cat] = score


                    # Update team. Store id and link for last team
                    teams = (self.seasons[season["season"]]["team"]["name"] +
                            "/" + season["team"]["name"])
                    self.seasons[season["season"]]["team"] = season["team"]
                    self.seasons[season["season"]]["team"]["name"] = teams
                else:
                    self.seasons[season["season"]] = (
                            convert_season_to_float(season))
                    previous_season = season["season"]

    def has_season(self, year):
        if year in self.seasons.keys():
            return True
        else:
            return False

    def season_has_fantasy(self, year):
        if "fantasy" in self.seasons[year].keys():
            return True
        else:
            return False

    def convert_season_to_fantasy(self, year, fantasy_point_system_path):
        with open(fantasy_point_system_path, "r") as f:
            point_system = json.load(f)

        season = self.seasons[year]

        season["fantasy"] = {}
        season["fantasy"]["games"] = season["stat"]["games"]

        tot_fpts = 0
        for cat, score in season["stat"].items():
            if cat in point_system.keys():
                self.seasons[year]["fantasy"][cat] = score
                conversion = float(point_system[cat])
                tot_fpts += conversion * float(score)

        avg_fpts = tot_fpts / float(
                self.seasons[year]["fantasy"]["games"])

        self.seasons[year]["fantasy"]["fptsTot"] = np.around(tot_fpts, 2)
        self.seasons[year]["fantasy"]["fptsAvg"] = np.around(avg_fpts, 2)

    def convert_all_seasons_to_fantasy(self, fantasy_point_system_path):
        for year, season in self.seasons.items():
            self.convert_season_to_fantasy(year, fantasy_point_system_path)

    def get_fantasy_points(self, year, fpts_system_path):
        if not self.season_has_fantasy(year):
            self.convert_season_to_fantasy(year, fpts_system_path)

        return [self.seasons[year]["fantasy"]["fptsTot"],
                self.seasons[year]["fantasy"]["fptsAvg"]]

    def get_fantasy_season_cat_list(self, year, cats,
            fpts_system_path):
        if not self.season_has_fantasy(year):
            self.convert_season_to_fantasy(year, fpts_system_path)

        cat_list = []
        for cat in cats:
            cat_list.append(self.seasons[year]["fantasy"][cat])

        return cat_list

    def get_season_cat_list(self, year, cats):
        cat_list = []
        for cat in cats:
            cat_list.append(self.seasons[year]["stat"][cat])

        return cat_list

    def print_seasons(self, years, print_all=False):
        print("\nPlayer: {}\n".format(self.info["fullName"]))
        if print_all or not years:
            for y, s in self.seasons.items():
                print_season(s)
                print("")
        else:
            for y in years:
                if y not in self.seasons.keys():
                    continue
                print_season(self.seasons[y])
                print("")

    def print_fantasy_season(self, year):
        pprint(self.fantasy_seasons[year])
