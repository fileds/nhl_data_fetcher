from nhl_loading import load_all_players
from nhl_create_db import create_fantasy_df, write_df_to_csv
from nhl_utils import load_instructions, print_status

if __name__ == "__main__":
    instructions_path = "./instructions.json"
    players_dir, fpts_system = load_instructions(instructions_path,
            ["players_dir", "fantasy_point_system_path"])

    players = load_all_players(players_dir, load_seasons=True)

    current_year = "20202021"
    pos = ["D"]
    cats = ["games", "goals", "assists", "shots", "hits", "blocked", "shotPct",
            "timeOnIce"]
    df = create_fantasy_df(players, current_year, pos, cats, fpts_system, True)

    write_df_to_csv(df, "./data/fantasy_db_defensemen.csv", True)
