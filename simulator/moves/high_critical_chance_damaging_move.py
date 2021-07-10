"""A class that allows a move to have a high critical hit ratio."""

import numpy as np

from simulator.battle.active_pokemon import ActivePokemon
from simulator.moves.damaging_move import DamagingMove


class HighCriticalChanceDamagingMove(DamagingMove):
    """A damaging move that is more likely to result in critical hits."""

    @staticmethod
    def is_critical_hit(attacker: ActivePokemon):
        crit_roll = np.random.randint(0, high=256)
        threshold = attacker.pokemon.pokemon.species.critical_hit_threshold(True, attacker.focus_energy)
        return crit_roll < threshold
