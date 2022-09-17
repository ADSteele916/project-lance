"""An agent that makes random moves, for testing purposes."""

from random import shuffle

from simulator.agents.agent import Agent
from simulator.agents.agent import NoValidActionsException
from simulator.battle.battle import AlreadyInBattleException
from simulator.battle.battle import Battle
from simulator.battle.battle import FaintedPokemonException
from simulator.battle.battle import MoveNotSwitchException
from simulator.battle.battle import NoMoveInSlotException
from simulator.battle.battle import NoPokemonInSlotException
from simulator.battle.battle import OutOfPPException
from simulator.battle.battle import Player
from simulator.battle.battle import SwitchNotRequestedException


class RandomAgent(Agent):
    """An agent that randomly selects an action each turn."""

    def notify_switch_required(self, battle: Battle, player: Player):
        switches = self.SWITCHES.copy()
        shuffle(switches)
        for switch in switches:
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
        actions = self.ACTIONS.copy()
        shuffle(actions)
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
