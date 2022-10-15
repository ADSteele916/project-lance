"""Moves that hit multiple times."""

import random
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Dict, List

from simulator.moves.damaging_move import DamagingMove

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class RepeatingMove(DamagingMove, metaclass=ABCMeta):
    """Abstract class for a move that hits repeatedly."""

    @property
    @abstractmethod
    def repetitions(self) -> Dict[int, float]:
        pass

    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        attacks: List[int] = []
        weights: List[float] = []
        for a, w in self.repetitions.items():
            attacks.append(a)
            weights.append(w)
        repetitions = random.choices(attacks, weights)
        for _ in repetitions:
            super().apply_effects(attacker, target)


class DoubleHitMove(RepeatingMove):
    """A move that hits twice."""

    @property
    def repetitions(self) -> Dict[int, float]:
        return {2: 1.0}


class MultiHitMove(RepeatingMove):
    """A move that hits between two and five times."""

    @property
    def repetitions(self) -> Dict[int, float]:
        return {2: 0.375, 3: 0.375, 4: 0.125, 5: 0.125}
