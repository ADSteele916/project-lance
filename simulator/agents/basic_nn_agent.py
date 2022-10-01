"""A simple NeuralNetworkAgent that can compete in 1v1s with the starters."""

from abc import ABCMeta
from typing import List

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
    def _encode_one_hot_pokedex(pokemon: PokemonSpecies) -> List[float]:
        """Encodes a one-hot representation of a Pokemon species as a vector.

        Args:
            pokemon: The PokemonSpecies to encode.

        Returns:
            A vector representation of the given PokemonSpecies.

        Raises:
            ValueError: The PokemonSpecies must be Bulbasaur, Charmander, or
              Squirtle.
        """
        encoding = [0.0 for _ in range(3)]
        if pokemon.dex_num in (1, 4, 7):
            index = pokemon.dex_num // 3
        else:
            raise ValueError(
                "The Basic Ruleset only allows for the three starter Pokemon.")
        encoding[index] = 1
        return encoding

    @staticmethod
    def _encode_stat_modifiers(stat_modifiers: List[int]) -> List[float]:
        """Encodes the given list of status modifiers as a vector.
        Args:
            stat_modifiers: A six-element-long list of stat modifiers.
        Returns:
            A column vector representation of the given stat modifiers.
        """
        return [float(m) for m in stat_modifiers]

    @staticmethod
    def _encode_one_hot_status(status: Status) -> List[float]:
        """Encodes a one-hot representation of a Status as a vector.

        Args:
            status: The Status to encode.

        Returns:
            A vector representation of the given Status.
        """
        encoding = [0.0 for _ in Status]
        for index, test_status in enumerate(Status):
            if status == test_status:
                encoding[index] = 1
                break
        return encoding

    def _encode_active_pokemon(self, pokemon: ActivePokemon) -> List[float]:
        """Encodes a representation of an ActivePokemon as a vector.

        Args:
            pokemon: The ActivePokemon to encode.

        Returns:
            A vector representation of the given ActivePokemon.
        """
        return (self._encode_one_hot_pokedex(pokemon.species) +
                [pokemon.hp / pokemon.max_hp] +
                self._encode_stat_modifiers(pokemon.stat_modifiers) +
                self._encode_one_hot_status(pokemon.status))

    def vectorize_battle(self, battle: Battle, player: Player) -> List[float]:
        return (self._encode_active_pokemon(battle.actives[player]) +
                self._encode_active_pokemon(battle.actives[player.opponent]))
