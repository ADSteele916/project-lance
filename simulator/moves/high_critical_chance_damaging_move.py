"""A class that allows a move to have a high critical hit ratio."""

from typing import TYPE_CHECKING

import numpy as np

from simulator.moves.damaging_move import DamagingMove

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class HighCriticalChanceDamagingMove(DamagingMove):
    """A damaging move that is more likely to result in critical hits."""

    @staticmethod
    def is_critical_hit(attacker: "ActivePokemon"):
        crit_roll = np.random.randint(0, high=256)
        threshold = attacker.pokemon.pokemon.species.critical_hit_threshold(True, attacker.focus_energy)
        return crit_roll < threshold
