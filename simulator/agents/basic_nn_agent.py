"""A simple NeuralNetworkAgent that can compete in 1v1s with the starters."""

from abc import ABCMeta
from typing import List

import numpy as np

from simulator.agents.nn_agent import NeuralNetworkAgent
from simulator.battle.active_pokemon import ActivePokemon
from simulator.battle.battle import Battle
from simulator.battle.battle import Player
from simulator.pokemon.pokemon_species import PokemonSpecies
from simulator.status import Status


class BasicNeuralNetworkAgent(NeuralNetworkAgent, metaclass=ABCMeta):
    """A basic NeuralNetworkAgent.

    This is an agent that bases its decisions solely on the status of the
    current ActivePokemon. Its Pokedex is limited to the three starters.
    """

    @staticmethod
    def __encode_one_hot_pokedex(pokemon: PokemonSpecies) -> np.ndarray:
        """Encodes a one-hot representation of a Pokemon species as a vector.

        Args:
            pokemon: The PokemonSpecies to encode.

        Returns:
            A column vector representation of the given PokemonSpecies.

        Raises:
            ValueError: The PokemonSpecies must be Bulbasaur, Charmander, or
              Squirtle.
        """
        encoding = np.zeros((3, 1))
        if pokemon.dex_num in (1, 4, 7):
            index = pokemon.dex_num // 3
        else:
            raise ValueError(
                "The Basic Ruleset only allows for the three starter Pokemon.")
        encoding[index, 0] = 1
        return encoding

    @staticmethod
    def __encode_stat_modifiers(stat_modifiers: List[int]) -> np.ndarray:
        """Encodes the given list of status modifiers as a vector.

        Args:
            stat_modifiers: A six-element-long list of stat modifiers.

        Returns:
            A column vector representation of the given stat modifiers.
        """
        encoding = np.array(stat_modifiers, ndmin=2).T
        assert encoding.shape == (6, 1)
        return encoding

    @staticmethod
    def __encode_one_hot_status(status: Status) -> np.ndarray:
        """Encodes a one-hot representation of a Status as a vector.

        Args:
            status: The Status to encode.

        Returns:
            A column vector representation of the given Status.
        """
        encoding = np.zeros((len(Status), 1))
        for index, test_status in enumerate(Status):
            if status == test_status:
                encoding[index, 0] = 1
                break
        return encoding

    def __encode_active_pokemon(self, pokemon: ActivePokemon) -> np.ndarray:
        """Encodes a representation of an ActivePokemon as a vector.

        Args:
            pokemon: The ActivePokemon to encode.

        Returns:
            A column vector representation of the given ActivePokemon.
        """
        return np.vstack(
            (self.__encode_one_hot_pokedex(pokemon.pokemon.pokemon.species),
             np.array([[pokemon.hp / pokemon.max_hp]]),
             self.__encode_stat_modifiers(pokemon.stat_modifiers),
             self.__encode_one_hot_status(pokemon.status)))

    def vectorize_battle(self, battle: Battle, player: Player) -> np.ndarray:
        return np.vstack(
            (self.__encode_active_pokemon(battle.actives[player]),
             self.__encode_active_pokemon(battle.actives[player.opponent])))
