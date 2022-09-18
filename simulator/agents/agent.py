"""An agent that can send commands to the Battle as requested."""

from abc import ABCMeta
from abc import abstractmethod
from typing import List

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

    def request_switch(self, battle: Battle, player: Player,
                       choices: List[Action]) -> Action:
        """Request the agent to make a switch in the given battle.

        Can decide based on internal functionality or user input.

        Defaults to the same functionality as actions, but can be overriden.

        Args:
            battle: The Battle in which the switch must be made.
            player: The Player who needs a pending switch added.
            choices: The possible Actions the agent can take.

        Returns:
            An element of choices that will be executed.
        """
        return self.request_action(battle, player, choices)

    @abstractmethod
    def request_action(self, battle: Battle, player: Player,
                       choices: List[Action]) -> Action:
        """Request the agent to take an action in the given battle.

        Can decide based on internal functionality or user input.

        Args:
            battle: The Battle in which the action must be taken.
            player: The Player who needs a pending action added.
            choices: The possible Actions the agent can take.

        Returns:
            An element of choices that will be executed.
        """
        pass
