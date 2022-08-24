"""Classes for moves that cannot be generalized into a category."""

from typing import TYPE_CHECKING

from simulator.moves.damaging_move import DamagingMove
from simulator.moves.move import Move
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
