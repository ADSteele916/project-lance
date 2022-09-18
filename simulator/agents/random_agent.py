"""An agent that makes random moves, for testing purposes."""

import random
from typing import List

from simulator.agents.agent import Agent
from simulator.battle.action import Action
from simulator.battle.battle import Battle
from simulator.battle.battle import Player


class RandomAgent(Agent):
    """An agent that randomly selects an action each turn."""

    def request_action(self, battle: Battle, player: Player,
                       choices: List[Action]) -> Action:
        return random.choice(choices)
