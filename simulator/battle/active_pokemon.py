"""Functionality for the Pokemon in a battle that is currently active."""

from enum import IntEnum
from typing import Optional, List, TYPE_CHECKING

from simulator.battle.battling_pokemon import BattlingPokemon
from simulator.moves.move import Move
from simulator.status import Status

if TYPE_CHECKING:
    from simulator.battle.battle import Battle, Player


class ZeroPPException(Exception):

    def __init__(self):
        super().__init__("PP is zero and cannot be decremented further.")


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
    def hp(self) -> int:
        return self.pokemon.hp

    @hp.setter
    def hp(self, new_hp):
        self.pokemon.hp = new_hp

    @property
    def max_hp(self) -> int:
        return self.pokemon.max_hp

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

    @property
    def status(self) -> Status:
        return self.pokemon.status

    @status.setter
    def status(self, new_status: Status):
        self.pokemon.status = new_status

    @property
    def moves(self) -> List[Move]:
        return self.pokemon.moves

    @property
    def pp(self) -> List[int]:
        return self.pokemon.pp

    @staticmethod
    def __stat_change_multiplier(modifier: int):
        if not -6 <= modifier <= 6:
            raise ValueError("Modifier must be in [-6, 6].")
        numerators = (25, 28, 33, 40, 50, 66, 100, 150, 200, 250, 300, 350, 400)
        return numerators[modifier + 6] / 100

    def deal_damage(self, damage: int):
        self.hp = self.hp - damage if self.hp - damage > 0 else 0

    def heal(self, damage: int):
        self.hp = self.hp + damage if self.hp + damage < self.max_hp else self.max_hp

    def use_move(self, move_index: int, battle: "Battle", player: "Player"):
        self.decrement_pp(move_index)
        self.moves[move_index].execute(battle, player)

    def decrement_pp(self, move_index: int):
        if self.pp[move_index] == 0:
            raise ZeroPPException()
        self.pp[move_index] -= 1
