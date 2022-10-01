"""Functionality for Pokemon with customized builds."""

from math import floor
from math import sqrt
from typing import Final, List, Optional, TYPE_CHECKING

from simulator.pokemon.pokemon_species import PokemonSpecies

if TYPE_CHECKING:
    from simulator.moves.move import Move


class InvalidLevelException(Exception):

    def __init__(self, invalid_level: int):
        super().__init__(
            f"{invalid_level} is an invalid level. It must be between 1 and "
            f"100, inclusive.")


class InvalidMoveException(Exception):

    def __init__(self, invalid_move: "Move", pokemon: PokemonSpecies):
        super().__init__(f"{invalid_move} cannot be learned by {pokemon}")


class InvalidDiversificationValueException(Exception):

    def __init__(self, invalid_dv: int):
        super().__init__(
            f"{invalid_dv} is not a valid DV. DVs must be between 0 and "
            f"{PartyPokemon.MAX_DV}, inclusive.")


class InvalidStatExperienceValueException(Exception):

    def __init__(self, invalid_se: int):
        super().__init__(
            f"{invalid_se} is not a valid Stat Exp value. Stat Exps must be "
            f"between 0 and {PartyPokemon.MAX_STAT_EXP}, inclusive.")


class InvalidMoveCountException(Exception):

    def __init__(self, size: int):
        super().__init__(
            f"{size} is an invalid number of moves. Each Pokemon must have "
            f"between 1 and 4 moves, inclusive.")


class PartyPokemon:
    """A Pokemon with player-customizable attributes, but no in-battle stats."""

    MAX_DV: Final[int] = 0b1111
    MAX_STAT_EXP: Final[int] = 0xFFFF

    def __init__(
        self,
        species: PokemonSpecies,
        level: int,
        moves: List["Move"],
        atk_dv: int = MAX_DV,
        def_dv: int = MAX_DV,
        spe_dv: int = MAX_DV,
        spc_dv: int = MAX_DV,
        hp_stat_exp: int = MAX_STAT_EXP,
        atk_stat_exp: int = MAX_STAT_EXP,
        def_stat_exp: int = MAX_STAT_EXP,
        spe_stat_exp: int = MAX_STAT_EXP,
        spc_stat_exp: int = MAX_STAT_EXP,
        nickname: Optional[str] = None,
    ):
        self._species = species

        if not 1 <= level <= 100:
            raise InvalidLevelException(level)
        self._level = level

        if not 1 <= len(moves) <= 4:
            raise InvalidMoveCountException(len(moves))
        for move in moves:
            if move is not None and move not in self.species.moveset:
                raise InvalidMoveException(move, self.species)
        self._moves = moves

        for dv in (atk_dv, def_dv, spe_dv, spc_dv):
            if not 0 <= dv <= PartyPokemon.MAX_DV:
                raise InvalidDiversificationValueException(dv)
        self._hp_dv = (8 * (atk_dv % 2) + 4 * (def_dv % 2) + 2 * (spe_dv % 2) +
                       (spc_dv % 2))
        self._atk_dv = atk_dv
        self._def_dv = def_dv
        self._spe_dv = spe_dv
        self._spc_dv = spc_dv

        for stat_exp in (hp_stat_exp, atk_stat_exp, def_stat_exp, spe_stat_exp,
                         spc_stat_exp):
            if not 0 <= stat_exp <= PartyPokemon.MAX_STAT_EXP:
                raise InvalidStatExperienceValueException(stat_exp)
        self._hp_stat_exp = hp_stat_exp
        self._atk_stat_exp = atk_stat_exp
        self._def_stat_exp = def_stat_exp
        self._spe_stat_exp = spe_stat_exp
        self._spc_stat_exp = spc_stat_exp

        self._nickname = nickname

        self._hp = (floor(
            ((species.base_hp + self._hp_dv) + floor(sqrt(hp_stat_exp) / 4)) *
            level / 100) + level + 10)
        self._attack = (floor(
            ((species.base_atk + atk_dv) + floor(sqrt(atk_stat_exp) / 4)) *
            level / 100) + 5)
        self._defense = (floor(
            ((species.base_def + def_dv) + floor(sqrt(def_stat_exp) / 4)) *
            level / 100) + 5)
        self._speed = (floor(
            ((species.base_spe + spe_dv) + floor(sqrt(spe_stat_exp) / 4)) *
            level / 100) + 5)
        self._special = (floor(
            ((species.base_spc + spc_dv) + floor(sqrt(spc_stat_exp) / 4)) *
            level / 100) + 5)

    def __str__(self):
        return str(self.species) if self._nickname is None else self._nickname

    def __repr__(self):
        return (f"{self.__class__.__name__}({repr(self.species)}, "
                f"{self.level}, {self.moves}, {self.atk_dv}, {self.def_dv}, "
                f"{self.spe_dv}, {self.spc_dv}, {self.hp_stat_exp}, "
                f"{self.atk_stat_exp}, {self.def_stat_exp}, "
                f"{self.spe_stat_exp}, {self.spc_stat_exp}, "
                f"{repr(self.nickname)})")

    @property
    def species(self) -> PokemonSpecies:
        return self._species

    @property
    def level(self) -> int:
        return self._level

    @property
    def moves(self,) -> List["Move"]:
        return self._moves

    @property
    def hp_dv(self) -> int:
        return 8 * (self.atk_dv % 2) + 4 * (self.def_dv % 2) + 2 * (
            self.spe_dv % 2) + (self.spc_dv % 2)

    @property
    def atk_dv(self) -> int:
        return self._atk_dv

    @property
    def def_dv(self) -> int:
        return self._def_dv

    @property
    def spe_dv(self) -> int:
        return self._spe_dv

    @property
    def spc_dv(self) -> int:
        return self._spc_dv

    @property
    def hp_stat_exp(self) -> int:
        return self._hp_stat_exp

    @property
    def atk_stat_exp(self) -> int:
        return self._atk_stat_exp

    @property
    def def_stat_exp(self) -> int:
        return self._def_stat_exp

    @property
    def spe_stat_exp(self) -> int:
        return self._spe_stat_exp

    @property
    def spc_stat_exp(self) -> int:
        return self._spc_stat_exp

    @property
    def nickname(self) -> Optional[str]:
        return self._nickname

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def attack(self) -> int:
        return self._attack

    @property
    def defense(self) -> int:
        return self._defense

    @property
    def speed(self) -> int:
        return self._speed

    @property
    def special(self) -> int:
        return self._special
