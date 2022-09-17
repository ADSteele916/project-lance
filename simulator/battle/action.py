"""Data structures for selecting which actions players will take."""

from enum import auto
from enum import Enum


class Action(Enum):
    """An action that a player can take on his or her turn."""

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
        return self in (Action.MOVE_1, Action.MOVE_2, Action.MOVE_3,
                        Action.MOVE_4)

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


MOVE_SLOTS = {
    Action.MOVE_1: 0,
    Action.MOVE_2: 1,
    Action.MOVE_3: 2,
    Action.MOVE_4: 3
}
SWITCH_SLOTS = {
    Action.SWITCH_1: 0,
    Action.SWITCH_2: 1,
    Action.SWITCH_3: 2,
    Action.SWITCH_4: 3,
    Action.SWITCH_5: 4,
    Action.SWITCH_6: 5,
}
