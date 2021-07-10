"""Functionality for a Battle between two Pokemon teams, with user input for both sides."""

from enum import Enum, IntEnum, auto
from typing import List, Optional, Tuple

from simulator.battle.active_pokemon import ActivePokemon
from simulator.battle.battling_pokemon import BattlingPokemon
from simulator.pokemon.party_pokemon import PartyPokemon


class Action(Enum):
    """An action (either making a move or switching) that a Player can take on his or her turn."""

    MOVE_1 = auto()
    MOVE_2 = auto()
    MOVE_3 = auto()
    MOVE_4 = auto()
    SWITCH_1 = auto()
    SWITCH_2 = auto()
    SWITCH_3 = auto()
    SWITCH_4 = auto()
    SWITCH_5 = auto()
    SWITCH_6 = auto()

    @property
    def is_move(self):
        return self in (Action.MOVE_1, Action.MOVE_2, Action.MOVE_3, Action.MOVE_4)

    @property
    def is_switch(self):
        return self in (
                Action.SWITCH_1,
                Action.SWITCH_2,
                Action.SWITCH_3,
                Action.SWITCH_4,
                Action.SWITCH_5,
                Action.SWITCH_6,
        )


MOVE_SLOTS = {Action.MOVE_1: 0, Action.MOVE_2: 1, Action.MOVE_3: 2, Action.MOVE_4: 3}
SWITCH_SLOTS = {
        Action.SWITCH_1: 0,
        Action.SWITCH_2: 1,
        Action.SWITCH_3: 2,
        Action.SWITCH_4: 3,
        Action.SWITCH_5: 4,
        Action.SWITCH_6: 5,
}


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


class Battle:
    """A Pokemon battle with all state information for both teams"""

    def __init__(
            self,
            team_one: List[PartyPokemon],
            team_two: List[PartyPokemon],
    ):
        if not 1 <= len(team_one) <= 6:
            raise InvalidTeamSizeException(len(team_one))
        if not 1 <= len(team_two) <= 6:
            raise InvalidTeamSizeException(len(team_two))

        self.teams = (list(map(BattlingPokemon, team_one)), list(map(BattlingPokemon, team_two)))
        self.team_cursors = (0, 0)
        self.active_pokemon = (ActivePokemon(self.teams[0][0]), ActivePokemon(self.teams[1][0]))
        self.__pending_actions: Tuple[Optional[Action], Optional[Action]] = (None, None)
        self.turn = 1

    @property
    def p1_active_pokemon(self) -> ActivePokemon:
        return self.active_pokemon[Player.P1]

    @property
    def p2_active_pokemon(self) -> ActivePokemon:
        return self.active_pokemon[Player.P2]

    def unset_pending_action(self, player: Player):
        """Unsets the Player's pending action.

        Args:
            player (Player): The Player whose pending action should be unset.
        """
        if player == Player.P1:
            self.__pending_actions = (None, self.__pending_actions[1])
        else:
            self.__pending_actions = (self.__pending_actions[0], None)

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
            if SWITCH_SLOTS[action] == self.team_cursors[player]:
                raise AlreadyInBattleException(self.active_pokemon[player])
            if len(self.teams[player]) < SWITCH_SLOTS[action] + 1:
                raise NoPokemonInSlotException(SWITCH_SLOTS[action] + 1)
            if self.teams[player][SWITCH_SLOTS[action]].knocked_out:
                raise FaintedPokemonException(self.teams[player][SWITCH_SLOTS[action]])
        if action.is_move:
            if len(self.active_pokemon[player].moves) < MOVE_SLOTS[action] + 1:
                raise NoMoveInSlotException(MOVE_SLOTS[action] + 1)
            if self.active_pokemon[player].pp[MOVE_SLOTS[action]] == 0:
                raise OutOfPPException(self.teams[player][self.team_cursors[player]].pokemon.moves[MOVE_SLOTS[action]])

        if player == Player.P1:
            self.__pending_actions = (action, self.__pending_actions[1])
        else:
            self.__pending_actions = (self.__pending_actions[0], action)
