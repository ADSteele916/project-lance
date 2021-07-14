# pylint: disable=consider-using-with
"""Functionality for a Battle between two Pokemon teams, with user input for both sides."""

from enum import IntEnum
from threading import Lock
from typing import List, Optional, Tuple

import numpy as np

from simulator.battle.action import MOVE_SLOTS, SWITCH_SLOTS, Action
from simulator.battle.active_pokemon import ActivePokemon
from simulator.battle.battling_pokemon import BattlingPokemon
from simulator.battle.player_agent import PlayerAgent
from simulator.pokemon.party_pokemon import PartyPokemon


class Player(IntEnum):
    """Indices for various tuples and 2-element lists in Battle"""

    P1 = 0
    P2 = 1

    @property
    def opponent(self):
        return Player.P1 if self == Player.P2 else Player.P2


class NoMoveInSlotException(Exception):

    def __init__(self, slot: int):
        super().__init__(f"There is no move in move slot {slot}")


class OutOfPPException(Exception):

    def __init__(self, move: str):
        super().__init__(f"{move} is out of PP and cannot be used.")


class AlreadyInBattleException(Exception):

    def __init__(self, pokemon: ActivePokemon):
        super().__init__(f"{pokemon} is already in battle.")


class FaintedPokemonException(Exception):

    def __init__(self, pokemon: PartyPokemon):
        super().__init__(f"{pokemon} has fainted and cannot switch in.")


class NoPokemonInSlotException(Exception):

    def __init__(self, slot: int):
        super().__init__(f"There is no pokemon in slot {slot}")


class InvalidTeamSizeException(Exception):

    def __init__(self, size: int):
        super().__init__(f"{size} is an invalid team size. Teams must have between 1 and 6 members.")


class SwitchNotRequestedException(Exception):

    def __init__(self, player: Player):
        super().__init__(f"{player.name} is not being prompted to switch at the moment.")


class MoveNotSwitchException(Exception):

    def __init__(self, player: Player):
        super().__init__(f"{player.name} must provide a slot to switch to, not a move.")


class ActionNotSetException(Exception):
    pass


class SwitchNotSetException(Exception):
    pass


