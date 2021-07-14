"""Functionality for a damaging move that has a chance to apply a stat debuff to its target."""

from typing import TYPE_CHECKING, Optional

from simulator.modifiable_stat import ModifiableStat
from simulator.moves.side_effect_damaging_move import SideEffectDamagingMove
from simulator.type import Type

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class DebuffingDamagingMove(SideEffectDamagingMove):
    """A damaging Pokemon move that can debuff one of its target's stats."""

    def __init__(
            self,
            name: str,
            pp: int,
            move_type: Type,
            power: int,
            accuracy: Optional[int],
            debuff_stat: ModifiableStat,
            debuff_stages: int,
            debuff_chance: int,
            priority
    ):
        super().__init__(name, pp, move_type, power, accuracy, debuff_chance, priority)
        self.debuff_stat = debuff_stat
        self.debuff_stages = debuff_stages

    def side_effect(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        target.modify_stat(self.debuff_stat, -self.debuff_stages)
