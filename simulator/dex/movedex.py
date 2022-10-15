"""A dictionary containing a Move subclass for every Pokemon move."""

import json
import os.path
from typing import Dict

from simulator.modifiable_stat import ModifiableStat
from simulator.moves.damaging_move import (
    ConstantDamageMove,
    DamagingMove,
    HighCriticalChanceDamagingMove,
    LevelDamagingMove,
    RecoilDamagingMove,
)
from simulator.moves.misc_moves import LeechSeed, Mist, Psywave, SuperFang, Toxic
from simulator.moves.move import Move
from simulator.moves.repeating_move import DoubleHitMove, MultiHitMove
from simulator.moves.side_effect_damaging_move import (
    DebuffingDamagingMove,
    FlinchingDamagingMove,
    StatusDamagingMove,
)
from simulator.moves.stat_modifying_move import StatLoweringMove, StatRaisingMove
from simulator.moves.status_effect_move import StatusEffectMove


def _gen_movedex() -> Dict[str, Move]:
    with open(
        os.path.join(os.path.dirname(__file__), "movedex.json"), encoding="utf-8"
    ) as json_file:
        movedex_dict_list = json.load(json_file)

    movedex = {}

    classes = {
        "DamagingMove": DamagingMove,
        "HighCriticalChanceDamagingMove": HighCriticalChanceDamagingMove,
        "DoubleHitMove": DoubleHitMove,
        "MultiHitMove": MultiHitMove,
        "StatusEffectMove": StatusEffectMove,
        "StatRaisingMove": StatRaisingMove,
        "StatLoweringMove": StatLoweringMove,
        "FlinchingDamagingMove": FlinchingDamagingMove,
        "DebuffingDamagingMove": DebuffingDamagingMove,
        "StatusDamagingMove": StatusDamagingMove,
        "ConstantDamageMove": ConstantDamageMove,
        "LevelDamagingMove": LevelDamagingMove,
        "RecoilDamagingMove": RecoilDamagingMove,
        "LeechSeed": LeechSeed,
        "Mist": Mist,
        "Psywave": Psywave,
        "Toxic": Toxic,
        "SuperFang": SuperFang,
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
