"""Enum for stats the can be modified by moves during a battle."""

from enum import IntEnum


class ModifiableStat(IntEnum):
    """Indices for ActivePokemon.__stat_modifiers' modifier values."""

    ATTACK = 0
    DEFENSE = 1
    SPECIAL = 2
    SPEED = 3
    EVASION = 4
    ACCURACY = 5
