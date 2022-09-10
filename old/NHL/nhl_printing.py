def print_season(season):
    print("Season:\t{}".format(season["season"]))
    print("Team:\t{}".format(season["team"]["name"]))
    print("Stats")
    for cat, score in season["stat"].items():
        print("\t{:<20s}\t{}".format(cat, score))

def print_fantasy_season(season):
    print("Not implemented")
