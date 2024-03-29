"""Functionality related to Pokemon moves."""
import random
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Optional

from simulator.type import Type

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon
    from simulator.battle.battle import Battle, Player


class InvalidPPException(Exception):
    def __init__(self, pp: int):
        super().__init__(f"{pp} is not a valid PP. It must be a positive integer.")


class InvalidAccuracyException(Exception):
    def __init__(self, accuracy: int):
        super().__init__(
            f"{accuracy} is not a valid accuracy. It must be an integer "
            f"between 1 and 255."
        )


class InvalidPriorityException(Exception):
    def __init__(self, priority: int):
        super().__init__(
            f"{priority} is not a valid priority. It must be an integer "
            f"between -1 and 1."
        )


class Move(metaclass=ABCMeta):
    """A Pokemon Move, that can freely modify that Battle state."""

    def __init__(
        self,
        name: str,
        pp: int,
        move_type: str,
        accuracy: Optional[int],
        *args,
        priority: int = 0,
        **kwargs,
    ):
        # pylint: disable=unused-argument
        if pp <= 0:
            raise InvalidPPException(pp)
        if accuracy is not None and not 0 < accuracy <= 255:
            raise InvalidAccuracyException(accuracy)
        if priority not in (-1, 0, 1):
            raise InvalidPriorityException(priority)
        self.name = name
        self.pp = pp
        self.move_type = Type[move_type.upper()]
        self.accuracy = None if accuracy is None else (accuracy * 255) // 100
        self.priority = priority

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Move):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self):
        return self.name

    def accuracy_check(
        self, attacker: "ActivePokemon", target: "ActivePokemon"
    ) -> bool:
        """Randomly determines whether the attacker will hit the target.

        Args:
            attacker: The Pokemon using this move.
            target: The Pokemon targeted by this move.

        Returns:
            Whether this Move will hit its target.
        """
        if self.accuracy is None or not attacker.battle.ruleset.accuracy_checks:
            return True

        accuracy = attacker.accuracy_multiplier
        evasion = target.evasion_multiplier
        threshold = max(0, min(255, self.accuracy * accuracy * evasion))

        accuracy_roll = random.randint(0, 255)

        return accuracy_roll < threshold

    def execute(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        """Executes the move, updating the given Battle environment as needed.

        Args:
            attacker: The Pokemon using this move.
            target: The Pokemon targeted by this move.
        """
        assert attacker.battle is target.battle
        if self.accuracy_check(attacker, target):
            self.apply_effects(attacker, target)

    @abstractmethod
    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        """Applies the effects of the move to the attacker and/or target.

        Args:
            attacker: The Pokemon using this move.
            target: The Pokemon targeted by this move.
        """
        pass
