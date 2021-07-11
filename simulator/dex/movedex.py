"""Loads a dictionary containing an instance of a Move subclass for every available move."""

import json

import numpy as np

from simulator.moves.damaging_move import DamagingMove
from simulator.moves.high_critical_chance_damaging_move import HighCriticalChanceDamagingMove
from simulator.type import Type

with open("movedex.json") as json_file:
    __movedex_dict_list = json.load(json_file)

MOVEDEX = {}

for __move in __movedex_dict_list:
    if "cls" in __move:
        if __move["cls"] == "DamagingMove":
            MOVEDEX[__move["name"]] = DamagingMove(
                    __move["name"],
                    __move["pp"],
                    Type[__move["move_type"].upper()],
                    __move["power"],
                    np.floor(__move["accuracy"] * 255 / 100),
                    __move["priority"]
            )
        elif __move["cls"] == "HighCriticalChanceDamagingMove":
            MOVEDEX[__move["name"]] = HighCriticalChanceDamagingMove(
                    __move["name"],
                    __move["pp"],
                    Type[__move["move_type"].upper()],
                    __move["power"],
                    np.floor(__move["accuracy"] * 255 / 100),
                    __move["priority"]
            )
