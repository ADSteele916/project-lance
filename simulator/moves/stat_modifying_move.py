"""Functionality related to moves that apply stat changes to active Pokemon."""

from abc import ABCMeta
from typing import TYPE_CHECKING, Optional

from simulator.modifiable_stat import ModifiableStat
from simulator.moves.move import Move

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class StatModifyingMove(Move, metaclass=ABCMeta):
    """A move that applies a stat change to one of the Pokemon on the field."""

    def __init__(
        self,
        name: str,
        pp: int,
        move_type: str,
        stat: ModifiableStat,
        stages: int,
        accuracy: Optional[int],
        *args,
        priority: int = 0,
        **kwargs
    ):
        super().__init__(name, pp, move_type, accuracy, priority, *args, **kwargs)
        self.stat = stat
        self.stages = stages


class StatRaisingMove(StatModifyingMove):
    """A Pokemon move that buffs one of its user's stats."""

    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        attacker.modify_stat(self.stat, self.stages)


class StatLoweringMove(StatModifyingMove):
    """A Pokemon move that debuffs one of its target's stats."""

    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        if not target.mist:
            target.modify_stat(self.stat, -self.stages)
