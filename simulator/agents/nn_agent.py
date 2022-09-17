"""Functionality for an Agent that interfaces with a neural network."""

from abc import ABCMeta
from abc import abstractmethod
from typing import List

import numpy as np

from simulator.agents.agent import Agent
from simulator.agents.agent import NoValidActionsException
from simulator.battle.action import Action
from simulator.battle.battle import AlreadyInBattleException
from simulator.battle.battle import Battle
from simulator.battle.battle import FaintedPokemonException
from simulator.battle.battle import MoveNotSwitchException
from simulator.battle.battle import NoMoveInSlotException
from simulator.battle.battle import NoPokemonInSlotException
from simulator.battle.battle import OutOfPPException
from simulator.battle.battle import Player
from simulator.battle.battle import SwitchNotRequestedException


class NeuralNetworkAgent(Agent, metaclass=ABCMeta):
    """An Agent whose decisions are made by a neural network."""

    def notify_switch_required(self, battle: Battle, player: Player):
        for switch in list(
                filter(lambda a: a.is_switch, self.rank_actions(battle,
                                                                player))):
            try:
                battle.set_pending_switch(player, switch)
            except (SwitchNotRequestedException, MoveNotSwitchException,
                    AlreadyInBattleException, NoPokemonInSlotException,
                    FaintedPokemonException):
                pass
            else:
                return
        raise NoValidActionsException()

    def notify_action_required(self, battle: Battle, player: Player):
        actions = self.rank_actions(battle, player)
        for action in actions:
            try:
                battle.set_pending_action(player, action)
            except (AlreadyInBattleException, NoPokemonInSlotException,
                    FaintedPokemonException, NoMoveInSlotException,
                    OutOfPPException):
                pass
            else:
                return
        raise NoValidActionsException()

    @abstractmethod
    def evaluate_network(self, input_vector: np.ndarray) -> List[float]:
        """Ranks available actions using neural network.

        Args:
            input_vector: A vectorized representation of the Battle.

        Returns:
            Scores for each of the elements of self.ACTIONS.
        """
        pass

    @abstractmethod
    def vectorize_battle(self, battle: Battle, player: Player) -> np.ndarray:
        """Produces a vector of requisite data for evaluate_network.

        Args:
            battle: The Battle in which an Action must be chosen.
            player: The Player that this Agent is choosing an Action for.

        Returns:
            A vectorized representation of the Battle to input to a network.
        """
        pass

    def rank_actions(self, battle: Battle, player: Player) -> List[Action]:
        """Rank ACTIONS in order from the best to the worst for the situation.

        Args:
            battle: The Battle in which an Action must be chosen.
            player: The Player that this Agent is choosing an Action for.

        Returns:
            A ranked copy of ACTIONS, from most preferred to least preferred.
        """
        output = self.evaluate_network(self.vectorize_battle(battle, player))
        assert len(output) == 10

        actions = self.ACTIONS.copy()
        idx_actions = list(enumerate(actions))
        idx_actions.sort(key=lambda p: output[p[0]], reverse=True)
        return list(map(lambda p: p[1], idx_actions))
