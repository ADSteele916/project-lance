"""Dataclass for and instances of rulesets for various Battle formats."""

import dataclasses
import warnings
from typing import List, Optional, Set

from simulator.dex.movedex import MOVEDEX
from simulator.dex.pokedex import POKEDEX
from simulator.moves.move import Move
from simulator.pokemon.party_pokemon import PartyPokemon
from simulator.pokemon.pokemon_species import PokemonSpecies


@dataclasses.dataclass(frozen=True)
class Ruleset:
    """A set of parameters specifying the rules for a Battle."""

    pokedex: Set[PokemonSpecies] = dataclasses.field(
        default_factory=lambda: set(POKEDEX.values())
    )
    movedex: Set[Move] = dataclasses.field(
        default_factory=lambda: set(MOVEDEX.values())
    )
    max_team_size: int = 6
    max_turns: Optional[int] = 1000
    use_pp: bool = True
    deterministic_damage: bool = False
    accuracy_checks: bool = True
    sleep_clause: bool = True
    freeze_clause: bool = True
    species_clause: bool = True
    ohko_clause: bool = True
    evasion_clause: bool = True

    def __post_init__(self):
        if not set() < self.pokedex <= set(POKEDEX.values()):
            raise ValueError(
                "Pokedex must be a non-empty subset of Generation 1 Pokedex."
            )
        if not set() < self.movedex <= set(MOVEDEX.values()):
            raise ValueError(
                "Movedex must be a non-empty subset of Generation 1 Movedex."
            )
        if (MOVEDEX["Struggle"] not in self.movedex) and self.use_pp:
            raise ValueError("Struggle must be usable if PP are being used.")
        for pokemon in self.pokedex:
            if not any(move in self.movedex for move in pokemon.moveset):
                warnings.warn(
                    f"{pokemon} cannot learn any of the allowed moves.", stacklevel=3
                )
        if not 1 <= self.max_team_size <= 6:
            raise ValueError("The maximum size of teams must be between 1 and 6.")
        if self.max_turns is not None and self.max_turns <= 0:
            raise ValueError("Maximum turns must be positive")

    def pokemon_is_legal(self, pokemon: PartyPokemon):
        if pokemon.species not in self.pokedex:
            return False
        if any(m not in self.movedex for m in pokemon.moves):
            return False
        return True

    def team_is_valid(self, team: List[PartyPokemon]):
        if not 1 <= len(team) <= self.max_team_size:
            return False
        if self.species_clause and (len(set(p.species for p in team)) < len(team)):
            return False
        return all(self.pokemon_is_legal(p) for p in team)


FULL_RULESET = Ruleset()
