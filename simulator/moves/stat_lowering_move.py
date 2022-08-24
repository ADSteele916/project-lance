"""Functionality for a move that applies a stat debuff to the ActivePokemon that it is used on."""

from typing import TYPE_CHECKING

from simulator.moves.stat_modifying_move import StatModifyingMove

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class StatLoweringMove(StatModifyingMove):
    """A Pokemon move that debuffs one of its target's stats."""

    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        if not target.mist:
            target.modify_stat(self.stat, -self.stages)
