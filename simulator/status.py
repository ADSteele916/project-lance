"""Enum for non-volatile status conditions."""

from enum import Enum, auto


class Status(Enum):
    """Mutually-exclusive, non-volatile status conditions."""

    NONE = auto()
    SLEEP = auto()
    POISON = auto()
    BURN = auto()
    FREEZE = auto()
    PARALYZE = auto()
