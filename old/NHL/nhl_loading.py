import os
from pprint import pprint
import pandas as pd

from nhl_classes import Player

def load_all_players(players_dir, load_seasons=False, verbose=False):
    # Getting player ids and paths
    players_in_db = [(d, (players_dir + d + "/")) for d in
            os.listdir(players_dir) if not d.startswith(".")]

    n_loaded = 0
    players = []
    for pid, path in players_in_db:
        player = Player(path)
        if load_seasons:
            player.load_seasons()
        players.append(player)

        n_loaded += 1

    if verbose:
        print("{} players loaded.".format(n_loaded))

    return players

# Description Loads a single player to RAM
#
# Note: Supply part of players name. If multiple instances with the same name
# exists, the first in the player list will be returned. Write exact name for
# exact player, altough naming might not be obvious. For an example PK Subban
# is named PK Subban.
#
# Input: part of player name, path to players directory, path to players list,
# verbose
#
# Output: player loaded as a player class object
#
def load_player(players_dir, token=" ", verbose=False):
    # Getting player ids and paths
    players_in_db = [(d, (players_dir + d + "/")) for d in
            os.listdir(players_dir) if not d.startswith(".")]

    if token is not " ":
        if verbose:
            print("Searching for player name containing {} ...".format(token),
                    end="")
        for i in range(0, len(players_in_db)):
            player = Player(players_in_db[i][1])
            if token in player.get_name():
                if verbose:
                    print("Found player {}.".format(player.get_name()))
                return player

    if verbose:
        print("\n\nError: Player not found.\n")
    return -1
