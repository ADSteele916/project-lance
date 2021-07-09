"""Enum for non-volatile status conditions."""

from enum import Enum, auto


class Status(Enum):
    """Mutually-exclusive, non-volatile status conditions."""

    NONE = auto()
    ASLEEP = auto()
    POISONED = auto()
    BURNED = auto()
    FROZEN = auto()
    PARALYZED = auto()
