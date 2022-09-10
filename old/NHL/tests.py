import unittest

import os

from nhl_classes import Player
import nhl_download
import nhl_loading

class TestingDownloading(unittest.TestCase):
    def test_download_active_teams(self):
        teams = nhl_download.download_active_teams()
        self.assertEqual(len(teams), 32)

    def test_download_player(self):
        # Testing downloading player info and season stats
        player_id = 8465009 # Player ID for Zdeno Chara
        players_dir = "./test_data/players/"

        nhl_download.download_player(player_id, players_dir, True)

        # Variables to test
        player_dir = players_dir + str(player_id)
        player_info_file = player_dir + "/info.json"
        player_seasons_file = player_dir + "/seasons.json"

        self.assertTrue(os.path.exists(player_dir))
        self.assertTrue(os.path.isfile(player_seasons_file))

    def test_player_in_db(self):
        player_id = 8465009 # Player ID for Zdeno Chara
        players_dir = "./test_data/players/"

        self.assertTrue(nhl_download.player_in_db(player_id, players_dir))
        self.assertFalse(nhl_download.player_in_db(0, players_dir))

    def test_load_all_players_n_players(self):
        players_dir = "./test_data/players/"

        n_players = len([(d, (players_dir + d + "/")) for d in
                os.listdir(players_dir) if not d.startswith(".")])

        players = nhl_loading.load_all_players(players_dir)

        self.assertEqual(n_players, len(players))

    def test_load_player_name(self):
        token = "Zdeno"  # Player ID for Zdeno Chara
        players_dir = "./test_data/players/"

        player = nhl_loading.load_player(players_dir, token=token, verbose=True)
        name = player.get_name()

        self.assertEqual(name, "Zdeno Chara")

    def test_load_player_wrong_name(self):
        token = "zdino"  # Player ID for Zdeno Chara
        players_dir = "./test_data/players/"

        player = nhl_loading.load_player(players_dir, token=token, verbose=True)

        self.assertEqual(player, -1)


unittest.main()
