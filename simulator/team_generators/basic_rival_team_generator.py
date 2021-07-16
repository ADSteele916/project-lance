"""A team generator that creates single-Pokemon teams consisting of the Kanto starters."""

from random import shuffle

from simulator.dex.movedex import MOVEDEX
from simulator.dex.pokedex import POKEDEX
from simulator.pokemon.party_pokemon import PartyPokemon
from simulator.team_generators.team_generator import NoMorePossibleTeamsException, TeamGenerator


class BasicRivalTeamGenerator(TeamGenerator):
    """A team generator that produces single-Pokemon teams.

    The Pokemon in each team is based on Blue's starters' level and movesets in the Cerulean City rival battle in the
    original Pokemon Red and Blue, to ensure that every starter has a STAB move. DVs and STAT EXPs are at their
    maximums.
    """

    MAX_ALLOWED_TEAMS = 3
    STARTERS = {
            PartyPokemon(
                    POKEDEX["Bulbasaur"],
                    17,
                    [
                            MOVEDEX["Tackle"],
                            MOVEDEX["Growl"],
                            MOVEDEX["Leech Seed"],
                            MOVEDEX["Vine Whip"]
                    ]
            ),
            PartyPokemon(
                    POKEDEX["Charmander"],
                    17,
                    [MOVEDEX["Scratch"],
                     MOVEDEX["Growl"],
                     MOVEDEX["Ember"],
                     MOVEDEX["Leer"]]
            ),
            PartyPokemon(
                    POKEDEX["Squirtle"],
                    17,
                    [MOVEDEX["Tackle"],
                     MOVEDEX["Tail Whip"],
                     MOVEDEX["Bubble"],
                     MOVEDEX["Water Gun"]]
            )
    }

    def generate_team(self):
        starters = list(self.STARTERS)
        shuffle(starters)
        if len(self.generated_teams) < self.MAX_ALLOWED_TEAMS:
            for starter in starters:
                valid = True
                for team in self.generated_teams:
                    if starter in team:
                        valid = False
                if valid:
                    self.generated_teams.append([starter])
                    return [starter]
        raise NoMorePossibleTeamsException()
