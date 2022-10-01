"""Functionality for a Battle between two Pokemon teams, with user input."""

from enum import auto
from enum import Enum
from enum import IntEnum
import random
from typing import List, Optional, Tuple, TYPE_CHECKING

from simulator.battle.action import Action
from simulator.battle.active_pokemon import ActivePokemon
from simulator.battle.battling_pokemon import BattlingPokemon
from simulator.pokemon.party_pokemon import PartyPokemon

if TYPE_CHECKING:
    from simulator.agents.agent import Agent


class Player(IntEnum):
    """Indices for various tuples and 2-element lists in Battle"""

    P1 = 0
    P2 = 1

    @property
    def opponent(self) -> "Player":
        return Player.P1 if self == Player.P2 else Player.P2


class Result(Enum):
    """Possible outcomes of a battle"""

    P1_WIN = Player.P1
    P2_WIN = Player.P2
    DRAW = auto()

    @property
    def victor(self) -> Optional[Player]:
        if self == Result.DRAW:
            return None
        return Player.P1 if self == Result.P1_WIN else Player.P2


class InvalidTeamSizeException(Exception):

    def __init__(self, size: int):
        super().__init__(
            f"{size} is an invalid team size. Teams must have between 1 and 6 "
            f"members.")


class Battle:
    """A Pokemon battle with all state information for both teams"""

    def __init__(self,
                 team_one: List[PartyPokemon],
                 team_two: List[PartyPokemon],
                 agent_one: "Agent",
                 agent_two: "Agent",
                 max_allowed_turns: Optional[int] = 1000):
        if not 1 <= len(team_one) <= 6:
            raise InvalidTeamSizeException(len(team_one))
        if not 1 <= len(team_two) <= 6:
            raise InvalidTeamSizeException(len(team_two))

        self.teams = ([BattlingPokemon(p) for p in team_one],
                      [BattlingPokemon(p) for p in team_two])
        self.agents: Tuple["Agent", "Agent"] = (agent_one, agent_two)
        self.team_cursors: List[int] = [0, 0]
        self._actives: List[ActivePokemon] = [
            ActivePokemon(self.teams[0][0]),
            ActivePokemon(self.teams[1][0])
        ]

        self._turn = 0
        self._max_allowed_turns = max_allowed_turns
        self.result: Optional[Result] = None

    @property
    def p1_agent(self) -> "Agent":
        return self.agents[Player.P1]

    @property
    def p2_agent(self) -> "Agent":
        return self.agents[Player.P2]

    @property
    def p1_active_pokemon(self) -> ActivePokemon:
        return self._actives[Player.P1]

    @property
    def p2_active_pokemon(self) -> ActivePokemon:
        return self._actives[Player.P2]

    @property
    def p1_team(self) -> List[BattlingPokemon]:
        return self.teams[Player.P1]

    @property
    def p2_team(self) -> List[BattlingPokemon]:
        return self.teams[Player.P2]

    @property
    def actives(self) -> Tuple[ActivePokemon, ActivePokemon]:
        return self.p1_active_pokemon, self.p2_active_pokemon

    @property
    def turn(self) -> int:
        return self._turn

    def increment_turn(self):
        self._turn += 1

    def validate_switch(self, player: Player, switch: Action) -> bool:
        """Checks whether the given switch can be executed.

        Returns False if the given action is a move.

        Returns False if the player is trying to switch to a Pokemon that is
        already active, trying to switch to a slot that he or she has not,
        filled, or trying to switch to a Pokemon that has fainted.

        Args:
            player: The Player whose pending action will be set.
            switch: The switch that the player wishes to make.

        Returns:
            Whether the pending switch is valid.
        """
        if switch.is_move:
            return False
        if switch.switch_slot == self.team_cursors[player]:
            return False
        if len(self.teams[player]) <= switch.switch_slot:
            return False
        if self.teams[player][switch.switch_slot].knocked_out:
            return False
        return True

    def request_switch(self, player: Player) -> Action:
        choices = [s for s in Action if self.validate_switch(player, s)]
        switch = self.agents[player].request_switch(self, player, choices)
        assert self.validate_switch(player, switch)
        return switch

    def validate_action(self, player: Player, action: Action) -> bool:
        """Checks whether the given action can be executed.

        In addition to the checks performed for switches in validate_switch,
        returns False if the player is trying to use a move slot that he or she
        has not filled or use a move that is out of PP without having to
        Struggle.

        Args:
            player: The Player whose pending action should be set.
            action: The Action that the player wishes to take.

        Returns:
            Whether the pending action is valid.
        """
        if action.is_switch:
            return self.validate_switch(player, action)
        if len(self._actives[player].moves) <= action.move_slot:
            return False
        if (self.actives[player].pp[action.move_slot] == 0 and
                not all(pp is None or pp == 0
                        for pp in self.actives[player].pp)):
            return False
        return True

    def request_action(self, player: Player) -> Action:
        choices = [a for a in Action if self.validate_action(player, a)]
        action = self.agents[player].request_action(self, player, choices)
        assert self.validate_action(player, action)
        return action

    def _execute_switch(self, player: Player, action: Action):
        """Executes the given player's pending switch.

        Args:
            player: The player to switch.
            action: The switch Action to take.
        """
        assert action.is_switch
        slot = action.switch_slot
        self.team_cursors[player] = slot
        self._actives[player] = ActivePokemon(self.teams[player][slot])

    def _execute_action(self, player: Player, action: Action):
        """Executes the given player's pending action.

        Args:
            player: The player to move or switch.
            action: The Action the player will take.
        """

        active_pokemon = self.actives[player]

        if action.is_switch:
            self._execute_switch(player, action)
        else:
            active_pokemon.use_move(action.move_slot, self, player)

    def _first_to_move(self, p1_action: Action, p2_action: Action) -> Player:
        """Determines which player should move first in the coming turn.

        If a player is switching out, that player gets priority. If both are
        switching out, the player with the fastest active Pokemon switches
        first. If one player's pending move has a high priority then the
        other's, then he or she will move first. If both moves have the same
        priority, then the player with the faster active Pokemon moves first.
        Speed ties are broken randomly.

        Returns:
            The Player who will move first this turn.
        """

        if self.p1_active_pokemon.speed > self.p2_active_pokemon.speed:
            faster_player = Player.P1
        elif self.p1_active_pokemon.speed < self.p2_active_pokemon.speed:
            faster_player = Player.P2
        else:
            faster_player = (Player.P1 if random.choice(
                (True, False)) else Player.P2)

        if p1_action.is_switch and p2_action.is_switch:
            return faster_player
        if p1_action.is_switch:
            return Player.P1
        if p2_action.is_switch:
            return Player.P2

        p1_priority = self.p1_active_pokemon.moves[p1_action.move_slot].priority
        p2_priority = self.p2_active_pokemon.moves[p2_action.move_slot].priority

        if p1_priority < p2_priority:
            return Player.P2
        if p1_priority > p2_priority:
            return Player.P1
        return faster_player

    def _execute_actions(self, p1_action: Action, p2_action: Action):
        """Execute the pending actions for all players in sequence"""

        first_mover = self._first_to_move(p1_action, p2_action)
        second_mover = first_mover.opponent

        if first_mover == Player.P1:
            first_action = p1_action
            second_action = p2_action
        else:
            first_action = p2_action
            second_action = p1_action

        self._execute_action(first_mover, first_action)
        if not any(pokemon.knocked_out for pokemon in self.actives):
            self._execute_action(second_mover, second_action)

    def _end_of_turn(self):
        for pokemon in self._actives:
            pokemon.flinch = False

        if self.p1_active_pokemon.toxic_counter is not None:
            self.p1_active_pokemon.toxic_counter += 1
        if self.p2_active_pokemon.toxic_counter is not None:
            self.p2_active_pokemon.toxic_counter += 1

    def _update_result(self):
        p1_eliminated = all(pokemon.knocked_out for pokemon in self.p1_team)
        p2_eliminated = all(pokemon.knocked_out for pokemon in self.p2_team)
        if p1_eliminated and p2_eliminated:
            self.result = Result.DRAW
        elif p1_eliminated:
            self.result = Result.P2_WIN
        elif p2_eliminated:
            self.result = Result.P1_WIN

    def play_turn(self):
        """Plays out one turn of the battle."""

        p1_action = self.request_action(Player.P1)
        p2_action = self.request_action(Player.P2)

        self._execute_actions(p1_action, p2_action)

        self._update_result()
        if self.result is not None:
            return

        self._end_of_turn()

        self._update_result()
        if self.result is not None:
            return

        if self.p1_active_pokemon.knocked_out:
            p1_switch = self.request_action(Player.P1)
            self._execute_switch(Player.P1, p1_switch)
        if self.p1_active_pokemon.knocked_out:
            p2_switch = self.request_action(Player.P2)
            self._execute_switch(Player.P2, p2_switch)

    def _under_turn_max(self):
        return (self._max_allowed_turns is None or
                self.turn < self._max_allowed_turns)

    def play(self) -> Tuple[Optional[Player], int]:
        """Plays out the entire battle to completion.

        Returns:
            The winner and the turn count of the battle.
        """

        while self.result is None and self._under_turn_max():
            self.increment_turn()
            self.play_turn()

        if self.result is None:
            self.result = Result.DRAW

        return self.result.victor, self.turn
