import sys
from pprint import pprint

from nhl_utils import load_instructions, add_instruction, print_status
from nhl_classes import Team, Player
from nhl_loading import load_player

if __name__ == "__main__":
    token = sys.argv[1]

    instructions_path = "./instructions.json"
    players_dir = load_instructions(instructions_path, "players_dir")

    player = load_player(players_dir, token, verbose=True)

    if player == -1:
        print("Player not found")
        exit()
    else:
        player.who_am_i()
        print("ID: {}".format(player.get_id()))

    # years = ["20162017", "20172018", "20182019", "20192020"]
    # years = []
    # player.load_seasons()
    # player.print_seasons(years)
