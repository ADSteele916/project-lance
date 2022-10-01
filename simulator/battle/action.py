"""Data structures for selecting which actions players will take."""

from enum import IntEnum


class Action(IntEnum):
    """An action that a player can take on his or her turn."""

    MOVE_1 = 0
    MOVE_2 = 1
    MOVE_3 = 2
    MOVE_4 = 3
    SWITCH_1 = 4
    SWITCH_2 = 5
    SWITCH_3 = 6
    SWITCH_4 = 7
    SWITCH_5 = 8
    SWITCH_6 = 9

    @property
    def is_move(self) -> bool:
        return self <= 3

    @property
    def is_switch(self) -> bool:
        return self >= 4

    @property
    def move_slot(self) -> int:
        assert self.is_move
        return self

    @property
    def switch_slot(self):
        assert self.is_switch
        return self - 4
