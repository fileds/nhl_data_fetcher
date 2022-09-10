import json
from nhl_utils import add_instruction

conversion = {}
conversion["goals"] = 2
conversion["assists"] = 1
conversion["points"] = 1
conversion["plusMinus"] = 0.3
conversion["shortHandedPoints"] = 1
conversion["shots"] = 0.2
conversion["hits"] = 0.2
conversion["blocked"] = 0.3

path = "./fantasy_point_system.json"

print("\nWriting fantasy point system to {} ... ".format(path), end="")
with open(path, "w+") as f:
    json.dump(conversion, f, indent=4)

print("Writing successful")

print("\nPoint system contains:")
for key, val in conversion.items():
    print("\t{}".format(key))

instructions_path = "./instructions.json"

add_instruction(instructions_path, "fantasy_point_system_path", path,
        verbose=True)
