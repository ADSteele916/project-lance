"""Functionality for Pokemon with customized builds."""

from math import floor
from math import sqrt
from typing import Final, List, TYPE_CHECKING

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
        nickname: str = "",
    ):
        self.__species = species
        self.level = level
        self.moves = moves
        self.atk_dv = atk_dv
        self.def_dv = def_dv
        self.spe_dv = spe_dv
        self.spc_dv = spc_dv
        self.hp_stat_exp = hp_stat_exp
        self.atk_stat_exp = atk_stat_exp
        self.def_stat_exp = def_stat_exp
        self.spe_stat_exp = spe_stat_exp
        self.spc_stat_exp = spc_stat_exp
        self.nickname = nickname

    def __str__(self):
        return self.nickname if len(self.nickname) > 0 else self.species.name

    def __repr__(self):
        return (f"{self.__class__.__name__}({repr(self.__species)}, "
                f"{self.level}, {self.moves}, {self.atk_dv}, {self.def_dv}, "
                f"{self.spe_dv}, {self.spc_dv}, {self.hp_stat_exp}, "
                f"{self.atk_stat_exp}, {self.def_stat_exp}, "
                f"{self.spe_stat_exp}, {self.spc_stat_exp}, "
                f"{repr(self.nickname)})")

    @property
    def species(self) -> PokemonSpecies:
        return self.__species

    @property
    def level(self) -> int:
        return self.__level

    @level.setter
    def level(self, new_level: int):
        if not 1 <= new_level <= 100:
            raise InvalidLevelException(new_level)
        self.__level = new_level

    @property
    def moves(self,) -> List["Move"]:
        return self.__moves

    @moves.setter
    def moves(
        self,
        new_moves: List["Move"],
    ):
        if not 1 <= len(new_moves) <= 4:
            raise InvalidMoveCountException(len(new_moves))
        for move in new_moves:
            if move is not None and move not in self.species.moveset:
                raise InvalidMoveException(move, self.species)
        self.__moves = new_moves

    @property
    def hp_dv(self) -> int:
        return 8 * (self.atk_dv % 2) + 4 * (self.def_dv % 2) + 2 * (
            self.spe_dv % 2) + (self.spc_dv % 2)

    @hp_dv.setter
    def hp_dv(self, dv: int):
        if not 0 <= dv <= PartyPokemon.MAX_DV:
            raise ValueError(
                f"{dv} is not a valid DV. DVs must be between 0 and 15, "
                f"inclusive.")
        hp_bits = list(f"{dv:004b}")  # 4-bit binary string, e.g. "0100"

        atk_bits = f"{self.atk_dv:004b}"
        def_bits = f"{self.def_dv:004b}"
        spe_bits = f"{self.spe_dv:004b}"
        spc_bits = f"{self.spc_dv:004b}"

        self.__atk_dv = int(atk_bits[:-1] + hp_bits[0], 2)
        self.__def_dv = int(def_bits[:-1] + hp_bits[1], 2)
        self.__spe_dv = int(spe_bits[:-1] + hp_bits[2], 2)
        self.__spc_dv = int(spc_bits[:-1] + hp_bits[3], 2)

    @property
    def atk_dv(self) -> int:
        return self.__atk_dv

    @atk_dv.setter
    def atk_dv(self, dv: int):
        if not 0 <= dv <= PartyPokemon.MAX_DV:
            raise InvalidDiversificationValueException(dv)
        self.__atk_dv = dv

    @property
    def def_dv(self) -> int:
        return self.__atk_dv

    @def_dv.setter
    def def_dv(self, dv: int):
        if not 0 <= dv <= PartyPokemon.MAX_DV:
            raise InvalidDiversificationValueException(dv)
        self.__def_dv = dv

    @property
    def spe_dv(self) -> int:
        return self.__spe_dv

    @spe_dv.setter
    def spe_dv(self, dv: int):
        if not 0 <= dv <= PartyPokemon.MAX_DV:
            raise InvalidDiversificationValueException(dv)
        self.__spe_dv = dv

    @property
    def spc_dv(self) -> int:
        return self.__atk_dv

    @spc_dv.setter
    def spc_dv(self, dv: int):
        if not 0 <= dv <= PartyPokemon.MAX_DV:
            raise InvalidDiversificationValueException(dv)
        self.__spc_dv = dv

    @property
    def hp_stat_exp(self) -> int:
        return self.__hp_stat_exp

    @hp_stat_exp.setter
    def hp_stat_exp(self, stat_exp: int):
        if not 0 <= stat_exp <= PartyPokemon.MAX_STAT_EXP:
            raise InvalidStatExperienceValueException(stat_exp)
        self.__hp_stat_exp = stat_exp

    @property
    def atk_stat_exp(self) -> int:
        return self.__atk_stat_exp

    @atk_stat_exp.setter
    def atk_stat_exp(self, stat_exp: int):
        if not 0 <= stat_exp <= PartyPokemon.MAX_STAT_EXP:
            raise InvalidStatExperienceValueException(stat_exp)
        self.__atk_stat_exp = stat_exp

    @property
    def def_stat_exp(self) -> int:
        return self.__def_stat_exp

    @def_stat_exp.setter
    def def_stat_exp(self, stat_exp: int):
        if not 0 <= stat_exp <= PartyPokemon.MAX_STAT_EXP:
            raise InvalidStatExperienceValueException(stat_exp)
        self.__def_stat_exp = stat_exp

    @property
    def spe_stat_exp(self) -> int:
        return self.__spe_stat_exp

    @spe_stat_exp.setter
    def spe_stat_exp(self, stat_exp: int):
        if not 0 <= stat_exp <= PartyPokemon.MAX_STAT_EXP:
            raise InvalidStatExperienceValueException(stat_exp)
        self.__spe_stat_exp = stat_exp

    @property
    def spc_stat_exp(self) -> int:
        return self.__spc_stat_exp

    @spc_stat_exp.setter
    def spc_stat_exp(self, stat_exp: int):
        if not 0 <= stat_exp <= PartyPokemon.MAX_STAT_EXP:
            raise InvalidStatExperienceValueException(stat_exp)
        self.__spc_stat_exp = stat_exp

    @property
    def hp(self) -> int:
        return (floor(((self.species.base_hp + self.hp_dv) +
                       floor(sqrt(self.hp_stat_exp) / 4)) * self.level / 100) +
                self.level + 10)

    @property
    def attack(self) -> int:
        return (floor(
            ((self.species.base_atk + self.__atk_dv) +
             floor(sqrt(self.atk_stat_exp) / 4)) * self.level / 100) + 5)

    @property
    def defense(self) -> int:
        return (floor(
            ((self.species.base_def + self.__def_dv) +
             floor(sqrt(self.def_stat_exp) / 4)) * self.level / 100) + 5)

    @property
    def speed(self) -> int:
        return (floor(
            ((self.species.base_spe + self.__spe_dv) +
             floor(sqrt(self.spe_stat_exp) / 4)) * self.level / 100) + 5)

    @property
    def special(self) -> int:
        return (floor(
            ((self.species.base_spc + self.__spc_dv) +
             floor(sqrt(self.spc_stat_exp) / 4)) * self.level / 100) + 5)
