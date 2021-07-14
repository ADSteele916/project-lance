"""Functionality related to moves that do damage while also applying some side effect after a hit."""

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Optional

import numpy as np

from simulator.moves.damaging_move import DamagingMove
from simulator.type import Type

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class SideEffectDamagingMove(DamagingMove, metaclass=ABCMeta):
    """Abstract base class for a damaging move that will apply a side effect to one of the Pokemon on the field."""

    def __init__(
            self,
            name: str,
            pp: int,
            move_type: Type,
            power: int,
            accuracy: Optional[int],
            effect_chance: int,
            priority: int = 0
    ):
        super().__init__(name, pp, move_type, power, accuracy, priority)
        self.effect_chance = effect_chance

    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        super().apply_effects(attacker, target)
        if self.should_apply_side_effect():
            self.side_effect(attacker, target)

    def should_apply_side_effect(self):
        return np.random.randint(0, 100) < self.effect_chance

    @abstractmethod
    def side_effect(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        pass
