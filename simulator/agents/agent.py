"""An agent that can send commands to the Battle as requested."""

from abc import ABCMeta
from abc import abstractmethod

from simulator.battle.battle import Action
from simulator.battle.battle import Battle
from simulator.battle.battle import Player


class NoValidActionsException(Exception):
    pass


class Agent(metaclass=ABCMeta):
    """Abstract class for an agent controlling a side in a Battle"""

    SWITCHES = [
        Action.SWITCH_1, Action.SWITCH_2, Action.SWITCH_3, Action.SWITCH_4,
        Action.SWITCH_5, Action.SWITCH_6
    ]
    ACTIONS = [Action.MOVE_1, Action.MOVE_2, Action.MOVE_3, Action.MOVE_4
              ] + SWITCHES

    @abstractmethod
    def notify_switch_required(self, battle: Battle, player: Player):
        """Notify the agent that a switch is required in the given battle.

        Can either update internal flags to allow user input, or immediately
        return a computed response.

        Args:
            battle: The Battle in which the switch must be made.
            player: The Player who needs a pending switch added.
        """
        pass

    @abstractmethod
    def notify_action_required(self, battle: Battle, player: Player):
        """Notify the agent that an action is required in the given battle.

        Can either update internal flags to allow user input, or immediately
        return a computed response.

        Args:
            battle: The Battle in which the action must be taken.
            player: The Player who needs a pending action added.
        """
        pass
