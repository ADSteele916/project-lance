"""Specification for a class that can generate team rosters."""

from abc import ABCMeta
from abc import abstractmethod


class NoMorePossibleTeamsException(Exception):
    pass


class TeamGenerator(metaclass=ABCMeta):
    """Abstract class for a Pokemon team generator."""

    MAX_ALLOWED_TEAMS = 2

    def __init__(self):
        self.generated_teams = []

    @abstractmethod
    def generate_team(self):
        pass

    def reset(self):
        self.generated_teams = []
