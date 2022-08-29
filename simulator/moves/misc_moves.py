"""Classes for moves that cannot be generalized into a category."""

from math import floor
from random import randint
from typing import TYPE_CHECKING

from simulator.moves.damaging_move import DamagingMove
from simulator.moves.move import Move
from simulator.status import Status
from simulator.type import Type

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class ConstantDamageMove(DamagingMove):

    @staticmethod
    def is_critical_hit(attacker: "ActivePokemon") -> bool:
        return False

    def get_damage(self, attacker: "ActivePokemon", target: "ActivePokemon", critical: bool) -> int:
        return self.power


class LevelDamagingMove(DamagingMove):

    @staticmethod
    def is_critical_hit(attacker: "ActivePokemon") -> bool:
        return False

    def get_damage(self, attacker: "ActivePokemon", target: "ActivePokemon", critical: bool) -> int:
        return attacker.pokemon.pokemon.level


class LeechSeed(Move):
    """Applies the leech seed volatile status condition to its target."""

    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        if Type.GRASS in (
                target.pokemon.pokemon.species.primary_type,
                target.pokemon.pokemon.species.secondary_type
        ) and not target.leech_seed:
            target.leech_seed = True


class Mist(Move):

    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        attacker.mist = True


class Psywave(DamagingMove):

    @staticmethod
    def is_critical_hit(attacker: "ActivePokemon") -> bool:
        return False

    def get_damage(self, attacker: "ActivePokemon", target: "ActivePokemon", critical: bool) -> int:
        max_damage = max(floor(1.5 * attacker.pokemon.pokemon.level - 1), 1)
        return randint(0, max_damage)


class Toxic(Move):

    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        if Type.POISON not in (
                target.pokemon.pokemon.species.primary_type,
                target.pokemon.pokemon.species.secondary_type
        ) and not target.status:
            target.status = Status.POISON
            target.toxic_counter = 1
