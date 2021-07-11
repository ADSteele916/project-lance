"""Specification for an agent that can send commands to the Battle as requested."""

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulator.battle.battle import Battle


class PlayerAgent(metaclass=ABCMeta):
    """Abstract class for a player controlling a side in a Battle"""

    @abstractmethod
    def notify_switch_required(self, battle: "Battle"):
        """Notify the agent that a switch is required in the given battle.

        Can either update internal flags to allow user input, or immediately return a computed response.

        Args:
            battle (Battle): The Battle in which the switch must be made.
        """
        pass

    @abstractmethod
    def notify_action_required(self, battle: "Battle"):
        """Notify the agent that an action (moving or switching) is required in the given battle.

        Can either update internal flags to allow user input, or immediately return a computed response.

        Args:
            battle (Battle): The Battle in which the action must be taken.
        """
        pass
