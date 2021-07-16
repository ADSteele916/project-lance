"""Loads a dictionary containing an instance of a Move subclass for every available move."""

import json
import os.path
from math import floor

from simulator.modifiable_stat import ModifiableStat
from simulator.moves.damaging_move import DamagingMove
from simulator.moves.debuffing_damaging_move import DebuffingDamagingMove
from simulator.moves.high_critical_chance_damaging_move import HighCriticalChanceDamagingMove
from simulator.moves.misc_moves import LeechSeed
from simulator.moves.stat_lowering_move import StatLoweringMove
from simulator.moves.stat_raising_move import StatRaisingMove
from simulator.moves.status_damaging_move import StatusDamagingMove
from simulator.status import Status
from simulator.type import Type

with open(os.path.join(os.path.dirname(__file__), "movedex.json")) as json_file:
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
                    None if __move["accuracy"] is None else floor(__move["accuracy"] * 255 / 100),
                    __move["priority"]
            )
        elif __move["cls"] == "HighCriticalChanceDamagingMove":
            MOVEDEX[__move["name"]] = HighCriticalChanceDamagingMove(
                    __move["name"],
                    __move["pp"],
                    Type[__move["move_type"].upper()],
                    __move["power"],
                    None if __move["accuracy"] is None else floor(__move["accuracy"] * 255 / 100),
                    __move["priority"]
            )
        elif __move["cls"] == "StatRaisingMove":
            MOVEDEX[__move["name"]] = StatRaisingMove(
                    __move["name"],
                    __move["pp"],
                    Type[__move["move_type"].upper()],
                    ModifiableStat[__move["stat"].upper()],
                    __move["stages"],
                    None if __move["accuracy"] is None else floor(__move["accuracy"] * 255 / 100),
                    __move["priority"]
            )
        elif __move["cls"] == "StatLoweringMove":
            MOVEDEX[__move["name"]] = StatLoweringMove(
                    __move["name"],
                    __move["pp"],
                    Type[__move["move_type"].upper()],
                    ModifiableStat[__move["stat"].upper()],
                    __move["stages"],
                    None if __move["accuracy"] is None else floor(__move["accuracy"] * 255 / 100),
                    __move["priority"]
            )
        elif __move["cls"] == "DebuffingDamagingMove":
            MOVEDEX[__move["name"]] = DebuffingDamagingMove(
                    __move["name"],
                    __move["pp"],
                    Type[__move["move_type"].upper()],
                    __move["power"],
                    None if __move["accuracy"] is None else floor(__move["accuracy"] * 255 / 100),
                    ModifiableStat[__move["debuff_stat"].upper()],
                    __move["debuff_stages"],
                    __move["debuff_chance"],
                    __move["priority"]
            )
        elif __move["cls"] == "StatusDamagingMove":
            MOVEDEX[__move["name"]] = StatusDamagingMove(
                    __move["name"],
                    __move["pp"],
                    Type[__move["move_type"].upper()],
                    __move["power"],
                    None if __move["accuracy"] is None else floor(__move["accuracy"] * 255 / 100),
                    Status[__move["status"].upper()],
                    __move["status_chance"],
                    __move["priority"]
            )
        elif __move["cls"] == "LeechSeed":
            MOVEDEX[__move["name"]] = LeechSeed(
                    __move["name"],
                    __move["pp"],
                    Type[__move["move_type"].upper()],
                    None if __move["accuracy"] is None else floor(__move["accuracy"] * 255 / 100),
                    __move["priority"]
            )