class Battle:
    """A Pokemon battle with all state information for both teams"""

    PLAYERS = (Player.P1, Player.P2)

    def __init__(
            self,
            team_one: List[PartyPokemon],
            team_two: List[PartyPokemon],
            agent_one: PlayerAgent,
            agent_two: PlayerAgent,
            max_allowed_turns: Optional[int] = 1000
    ):
        if not 1 <= len(team_one) <= 6:
            raise InvalidTeamSizeException(len(team_one))
        if not 1 <= len(team_two) <= 6:
            raise InvalidTeamSizeException(len(team_two))

        self.teams = (list(map(BattlingPokemon, team_one)), list(map(BattlingPokemon, team_two)))
        self.agents = (agent_one, agent_two)
        self.team_cursors: List[int] = [0, 0]
        self.__active_pokemon: List[ActivePokemon] = [ActivePokemon(self.teams[0][0]), ActivePokemon(self.teams[1][0])]

        self.__turn = 0
        self.__max_allowed_turns = max_allowed_turns
        self.victor: Optional[Player] = None

        self.__action_lock = Lock()
        self.__pending_actions: List[Optional[Action]] = [None, None]

        self.__switch_lock = Lock()
        self.__waiting_for_switch: List[bool] = [False, False]
        self.__pending_switches: List[Optional[Action]] = [None, None]

    @property
    def actives(self) -> List[ActivePokemon]:
        return [self.p1_active_pokemon, self.p2_active_pokemon]

    @property
    def p1_active_pokemon(self) -> ActivePokemon:
        return self.__active_pokemon[Player.P1]

    @property
    def p2_active_pokemon(self) -> ActivePokemon:
        return self.__active_pokemon[Player.P2]

    @property
    def p1_pending_action(self) -> Optional[Action]:
        return self.__pending_actions[Player.P1]

    @property
    def p2_pending_action(self) -> Optional[Action]:
        return self.__pending_actions[Player.P2]

    @property
    def turn(self) -> int:
        return self.__turn

    def increment_turn(self):
        self.__turn += 1

    def __switch_checks(self, player: Player, switch: Action):
        """Raises an exception if the pending switch is invalid.

        Args:
            player (Player): The Player whose pending action will be set.
            switch (Action): The switch that the player wishes to make.

        Raises:
            AlreadyInBattleException: The player is trying to switch to a Pokemon that is already active.
            NoPokemonInSlotException: The player is trying to switch to a slot that he or she has not filled.
            FaintedPokemonException: The player is trying to switch to a Pokemon that has fainted.
        """
        if SWITCH_SLOTS[switch] == self.team_cursors[player]:
            raise AlreadyInBattleException(self.__active_pokemon[player])
        if len(self.teams[player]) < SWITCH_SLOTS[switch] + 1:
            raise NoPokemonInSlotException(SWITCH_SLOTS[switch] + 1)
        if self.teams[player][SWITCH_SLOTS[switch]].knocked_out:
            raise FaintedPokemonException(self.teams[player][SWITCH_SLOTS[switch]])

    def set_pending_action(self, player: Player, action: Action):
        """Sets the Player's pending action to the given Action.

        Args:
            player (Player): The Player whose pending action should be set.
            action (Action): The Action that the player wishes to take.

        Raises:
            AlreadyInBattleException: The player is trying to switch to a Pokemon that is already active.
            NoPokemonInSlotException: The player is trying to switch to a slot that he or she has not filled.
            FaintedPokemonException: The player is trying to switch to a Pokemon that has fainted.
            NoMoveInSlotException: The player is trying to use a move slot that he or she has not filled.
            OutOfPPException: The player is trying to use a move that is out of PP.
        """
        if action.is_switch:
            self.__switch_checks(player, action)
        if action.is_move:
            if len(self.__active_pokemon[player].moves) < MOVE_SLOTS[action] + 1:
                raise NoMoveInSlotException(MOVE_SLOTS[action] + 1)
            if self.__active_pokemon[player].pp[MOVE_SLOTS[action]] == 0:
                raise OutOfPPException(self.teams[player][self.team_cursors[player]].pokemon.moves[MOVE_SLOTS[action]])

        self.__pending_actions[player] = action

        if None not in self.__pending_actions:
            self.__action_lock.release()

    def set_pending_switch(self, player, action: Action):
        """Sets the Player's pending switch to the given one.

        Args:
            player (Player): The Player whose pending action should be set.
            action (Action): The switch that the player wishes to make.

        Raises:
            SwitchNotRequestedException: The player is trying to make a switch when he or she has not been asked to.
            MoveNotSwitchException: The player is trying to make a move, not a switch.
            AlreadyInBattleException: The player is trying to switch to a Pokemon that is already active.
            NoPokemonInSlotException: The player is trying to switch to a slot that he or she has not filled.
            FaintedPokemonException: The player is trying to switch to a Pokemon that has fainted.
        """
        if not self.__waiting_for_switch[player]:
            raise SwitchNotRequestedException(player)
        if action.is_move:
            raise MoveNotSwitchException(player)
        self.__switch_checks(player, action)

        self.__pending_switches[player] = action

        unlock = True
        for waiting, switch in zip(self.__waiting_for_switch, self.__pending_switches):
            if waiting and switch is None:
                unlock = False
        if unlock:
            self.__switch_lock.release()

    def __execute_switch(self, player: Player, slot: int):
        """Executes the given player's pending switch.

        Args:
            player (Player): The player to switch.
            slot (int): The slot to switch to.
        """
        self.team_cursors[player] = slot
        self.__active_pokemon[player] = ActivePokemon(self.teams[player][slot])

    def __execute_action(self, player: Player):
        """Executes the given player's pending action.

        Args:
            player (Player): The player to move or switch.
        """
        action = self.p1_pending_action if player == Player.P1 else self.p2_pending_action
        active_pokemon = self.p1_active_pokemon if player == Player.P2 else self.p2_active_pokemon
        if action.is_switch:
            self.__execute_switch(player, SWITCH_SLOTS[self.__pending_actions[player]])
        else:
            active_pokemon.use_move(MOVE_SLOTS[action], self, player)

    def __first_to_move(self) -> Player:
        """Determines which player should move first in the coming turn.

        If a player is switching out, that player gets priority. If both are switching out, the player with the fastest
        active Pokemon switches first. If one player's pending move has a high priority then the other's, then he or she
        will move first. If both moves have the same priority, then the player with the faster active Pokemon moves
        first. Speed ties are broken randomly.

        Returns:
            Player: The Player who will move first this turn.
        """
        if self.p1_active_pokemon.speed > self.p2_active_pokemon.speed:
            faster_player = Player.P1
        elif self.p1_active_pokemon.speed < self.p2_active_pokemon.speed:
            faster_player = Player.P2
        else:
            faster_player = None
        rand_player = Player.P1 if np.random.choice((True, False)) else Player.P2

        if self.p1_pending_action.is_switch and self.p2_pending_action.is_switch:
            return faster_player if faster_player is not None else rand_player
        if self.p1_pending_action.is_switch:
            return Player.P1
        if self.p2_pending_action.is_switch:
            return Player.P2

        p1_priority = self.p1_active_pokemon.moves[MOVE_SLOTS[self.p1_pending_action]].priority
        p2_priority = self.p2_active_pokemon.moves[MOVE_SLOTS[self.p2_pending_action]].priority

        if p1_priority == p2_priority:
            return faster_player if faster_player is not None else rand_player
        if p1_priority > p2_priority:
            return Player.P1
        return Player.P2

    def __wait_for_switch(self, player: Player):
        """Require the given player to switch Pokemon.

        Args:
            player (Player): The player who must switch.
        """
        self.agents[player].notify_switch_required(self)
        self.__waiting_for_switch[player] = True
        if not self.__switch_lock.locked():
            self.__switch_lock.acquire()

    def __execute_actions(self):
        """Execute the pending actions for all players in sequence"""
        if None in self.__pending_actions:
            raise ActionNotSetException

        first_mover = self.__first_to_move()
        second_mover = first_mover.opponent

        self.__execute_action(first_mover)
        if not self.__active_pokemon[second_mover].knocked_out:
            self.__execute_action(second_mover)
        else:
            if all(map(lambda p: p.knocked_out, self.teams[second_mover])):
                self.victor = first_mover
                return

        if all(map(lambda p: p.knocked_out, self.teams[first_mover])):
            self.victor = second_mover
            return

        if self.p1_active_pokemon.knocked_out:
            self.__wait_for_switch(Player.P1)
        if self.p2_active_pokemon.knocked_out:
            self.__wait_for_switch(Player.P2)

    def __execute_switches(self):
        """Execute switches for any players with pending switches simultaneously."""
        for waiting, switch in zip(self.__waiting_for_switch, self.__pending_switches):
            if waiting and switch is None:
                raise SwitchNotSetException()
        for player, waiting, switch in zip(Battle.PLAYERS, self.__waiting_for_switch, self.__pending_switches):
            if waiting:
                self.__execute_switch(player, SWITCH_SLOTS[switch])
        self.__waiting_for_switch = list(map(lambda _: False, self.__waiting_for_switch))

    def play_turn(self):
        """Plays out one turn of the battle."""
        self.__turn += 1

        with self.__action_lock:
            # Execute switches and moves of the currently-active Pokemon.
            self.__execute_actions()

        if self.victor is not None:
            return

        with self.__switch_lock:
            # Replace any Pokemon that have fainted.
            self.__execute_switches()

        self.__action_lock.acquire()

    def __under_turn_max(self):
        return self.__max_allowed_turns is None or self.turn < self.__max_allowed_turns

    def play(self) -> Tuple[Optional[Player], int]:
        """Plays out the entire battle to completion.

        Returns:
            Optional[Player]: The winner of the battle.
            int: The turn count of the battle.
        """
        self.__action_lock.acquire()

        while self.victor is None and self.__under_turn_max():
            self.play_turn()

        return self.victor, self.turn
