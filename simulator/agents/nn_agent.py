"""Functionality for an Agent that interfaces with a neural network."""

from abc import ABCMeta
from abc import abstractmethod
from typing import List

from simulator.agents.agent import Agent
from simulator.agents.agent import NoValidActionsException
from simulator.battle.action import Action
from simulator.battle.battle import Battle
from simulator.battle.battle import Player


class NeuralNetworkAgent(Agent, metaclass=ABCMeta):
    """An Agent whose decisions are made by a neural network."""

    def request_action(self, battle: Battle, player: Player,
                       choices: List[Action]) -> Action:
        for action in self.rank_actions(battle, player):
            if action in choices:
                return action
        raise NoValidActionsException()

    @abstractmethod
    def evaluate_network(self, input_vector: List[float]) -> List[float]:
        """Ranks available actions using neural network.

        Args:
            input_vector: A vectorized representation of the Battle.

        Returns:
            Scores for each of the elements of self.ACTIONS.
        """
        pass

    @abstractmethod
    def vectorize_battle(self, battle: Battle, player: Player) -> List[float]:
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
