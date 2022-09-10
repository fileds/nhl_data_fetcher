import numpy as np
from pprint import pprint
from nhl_classes import Player
import pandas as pd

def write_df_to_csv(df, path, verbose=False):
    if verbose:
        print("Writing player database to", path)
    df.to_csv(path_or_buf=path, sep=";", decimal=",", index=False)

    if verbose:
        print("Done\n")

def create_fantasy_df(players, year, pos, cats, fpts_system, verbose=False):
    if verbose:
        print("Creating fantasy DataFrame with positions {} ...".format(pos),
                end="\t")

    df = pd.DataFrame(columns = ["name", "pos", "fpts", "fptsAvg", *cats])

    for i, player in enumerate(players):
        if player.has_season(year):
            player_pos = player.get_position_fantasy()
            if player_pos in pos:
                player_name = player.get_name()
                df.loc[i] = [player_name, player_pos,
                        *player.get_fantasy_points(year, fpts_system),
                        *player.get_season_cat_list(year, cats)]

    if verbose:
        print("Done\n")

    return df

def create_draft_df(players, years, pos, fpts_system, verbose=False):
    if verbose:
        print("Creating fantasy DataFrame with positions {} ...".format(pos),
                end="\t")

    active_teams = pd.read_csv("data/active_teams.csv", delimiter=";",
            skiprows=1)
    pprint(active_teams)

    years = ["20182019", "20192020", "20202021"]

    df = pd.DataFrame(columns = ["name", "pos", "team", "fpts1819",
        "fptsAvg1819", "fpts1920", "fptsAvg1920", "fpts2021", "fptsAvg2021",
        "fptsCumAvg", "fptsAvgCumAvg", "fptsWeighted", "avgWeighted"])


    for i, player in enumerate(players):
        n_seasons = 0
        fpts_3_yr = 0
        avg_3_yr = 0
        fpts = []
        avg = []
        player_pos = player.get_position_type()
        if player_pos == pos:
            player_name = player.get_name()
            player_fantasy_pos = player.get_position_fantasy()
            try:
                player_team = active_teams.loc[lambda active_teams:
                        active_teams["name"] ==
                        player.get_team_name()].values[0][2]
            except:
                player_team = "???"
            for year in years:
                if player.has_season(year):
                    fs = player.get_fantasy_points(year, fpts_system)
                    fpts.append(fs[0])
                    avg.append(fs[1])
                    fpts_3_yr += fs[0]
                    avg_3_yr += fs[1]
                    n_seasons += 1
                else:
                    fpts.append(0)
                    avg.append(0)
            if n_seasons > 0:
                fpts_3_yr = np.around(fpts_3_yr / n_seasons, 2)
                avg_3_yr = np.around(avg_3_yr / n_seasons, 2)
                fpts_weighted = 0
                avg_weighted = 0

                if fpts_3_yr > 100 or fpts[2] > (130 / 82) * 56:
                    numerator = 0
                    for j in [0, 1, 2]:
                        if fpts[j] > 10:
                            avg_weighted += (j+1) * avg[j]
                            numerator += j+1
                    if numerator < 6:
                        fpts_weighted = 0
                        avg_weighted = 0

                    fpts_weighted /= numerator
                    avg_weighted /= numerator
                    fpts_weighted = np.around(fpts_weighted, 2)
                    avg_weighted = np.around(avg_weighted, 2)

                    df.loc[i] = [player_name,
                                 player_fantasy_pos,
                                 player_team,
                                 float(fpts[0]),
                                 float(avg[0]),
                                 float(fpts[1]),
                                 float(avg[1]),
                                 float(fpts[2]),
                                 float(avg[2]),
                                 float(fpts_3_yr),
                                 float(avg_3_yr),
                                 float(fpts_weighted),
                                 float(avg_weighted)]

    if verbose:
        print("Done\n")

    return df
