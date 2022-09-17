"""Functionality for the Pokemon in a battle that is currently active."""

from typing import List, Optional, TYPE_CHECKING

import numpy as np

from simulator.battle.battling_pokemon import BattlingPokemon
from simulator.modifiable_stat import ModifiableStat
from simulator.moves.move import Move
from simulator.pokemon.party_pokemon import PartyPokemon
from simulator.pokemon.pokemon_species import PokemonSpecies
from simulator.status import Status
from simulator.type import Type

if TYPE_CHECKING:
    from simulator.battle.battle import Battle
    from simulator.battle.battle import Player


class ZeroPPException(Exception):

    def __init__(self):
        super().__init__("PP is zero and cannot be decremented further.")


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
        self.mist = False
        self.flinch = False

    @property
    def species(self) -> PokemonSpecies:
        return self.pokemon.species

    @property
    def party_member(self) -> PartyPokemon:
        return self.pokemon.pokemon

    @property
    def pokemon(self) -> BattlingPokemon:
        return self.__pokemon

    @property
    def stat_modifiers(self) -> List[int]:
        return self.__stat_modifiers.copy()

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
        burn_multiplier = 0.5 if self.status == Status.BURN else 1.0
        return int(self.pokemon.attack * self.__stat_change_multiplier(
            self.__stat_modifiers[ModifiableStat.ATTACK]) * burn_multiplier)

    @property
    def defense(self) -> int:
        return int(self.pokemon.defense * self.__stat_change_multiplier(
            self.__stat_modifiers[ModifiableStat.DEFENSE]))

    @property
    def special(self) -> int:
        return int(self.pokemon.special * self.__stat_change_multiplier(
            self.__stat_modifiers[ModifiableStat.SPECIAL]))

    @property
    def speed(self) -> int:
        paralysis_multiplier = 0.25 if self.status == Status.PARALYZE else 1.0
        return int(self.pokemon.speed * self.__stat_change_multiplier(
            self.__stat_modifiers[ModifiableStat.SPEED]) * paralysis_multiplier)

    @property
    def evasion_multiplier(self) -> float:
        return self.__stat_change_multiplier(
            -self.__stat_modifiers[ModifiableStat.EVASION])

    @property
    def accuracy_multiplier(self) -> float:
        return self.__stat_change_multiplier(
            self.__stat_modifiers[ModifiableStat.ACCURACY])

    def modify_stat(self, stat: ModifiableStat, change: int):
        self.__stat_modifiers[stat] = max(
            -6, min(6, self.__stat_modifiers[stat] + change))

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
    def knocked_out(self) -> bool:
        return self.pokemon.knocked_out

    @property
    def pp(self) -> List[int]:
        return self.pokemon.pp

    @staticmethod
    def __stat_change_multiplier(modifier: int) -> float:
        """Produces the stat multiplier for a given modifier amount.

        Args:
            modifier: A stat modifier between -6 and 6, inclusive.

        Returns:
            The number by which the stat being modified should be multiplied
            during calculations.

        Raises:
            ValueError: The given modifier is outside the valid range.
        """
        if not -6 <= modifier <= 6:
            raise ValueError("Modifier must be in [-6, 6].")
        numerators = (25, 28, 33, 40, 50, 66, 100, 150, 200, 250, 300, 350, 400)
        return numerators[modifier + 6] / 100

    def deal_damage(self, damage: int):
        self.hp = self.hp - damage if self.hp - damage > 0 else 0

    def heal(self, damage: int):
        self.hp = (self.hp +
                   damage if self.hp + damage < self.max_hp else self.max_hp)

    def apply_status(self, status: Status):
        if self.status == Status.FREEZE and status == Status.BURN:
            self.status = Status.NONE
        elif status == Status.POISON and Type.POISON in (
                self.species.primary_type, self.species.secondary_type):
            return
        elif status == Status.BURN and Type.FIRE in (
                self.species.primary_type, self.species.secondary_type):
            return
        elif self.status == Status.NONE:
            self.status = status

    def use_move(self, move_index: int, battle: "Battle", player: "Player"):
        """Uses the move with the given index.

        If the Pokemon is paralyzed, there is a 25% chance it cannot move. If
        frozen, it will not be able to move until thawed. If burned or poisoned,
        one sixteenth of the Pokemon's max health will be dealt as damage if the
        opponent was not just knocked out. If seeded, another sixteenth of the
        Pokemon's max health is given to the opponent.

        Args:
            move_index: The index of the move that should be used.
            battle: The Battle in which the move is being used.
            player: The Player whose Pokemon is using the move.

        Raises:
            ValueError: The given index is out of range.
        """
        if not 0 <= move_index < len(self.moves):
            raise ValueError(f"Move index must be in [0, {len(self.moves)}).")

        if self.flinch:
            return

        if self.status == Status.PARALYZE:
            roll = np.random.random()
            if roll < 0.25:
                return
        if self.status == Status.FREEZE:
            return
        self.decrement_pp(move_index)
        self.moves[move_index].execute(battle, player)

        opponent = battle.actives[player.opponent]
        if not opponent.knocked_out:
            status_damage = max(self.max_hp // 16, 1)
            if self.status in (Status.POISON, Status.BURN):
                self.deal_damage(status_damage)
            if self.leech_seed:
                self.deal_damage(status_damage)
                opponent.heal(status_damage)

    def decrement_pp(self, move_index: int):
        if self.pp[move_index] == 0:
            raise ZeroPPException()
        self.pp[move_index] -= 1
