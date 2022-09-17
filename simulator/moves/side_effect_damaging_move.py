"""Moves that do damage while also applying some side effect after a hit."""

from abc import ABCMeta
from abc import abstractmethod
import random
from typing import Optional, TYPE_CHECKING

from simulator.modifiable_stat import ModifiableStat
from simulator.moves.damaging_move import DamagingMove
from simulator.status import Status

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class SideEffectDamagingMove(DamagingMove, metaclass=ABCMeta):
    """A damaging move that applies a side effect to a Pokemon on the field."""

    def __init__(self,
                 name: str,
                 pp: int,
                 move_type: str,
                 power: int,
                 accuracy: Optional[int],
                 effect_chance: int,
                 *args,
                 priority: int = 0,
                 **kwargs):
        super().__init__(name, pp, move_type, power, accuracy, priority, *args,
                         **kwargs)
        self.effect_chance = effect_chance

    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        super().apply_effects(attacker, target)
        if self.should_apply_side_effect():
            self.side_effect(attacker, target)

    def should_apply_side_effect(self):
        return random.randint(0, 100) < self.effect_chance

    @abstractmethod
    def side_effect(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        pass


class DebuffingDamagingMove(SideEffectDamagingMove):
    """A damaging Pokemon move that can debuff one of its target's stats."""

    def __init__(self, name: str, pp: int, move_type: str, power: int,
                 accuracy: Optional[int], debuff_stat: ModifiableStat,
                 debuff_stages: int, debuff_chance: int, priority, *args,
                 **kwargs):
        super().__init__(name, pp, move_type, power, accuracy, debuff_chance,
                         priority, *args, **kwargs)
        self.debuff_stat = debuff_stat
        self.debuff_stages = debuff_stages

    def side_effect(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        target.modify_stat(self.debuff_stat, -self.debuff_stages)


class StatusDamagingMove(SideEffectDamagingMove):
    """A damaging move that applies a status condition to its target."""

    def __init__(self, name: str, pp: int, move_type: str, power: int,
                 accuracy: Optional[int], status: Status, status_chance: int,
                 priority, *args, **kwargs):
        super().__init__(name, pp, move_type, power, accuracy, status_chance,
                         priority, *args, **kwargs)
        self.status = status

    def side_effect(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        target.apply_status(self.status)


class FlinchingDamagingMove(SideEffectDamagingMove):

    def __init__(self, name: str, pp: int, move_type: str, power: int,
                 accuracy: Optional[int], flinch_chance: int, priority, *args,
                 **kwargs):
        super().__init__(name, pp, move_type, power, accuracy, flinch_chance,
                         priority, *args, **kwargs)

    def side_effect(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        target.flinch = True
