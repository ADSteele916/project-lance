import random
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Dict, List

from simulator.moves.damaging_move import DamagingMove

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class RepeatingMove(DamagingMove, metaclass=ABCMeta):

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
