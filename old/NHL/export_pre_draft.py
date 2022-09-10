from pprint import pprint
from nhl_loading import load_all_players
from nhl_create_db import create_draft_df, write_df_to_csv
from nhl_utils import load_instructions, print_status

if __name__ == "__main__":
    instructions_path = "./instructions.json"
    players_dir, fpts_system = load_instructions(instructions_path,
            ["players_dir", "fantasy_point_system_path"])

    players = load_all_players(players_dir, load_seasons=True)

    cats = ["games"]
    years = ["20182019", "20192020", "20202021"]
    pos = ["F", "D"]
    for p in pos:
        path = "./data/fantasy_draft_db_{}.csv".format(p)
        df = create_draft_df(players, years, p, fpts_system, True)
        df.to_csv(path_or_buf=path, sep=";", decimal=",", index=False)
