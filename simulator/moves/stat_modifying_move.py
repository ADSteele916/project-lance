"""Functionality related to moves that apply stat changes to active Pokemon."""

from abc import ABCMeta
from typing import Optional

from simulator.modifiable_stat import ModifiableStat
from simulator.moves.move import Move
from simulator.type import Type


class StatModifyingMove(Move, metaclass=ABCMeta):
    """Abstract base class for a move that will apply a stat change to one of the Pokemon on the field."""

    def __init__(
            self,
            name: str,
            pp: int,
            move_type: Type,
            stat: ModifiableStat,
            stages: int,
            accuracy: Optional[int],
            priority: int = 0,
            *args,
            **kwargs
    ):
        super().__init__(name, pp, move_type, accuracy, priority, *args, **kwargs)
        self.stat = stat
        self.stages = stages
