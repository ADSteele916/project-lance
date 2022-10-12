"""Functionality for logging battles turn-by-turn"""

from typing import List


class BattleLog:
    """Stores a log of what actions occurred in each turn of a battle."""

    def __init__(self):
        self._turn = 0
        self._log: List[List[str]] = []

    def advance_turn(self):
        self._turn += 1
        self._log.append([])

    def log(self, log_entry: str):
        self._log[self._turn - 1].append(log_entry)

    def get_log(self) -> List[List[str]]:
        return [l.copy() for l in self._log]
