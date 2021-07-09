"""Functionality related to Pokemon types and their interactions."""

from enum import Enum, auto

import numpy as np


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


__WEAK = 2.0
__RESIST = 0.5
__IMMUNE = 0.0

__ATTACK_EFFECTIVENESS = {
        Type.NORMAL: {
                Type.ROCK: __RESIST,
                Type.GHOST: __IMMUNE
        },
        Type.FIGHTING: {
                Type.NORMAL: __WEAK,
                Type.FLYING: __RESIST,
                Type.POISON: __RESIST,
                Type.ROCK: __WEAK,
                Type.BUG: __RESIST,
                Type.GHOST: __IMMUNE,
                Type.PSYCHIC: __RESIST,
                Type.ICE: __WEAK,
        },
        Type.FLYING: {
                Type.FIGHTING: __WEAK,
                Type.ROCK: __RESIST,
                Type.BUG: __WEAK,
                Type.GRASS: __WEAK,
                Type.ELECTRIC: __RESIST,
        },
        Type.POISON: {
                Type.POISON: __RESIST,
                Type.GROUND: __RESIST,
                Type.ROCK: __RESIST,
                Type.BUG: __WEAK,
                Type.GHOST: __RESIST,
                Type.GRASS: __WEAK,
        },
        Type.GROUND: {
                Type.FLYING: __IMMUNE,
                Type.POISON: __WEAK,
                Type.ROCK: __WEAK,
                Type.BUG: __RESIST,
                Type.FIRE: __WEAK,
                Type.GRASS: __RESIST,
                Type.ELECTRIC: __WEAK,
        },
        Type.ROCK: {
                Type.FIGHTING: __RESIST,
                Type.FLYING: __WEAK,
                Type.GROUND: __RESIST,
                Type.BUG: __WEAK,
                Type.FIRE: __WEAK,
                Type.ICE: __WEAK,
        },
        Type.BUG: {
                Type.FIGHTING: __RESIST,
                Type.FLYING: __RESIST,
                Type.POISON: __WEAK,
                Type.GHOST: __RESIST,
                Type.FIRE: __RESIST,
                Type.GRASS: __WEAK,
                Type.PSYCHIC: __WEAK,
        },
        Type.GHOST: {
                Type.NORMAL: __IMMUNE,
                Type.GHOST: __WEAK,
                Type.PSYCHIC: __IMMUNE
        },
        Type.FIRE: {
                Type.ROCK: __RESIST,
                Type.BUG: __WEAK,
                Type.FIRE: __RESIST,
                Type.WATER: __RESIST,
                Type.GRASS: __WEAK,
                Type.ICE: __WEAK,
                Type.DRAGON: __RESIST,
        },
        Type.WATER: {
                Type.GROUND: __WEAK,
                Type.ROCK: __WEAK,
                Type.FIRE: __WEAK,
                Type.WATER: __RESIST,
                Type.GRASS: __RESIST,
                Type.DRAGON: __RESIST,
        },
        Type.GRASS: {
                Type.FLYING: __RESIST,
                Type.POISON: __RESIST,
                Type.GROUND: __WEAK,
                Type.ROCK: __WEAK,
                Type.BUG: __RESIST,
                Type.FIRE: __RESIST,
                Type.WATER: __WEAK,
                Type.GRASS: __RESIST,
                Type.DRAGON: __RESIST,
        },
        Type.ELECTRIC: {
                Type.FLYING: __WEAK,
                Type.GROUND: __IMMUNE,
                Type.WATER: __WEAK,
                Type.GRASS: __RESIST,
                Type.ELECTRIC: __RESIST,
                Type.DRAGON: __RESIST,
        },
        Type.PSYCHIC: {
                Type.FIGHTING: __WEAK,
                Type.POISON: __WEAK,
                Type.PSYCHIC: __RESIST
        },
        Type.ICE: {
                Type.FLYING: __WEAK,
                Type.GROUND: __WEAK,
                Type.WATER: __RESIST,
                Type.GRASS: __WEAK,
                Type.ICE: __RESIST,
                Type.DRAGON: __WEAK,
        },
        Type.DRAGON: {
                Type.DRAGON: __WEAK
        },
}


def __gen_types_chart() -> np.ndarray:
    """Uses the __ATTACK_EFFECTIVENESS constant to generate a table of type effectiveness matchups.

    Returns:
        np.ndarray: A 15 by 15 table of effectiveness multipliers where rows are attacking types and cols are
            defending types.
    """
    types = list(Type)
    chart = np.ones((15, 15))

    for idx, pokemon_type in enumerate(types):
        for special_type, effectiveness in __ATTACK_EFFECTIVENESS[pokemon_type].items():
            chart[idx, types.index(special_type)] = effectiveness

    return chart


EFFECTIVENESS_CHART = __gen_types_chart()


def get_attack_effectiveness(attacking_type: Type, defending_type: Type) -> float:
    """Uses the EFFECTIVENESS_CHART to look up the type multiplier for the given attacking and defending types.

    Args:
        attacking_type (Type): The type of the attack being used.
        defending_type (Type): The type of the target of the attack.

    Returns:
        float: The type effectiveness multiplier for the given types.
    """
    types = list(Type)
    return EFFECTIVENESS_CHART[types.index(attacking_type), types.index(defending_type)]
