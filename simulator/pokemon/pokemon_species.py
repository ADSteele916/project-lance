"""Representation of a Base Pokemon, without any DVs or EVs."""

from math import floor, prod
from typing import TYPE_CHECKING, Optional, Set

from simulator.type import Type, get_attack_effectiveness

if TYPE_CHECKING:
    from simulator.moves.move import Move


class InvalidBaseStatException(Exception):
    def __init__(self, invalid_stat: int):
        super().__init__(
            f"{invalid_stat} is an invalid base stat. It must be representable "
            f"as a single unsigned byte."
        )


class PokemonSpecies:
    """A Pokemon species with name, number, base stats, type(s), and moveset."""

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

        self.name = name
        self.dex_num = dex_num

        for stat in (base_hp, base_atk, base_def, base_spe, base_spc):
            if not 0 <= stat <= 255:
                raise InvalidBaseStatException(stat)
        self.base_hp = base_hp
        self.base_atk = base_atk
        self.base_def = base_def
        self.base_spe = base_spe
        self.base_spc = base_spc
        self.moveset = moveset
        self.primary_type = primary_type
        self.secondary_type = secondary_type
        self.types = (
            [self.primary_type]
            if self.secondary_type is None
            else [self.primary_type, self.secondary_type]
        )

        self._effectivenesses = {
            attacking_type: prod(
                get_attack_effectiveness(attacking_type, own_type)
                for own_type in self.types
            )
            for attacking_type in Type
        }

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PokemonSpecies):
            return (self.name, self.dex_num) == (other.name, other.dex_num)
        return False

    def __hash__(self) -> int:
        return hash((self.name, self.dex_num))

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({repr(self.name)}, {self.dex_num}, "
            f"{self.base_hp}, {self.base_atk}, {self.base_def}, "
            f"{self.base_spe}, {self.base_spc}, {self.moveset}, "
            f"{self.primary_type}, {self.secondary_type})"
        )

    def attack_effectiveness(self, attacking_type: Type) -> float:
        """Produces the effectiveness of a given type against this Pokemon.

        Args:
            attacking_type: The type of the attack being used.

        Returns:
            The damage multiplier for the given attack type.
        """
        return self._effectivenesses[attacking_type]

    def critical_hit_threshold(
        self, high_crit_ratio: bool = False, focus_energy: bool = False
    ) -> int:
        """Produces the critical hit threshold for this Pokemon under.

        Note that Focus Energy will actually reduce the critical hit ratio, due
        to a bug in the original games.

        Args:
            high_crit_ratio: Whether the move used has a high critical hit ratio
              (Slash, etc.).
            focus_energy: Whether the user has the effects of Focus Energy.

        Returns:
            Number between 0 and 255 used as a maximum for a random byte to
            calculate a critical hit.
        """
        if not high_crit_ratio and not focus_energy:
            return floor(self.base_spe / 2)
        if not high_crit_ratio:
            return floor(self.base_spe / 8)
        if not focus_energy:
            return min(8 * floor(self.base_spe / 2), 255)
        return 4 * floor(self.base_spe / 4)
