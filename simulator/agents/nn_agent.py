"""Functionality for an Agent that interfaces with a neural network."""

from abc import ABCMeta, abstractmethod
from typing import List

import numpy as np

from simulator.agents.agent import Agent, NoValidActionsException
from simulator.battle.action import Action
from simulator.battle.battle import (
        AlreadyInBattleException,
        Battle,
        FaintedPokemonException,
        MoveNotSwitchException,
        NoMoveInSlotException,
        NoPokemonInSlotException,
        OutOfPPException,
        Player,
        SwitchNotRequestedException
)


class NeuralNetworkAgent(Agent, metaclass=ABCMeta):
    """An Agent whose decisions are made by a neural network."""

    def notify_switch_required(self, battle: Battle, player: Player):
        for switch in list(filter(lambda a: a.is_switch, self.rank_actions(battle, player))):
            try:
                battle.set_pending_switch(player, switch)
            except (
                    SwitchNotRequestedException,
                    MoveNotSwitchException,
                    AlreadyInBattleException,
                    NoPokemonInSlotException,
                    FaintedPokemonException
            ):
                pass
            else:
                return
        raise NoValidActionsException()

    def notify_action_required(self, battle: Battle, player: Player):
        actions = self.rank_actions(battle, player)
        for action in actions:
            try:
                battle.set_pending_action(player, action)
            except (
                    AlreadyInBattleException,
                    NoPokemonInSlotException,
                    FaintedPokemonException,
                    NoMoveInSlotException,
                    OutOfPPException
            ):
                pass
            else:
                return
        raise NoValidActionsException()

    @abstractmethod
    def evaluate_network(self, input_vector: np.ndarray) -> List[float]:
        """Consumes a column vector representation of a Battle and ranks available actions.

        Args:
            input_vector (np.ndarray): A vectorized representation of the Battle

        Returns:
            List[float]: Scores for each of the elements of self.ACTIONS.
        """
        pass

    @abstractmethod
    def vectorize_battle(self, battle: Battle, player: Player) -> np.ndarray:
        """Produce a column vector containing all requisite data for evaluate_network to make a decision.

        Args:
            battle (Battle): The Battle in which an Action must be chosen.
            player (Player): The Player that this Agent is choosing an Action for.

        Returns:
            np.ndarray: A vectorized representation of the Battle to input to a network.
        """
        pass

    def rank_actions(self, battle: Battle, player: Player) -> List[Action]:
        """Rank self.ACTIONS in order from the best to the worst for the present situation.

        Args:
            battle (Battle): The Battle in which an Action must be chosen.
            player (Player): The Player that this Agent is choosing an Action for.

        Returns:
            List[Action]: A ranked copy of self.ACTIONS, from most preferred to least preferred.
        """
        output = self.evaluate_network(self.vectorize_battle(battle, player))
        assert len(output) == 10

        actions = self.ACTIONS.copy()
        idx_actions = list(enumerate(actions))
        idx_actions.sort(key=lambda p: output[p[0]], reverse=True)
        return list(map(lambda p: p[1], idx_actions))
