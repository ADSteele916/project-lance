"""Representation of a Base Pokemon, without any DVs or EVs."""
from typing import TYPE_CHECKING, Optional, Set

import numpy as np

from simulator.type import Type, get_attack_effectiveness

if TYPE_CHECKING:
    from simulator.moves.move import Move


class InvalidBaseStatException(Exception):

    def __init__(self, invalid_stat: int):
        super().__init__(f"{invalid_stat} is an invalid base stat. It must be representable as a single unsigned byte.")


class PokemonSpecies:
    """A Pokemon species with a name, dex number, base stats, type(s), and a moveset."""

    def __init__(
            self,
            name: str,
            dex_num: int,
            base_hp: int,
            base_atk: int,
            base_def: int,
            base_spe: int,
            base_spc: int,
            moveset: Set["Move"],
            primary_type: Type,
            secondary_type: Optional[Type] = None,
    ):
        for stat in (base_hp, base_atk, base_def, base_spe, base_spc):
            if not 0 <= stat <= 255:
                raise InvalidBaseStatException(stat)
        self.name = name
        self.dex_num = dex_num
        self.base_hp = base_hp
        self.base_atk = base_atk
        self.base_def = base_def
        self.base_spe = base_spe
        self.base_spc = base_spc
        self.moveset = moveset
        self.primary_type = primary_type
        self.secondary_type = secondary_type

    def __str__(self):
        return self.name

    def attack_effectiveness(self, attacking_type: Type) -> float:
        """Produces the type effectiveness of a given attack type against this Pokemon.

        Args:
            attacking_type (Type): The type of the attack being used.

        Returns:
            float: The damage multiplier for the given attack type.
        """
        if self.secondary_type is not None:
            return get_attack_effectiveness(attacking_type,
                                            self.primary_type
                                            ) * get_attack_effectiveness(attacking_type,
                                                                         self.secondary_type)
        return get_attack_effectiveness(attacking_type, self.primary_type)

    def critical_hit_threshold(self, high_crit_ratio: bool = False, focus_energy: bool = False) -> int:
        """Produces the critical hit threshold for this Pokemon under certain conditions.

        Note that Focus Energy will actually reduce the critical hit ratio, due to a bug in the original games.

        Args:
            high_crit_ratio (bool): Whether or not the move used has a high critical hit ratio (Slash, etc.).
            focus_energy (bool): Whether or not the user has the effects of Focus Energy.

        Returns:
            int: Number between 0 and 255 used as a maximum for a random int to calculate a critical hit.
        """
        if not high_crit_ratio and not focus_energy:
            return np.floor(self.base_spe / 2)
        if not high_crit_ratio:
            return np.floor(self.base_spe / 8)
        if not focus_energy:
            return min(8 * np.floor(self.base_spe / 2), 255)
        return 4 * np.floor(self.base_spe / 4)
