"""Functionality for the Pokemon in a battle that is currently active."""

from enum import IntEnum
from typing import Optional

from simulator.battle.battling_pokemon import BattlingPokemon


class ModifiableStat(IntEnum):
    """Indices for ActivePokemon.__stat_modifiers' modifier values"""

    ATTACK = 0
    DEFENSE = 1
    SPECIAL = 2
    SPEED = 3
    EVASION = 4
    ACCURACY = 5


class ActivePokemon:
    """Pokemon currently in battle, with stat changes, toxic counter, etc."""

    def __init__(self, pokemon: BattlingPokemon):
        self.__pokemon = pokemon
        self.__stat_modifiers = [0 for _ in range(6)]
        self.confused = False
        self.leech_seed = False
        self.toxic_counter: Optional[int] = None
        self.reflect = False
        self.light_screen = False
        self.focus_energy = False

    @property
    def pokemon(self) -> BattlingPokemon:
        return self.__pokemon

    @property
    def attack(self) -> int:
        return self.pokemon.attack * self.__stat_change_multiplier(self.__stat_modifiers[ModifiableStat.ATTACK])

    @property
    def defense(self) -> int:
        return self.pokemon.defense * self.__stat_change_multiplier(self.__stat_modifiers[ModifiableStat.DEFENSE])

    @property
    def special(self) -> int:
        return self.pokemon.special * self.__stat_change_multiplier(self.__stat_modifiers[ModifiableStat.SPECIAL])

    @property
    def speed(self) -> int:
        return self.pokemon.speed * self.__stat_change_multiplier(self.__stat_modifiers[ModifiableStat.SPEED])

    @property
    def evasion_multiplier(self) -> float:
        return self.__stat_change_multiplier(-self.__stat_modifiers[ModifiableStat.EVASION])

    @property
    def accuracy_multiplier(self) -> float:
        return self.__stat_change_multiplier(self.__stat_modifiers[ModifiableStat.ACCURACY])

    def modify_stat(self, stat: ModifiableStat, change: int):
        self.__stat_modifiers[stat] = max(-6, min(6, self.__stat_modifiers[stat] + change))

    @staticmethod
    def __stat_change_multiplier(modifier: int):
        if not -6 <= modifier <= 6:
            raise ValueError("Modifier must be in [-6, 6].")
        numerators = (25, 28, 33, 40, 50, 66, 100, 150, 200, 250, 300, 350, 400)
        return numerators[modifier + 6] / 100
