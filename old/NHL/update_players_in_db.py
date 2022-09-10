import os

from nhl_download import *
from nhl_classes import Player
from nhl_utils import load_instructions, add_instruction, print_status

def update_players_in_db(players_dir, threshold=1, verbose=False):
    # Getting player ids and paths
    players_in_db = [(d, (players_dir + d + "/")) for d in
            os.listdir(players_dir) if not d.startswith(".")]

    n_players_in_db = len(players_in_db)
    n_processed = 0
    n_updated = 0
    if verbose:
        print(" ")
    for pid, path in players_in_db:
        player = Player(path)
        if abs((datetime.now() - player.get_last_update()).days) > threshold:
            download_player(pid, players_dir, False)
            n_updated += 1

        n_processed += 1
        if verbose:
            print_status(n_processed, n_players_in_db)

    if verbose:
        print("\n{} players out of {} updated.\n".format(n_updated,
            n_players_in_db))

if __name__ == "__main__":
    instructions_path = "./instructions.json"
    players_dir = load_instructions(instructions_path, "players_dir")
    update_players_in_db(players_dir, 1, True)
