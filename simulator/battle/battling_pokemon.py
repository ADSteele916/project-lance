"""Functionality for a Pokemon currently in battle, with variable HP, Status, and PP"""

from typing import TYPE_CHECKING, List

from simulator.pokemon.party_pokemon import PartyPokemon
from simulator.status import Status

if TYPE_CHECKING:
    from simulator.battle.battle import Battle, Player


class ZeroPPException(Exception):

    def __init__(self):
        super().__init__("PP is zero and cannot be decremented further.")


class BattlingPokemon:
    """A Pokemon that is currently in a battle, but may or may not be active."""

    def __init__(self, pokemon: PartyPokemon):
        self.__pokemon = pokemon
        self.__hp = pokemon.hp
        self.__status = Status.NONE
        self.__pp = list(map(lambda m: None if m is None else m.pp, pokemon.moves))

    @property
    def pokemon(self) -> PartyPokemon:
        return self.__pokemon

    @property
    def hp(self) -> int:
        return self.__hp

    @property
    def attack(self) -> int:
        return self.pokemon.attack

    @property
    def defense(self) -> int:
        return self.pokemon.defense

    @property
    def speed(self) -> int:
        return self.pokemon.speed

    @property
    def special(self) -> int:
        return self.pokemon.special

    @property
    def status(self) -> Status:
        return self.__status

    @status.setter
    def status(self, new_status: Status):
        self.__status = new_status

    @property
    def pp(self) -> List[int]:
        return self.__pp

    @property
    def knocked_out(self) -> bool:
        return self.hp == 0

    def deal_damage(self, damage: int):
        self.__hp = self.__hp - damage if self.__hp - damage > 0 else 0

    def heal(self, damage: int):
        self.__hp = self.__hp + damage if self.__hp + damage < self.pokemon.hp else self.pokemon.hp

    def use_move(self, move_index: int, battle: "Battle", player: "Player"):
        self.decrement_pp(move_index)
        self.pokemon.moves[move_index].execute(battle, player)

    def decrement_pp(self, move_index: int):
        if self.__pp[move_index] == 0:
            raise ZeroPPException()
        self.__pp[move_index] -= 1
