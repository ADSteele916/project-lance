"""Functionality related to Pokemon moves."""

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Optional

import numpy as np

from simulator.type import Type

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon
    from simulator.battle.battle import Battle, Player


class InvalidPPException(Exception):

    def __init__(self, pp: int):
        super().__init__(f"{pp} is not a valid PP. It must be a positive integer.")


class InvalidAccuracyException(Exception):

    def __init__(self, accuracy: int):
        super().__init__(f"{accuracy} is not a valid accuracy. It must be an integer between 1 and 255.")


class InvalidPriorityException(Exception):

    def __init__(self, priority: int):
        super().__init__(f"{priority} is not a valid priority. It must be an integer between -1 and 1.")


class Move(metaclass=ABCMeta):
    """Abstract Base Class for a Pokemon Move, that can freely modify that Battle state."""

    def __init__(self, name: str, pp: int, move_type: Type, accuracy: Optional[int], priority: int = 0):
        if pp <= 0:
            raise InvalidPPException(pp)
        if accuracy is not None and not 0 < accuracy <= 255:
            raise InvalidAccuracyException(accuracy)
        if priority not in (-1, 0, 1):
            raise InvalidPriorityException(priority)
        self.name = name
        self.pp = pp
        self.move_type = move_type
        self.accuracy = accuracy
        self.priority = priority

    def __str__(self):
        return self.name

    def accuracy_check(self, attacker: "ActivePokemon", target: "ActivePokemon") -> bool:
        """Randomly determines whether or not the attacker will be be able to hit the target using this Move.

        Args:
            attacker (ActivePokemon): The Pokemon using this move.
            target (ActivePokemon): The Pokemon targeted by this move.

        Returns:
            bool: Whether or not this Move will hit its target.
        """
        if self.accuracy is None:
            return True

        accuracy = attacker.accuracy_multiplier
        evasion = target.evasion_multiplier
        threshold = max(0, min(255, self.accuracy * accuracy * evasion))

        accuracy_roll = np.random.randint(0, high=256)

        return accuracy_roll < threshold

    def execute(self, battle: "Battle", player: "Player"):
        """Executes the move pending an accuracy check, updating the given Battle environment as necessary.

        Args:
            battle (Battle): The Battle environment in which the move is being used.
            player (Player): The Player who used the move.
        """
        attacker: "ActivePokemon" = battle.teams[player][battle.team_cursors[player]]
        target: "ActivePokemon" = battle.teams[1 - player][battle.team_cursors[1 - player]]

        if self.accuracy_check(attacker, target):
            self.apply_effects(attacker, target)

    @abstractmethod
    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        """Applies the effects of the move to the attacker and/or target.

        Args:
            attacker (ActivePokemon): The Pokemon using this move.
            target (ActivePokemon): The Pokemon targeted by this move.
        """
        pass
