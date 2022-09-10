import json
import requests

from nhl_download import *

# Description: Downloading players from active teams rosters. Saves a csv file
# containing all id, name, and team abbreviation for all downloaded players.
#
# Note: Does not include unsigned players.
#
# Input: path to instructions.json, data directory, player directory, teams
# dictionary, delay for delaying pinging the nhl website
#
# Output:
#
def download_rostered_players(players_dir, delay=1, verbose=False):
    teams = download_active_teams(verbose)

    n_teams = len(teams)
    n_done = 0
    n_downloaded_players = 0
    if verbose:
        print("Downloading rostered players from {} teams.".format(n_teams))
    for team in teams.values():
        url = ("https://statsapi.web.nhl.com/api/v1/teams/" +
                str(team.get_id()) + "?expand=team.roster")
        team_data = requests.get(url).json()

        for player in team_data["teams"][0]["roster"]["roster"]:
            player_id = player["person"]["id"]
            if not player_in_db:
                download_player(player_id, players_dir, verbose)
                n_downloaded_players += 1

        n_done += 1
        if verbose:
            print_status(n_done, n_teams)

        if delay:
            time.sleep(delay)

    if verbose:
        print("\nFinished downloading {} rostered players for {} teams".format(
            n_downloaded_players, n_teams))

if __name__ == "__main__":
    instructions_path = "./instructions.json"
    players_dir = load_instructions(instructions_path, "players_dir")
    delay = 0
    verbose = True
    download_rostered_players(players_dir, delay, verbose)
