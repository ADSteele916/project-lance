"""Functionality for a move that applies a stat buff to the ActivePokemon that uses it."""

from typing import TYPE_CHECKING

from simulator.moves.stat_modifying_move import StatModifyingMove

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class StatRaisingMove(StatModifyingMove):
    """A Pokemon move that buffs one of its user's stats."""

    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        attacker.modify_stat(self.stat, self.stages)
