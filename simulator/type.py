"""Functionality related to Pokemon types and their interactions."""

from enum import auto
from enum import Enum


class Type(Enum):
    """Type of a Pokemon or of a move."""

    NORMAL = auto()
    FIGHTING = auto()
    FLYING = auto()
    POISON = auto()
    GROUND = auto()
    ROCK = auto()
    BUG = auto()
    GHOST = auto()
    FIRE = auto()
    WATER = auto()
    GRASS = auto()
    ELECTRIC = auto()
    PSYCHIC = auto()
    ICE = auto()
    DRAGON = auto()

    @property
    def is_physical(self) -> bool:
        """Determines whether this Type has physical attacks.

        Returns:
            bool: Whether or not this Type has physical attacks.
        """
        return self in (
            Type.NORMAL,
            Type.FIGHTING,
            Type.FLYING,
            Type.POISON,
            Type.GROUND,
            Type.ROCK,
            Type.BUG,
            Type.GHOST,
        )

    @property
    def is_special(self) -> bool:
        """Determines whether this Type has special attacks.

        Returns:
            bool: Whether or not this Type has special attacks.
        """
        return self in (
            Type.FIRE,
            Type.WATER,
            Type.GRASS,
            Type.ELECTRIC,
            Type.PSYCHIC,
            Type.ICE,
            Type.DRAGON,
        )


_WEAK = 2.0
_RESIST = 0.5
_IMMUNE = 0.0

_ATTACK_EFFECTIVENESS = {
    Type.NORMAL: {
        Type.ROCK: _RESIST,
        Type.GHOST: _IMMUNE
    },
    Type.FIGHTING: {
        Type.NORMAL: _WEAK,
        Type.FLYING: _RESIST,
        Type.POISON: _RESIST,
        Type.ROCK: _WEAK,
        Type.BUG: _RESIST,
        Type.GHOST: _IMMUNE,
        Type.PSYCHIC: _RESIST,
        Type.ICE: _WEAK,
    },
    Type.FLYING: {
        Type.FIGHTING: _WEAK,
        Type.ROCK: _RESIST,
        Type.BUG: _WEAK,
        Type.GRASS: _WEAK,
        Type.ELECTRIC: _RESIST,
    },
    Type.POISON: {
        Type.POISON: _RESIST,
        Type.GROUND: _RESIST,
        Type.ROCK: _RESIST,
        Type.BUG: _WEAK,
        Type.GHOST: _RESIST,
        Type.GRASS: _WEAK,
    },
    Type.GROUND: {
        Type.FLYING: _IMMUNE,
        Type.POISON: _WEAK,
        Type.ROCK: _WEAK,
        Type.BUG: _RESIST,
        Type.FIRE: _WEAK,
        Type.GRASS: _RESIST,
        Type.ELECTRIC: _WEAK,
    },
    Type.ROCK: {
        Type.FIGHTING: _RESIST,
        Type.FLYING: _WEAK,
        Type.GROUND: _RESIST,
        Type.BUG: _WEAK,
        Type.FIRE: _WEAK,
        Type.ICE: _WEAK,
    },
    Type.BUG: {
        Type.FIGHTING: _RESIST,
        Type.FLYING: _RESIST,
        Type.POISON: _WEAK,
        Type.GHOST: _RESIST,
        Type.FIRE: _RESIST,
        Type.GRASS: _WEAK,
        Type.PSYCHIC: _WEAK,
    },
    Type.GHOST: {
        Type.NORMAL: _IMMUNE,
        Type.GHOST: _WEAK,
        Type.PSYCHIC: _IMMUNE
    },
    Type.FIRE: {
        Type.ROCK: _RESIST,
        Type.BUG: _WEAK,
        Type.FIRE: _RESIST,
        Type.WATER: _RESIST,
        Type.GRASS: _WEAK,
        Type.ICE: _WEAK,
        Type.DRAGON: _RESIST,
    },
    Type.WATER: {
        Type.GROUND: _WEAK,
        Type.ROCK: _WEAK,
        Type.FIRE: _WEAK,
        Type.WATER: _RESIST,
        Type.GRASS: _RESIST,
        Type.DRAGON: _RESIST,
    },
    Type.GRASS: {
        Type.FLYING: _RESIST,
        Type.POISON: _RESIST,
        Type.GROUND: _WEAK,
        Type.ROCK: _WEAK,
        Type.BUG: _RESIST,
        Type.FIRE: _RESIST,
        Type.WATER: _WEAK,
        Type.GRASS: _RESIST,
        Type.DRAGON: _RESIST,
    },
    Type.ELECTRIC: {
        Type.FLYING: _WEAK,
        Type.GROUND: _IMMUNE,
        Type.WATER: _WEAK,
        Type.GRASS: _RESIST,
        Type.ELECTRIC: _RESIST,
        Type.DRAGON: _RESIST,
    },
    Type.PSYCHIC: {
        Type.FIGHTING: _WEAK,
        Type.POISON: _WEAK,
        Type.PSYCHIC: _RESIST
    },
    Type.ICE: {
        Type.FLYING: _WEAK,
        Type.GROUND: _WEAK,
        Type.WATER: _RESIST,
        Type.GRASS: _WEAK,
        Type.ICE: _RESIST,
        Type.DRAGON: _WEAK,
    },
    Type.DRAGON: {
        Type.DRAGON: _WEAK
    },
}


def get_attack_effectiveness(attacking_type: Type,
                             defending_type: Type) -> float:
    """Looks up the type multiplier for the given attacking and defending types.

    Args:
        attacking_type: The type of the attack being used.
        defending_type: The type of the target of the attack.

    Returns:
        float: The type effectiveness multiplier for the given types.
    """
    try:
        return _ATTACK_EFFECTIVENESS[attacking_type][defending_type]
    except KeyError:
        return 1.0
