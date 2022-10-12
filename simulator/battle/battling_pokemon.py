"""A Pokemon currently in battle, with variable HP, Status, and PP"""

from typing import List

from simulator.moves.move import Move
from simulator.pokemon.party_pokemon import PartyPokemon
from simulator.pokemon.pokemon_species import PokemonSpecies
from simulator.status import Status


class InvalidHPException(Exception):

    def __init__(self, invalid_hp: int):
        super().__init__(
            f"{invalid_hp} is an invalid HP. HP values must be between 0 and "
            f"the Pokemon's maximum HP.")


class BattlingPokemon:
    """A Pokemon that is currently in a battle, but may or may not be active."""

    def __init__(self, party_pokemon: PartyPokemon):
        self._party_pokemon = party_pokemon
        self._hp = party_pokemon.hp
        self._status = Status.NONE
        self._pp = [m.pp for m in party_pokemon.moves]

    def __str__(self):
        return str(self._party_pokemon)

    @property
    def species(self) -> PokemonSpecies:
        return self.pokemon.species

    @property
    def pokemon(self) -> PartyPokemon:
        return self._party_pokemon

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, new_hp: int):
        if not 0 <= new_hp <= self.max_hp:
            raise InvalidHPException(new_hp)
        self._hp = new_hp

    @property
    def max_hp(self) -> int:
        return self.pokemon.hp

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
        return self._status

    @status.setter
    def status(self, new_status: Status):
        self._status = new_status

    @property
    def moves(self) -> List[Move]:
        return self.pokemon.moves

    @property
    def pp(self) -> List[int]:
        return self._pp

    @property
    def knocked_out(self) -> bool:
        return self.hp == 0
