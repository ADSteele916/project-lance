"""An agent that makes random moves, for testing purposes."""

from random import shuffle

from simulator.agents.agent import Agent, NoValidActionsException
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


class RandomAgent(Agent):
    """An agent that randomly selects an action each turn."""

    def notify_switch_required(self, battle: Battle, player: Player):
        switches = self.SWITCHES.copy()
        shuffle(switches)
        for switch in switches:
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
        actions = self.ACTIONS.copy()
        shuffle(actions)
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
