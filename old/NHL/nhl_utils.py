import os
import numpy as np
import sys
from pprint import pprint
import json

def convert_time_stat(stat):
    if isinstance(stat, int):
        return float(stat)
    elif isinstance(stat, str):
        value = stat.split(":")
        return float(value[0]) + float(value[1]) / 60.0
    else:
        return -1

def load_instructions(instructions_path, keys):
    with open(instructions_path, "r") as f:
        instructions = json.load(f)

    if isinstance(keys, list):
        values = []
        for key in keys:
            if key not in instructions.keys():
                print("Error: Could not find key {}\n".format(key))
            else:
                values.append(instructions[key])
        return tuple(values)
    elif isinstance(keys, str):
        return instructions[keys]


def add_instruction(instructions_path, key, value, verbose=True):
    with open(instructions_path, "r") as f:
        instructions = json.load(f)
        instructions[key] = value

    if verbose:
        print("\nAdding instruction {} for {} to {}".format(value, key,
            instructions_path))

    with open(instructions_path, "w+") as f:
        json.dump(instructions, f, indent=4)

        if verbose:
            print("Writing successful")
            print("\nInstructions now contains:")
            for key, val in instructions.items():
                print("\t{}".format(key))

def print_status(n_done, n_tot):
    n_signs = 50
    n_tot_norm = n_tot / n_signs
    n_done_norm = int(np.ceil(n_done / n_tot_norm))
    # n_done_norm = int(n_done / n_tot_norm)
    diff = n_signs - n_done_norm
    string = ("Processing: " + n_done_norm * "#" + diff * "_")
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(string)
    sys.stdout.flush()
