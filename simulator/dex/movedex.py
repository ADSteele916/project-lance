"""Loads a dictionary containing an instance of a Move subclass for every available move."""

import json
import os.path
from typing import Dict

from simulator.modifiable_stat import ModifiableStat
from simulator.moves.damaging_move import DamagingMove
from simulator.moves.debuffing_damaging_move import DebuffingDamagingMove
from simulator.moves.flinching_damaging_move import FlinchingDamagingMove
from simulator.moves.high_critical_chance_damaging_move import HighCriticalChanceDamagingMove
from simulator.moves.misc_moves import ConstantDamageMove, LeechSeed, LevelDamagingMove, Mist
from simulator.moves.move import Move
from simulator.moves.stat_lowering_move import StatLoweringMove
from simulator.moves.stat_raising_move import StatRaisingMove
from simulator.moves.status_damaging_move import StatusDamagingMove


def _gen_movedex() -> Dict[str, Move]:
    with open(os.path.join(os.path.dirname(__file__), "movedex.json")) as json_file:
        movedex_dict_list = json.load(json_file)

    movedex = {}

    classes = {
            "DamagingMove": DamagingMove,
            "HighCriticalChanceDamagingMove": HighCriticalChanceDamagingMove,
            "StatRaisingMove": StatRaisingMove,
            "StatLoweringMove": StatLoweringMove,
            "FlinchingDamagingMove": FlinchingDamagingMove,
            "DebuffingDamagingMove": DebuffingDamagingMove,
            "StatusDamagingMove": StatusDamagingMove,
            "ConstantDamageMove": ConstantDamageMove,
            "LevelDamagingMove": LevelDamagingMove,
            "LeechSeed": LeechSeed,
            "Mist": Mist,
    }

    stat_mapping = {
        "Attack": ModifiableStat.ATTACK,
        "Defense": ModifiableStat.DEFENSE,
        "Special": ModifiableStat.SPECIAL,
        "Speed": ModifiableStat.SPEED,
        "Evasion": ModifiableStat.EVASION,
        "Accuracy": ModifiableStat.ACCURACY,
    }

    for move in movedex_dict_list:
        try:
            move_class = classes[move["cls"]]
        except KeyError:
            continue
        move_dict = {**move}
        if "stat" in move_dict:
            move_dict["stat"] = stat_mapping[move_dict["stat"]]
        if "debuff_stat" in move_dict:
            move_dict["debuff_stat"] = stat_mapping[move_dict["debuff_stat"]]

        movedex[move["name"]] = move_class(**move_dict)

    return movedex


MOVEDEX = _gen_movedex()
