"""Functionality for a damaging move that has a chance to apply a non-volatile status condition to its target."""

from typing import TYPE_CHECKING, Optional

from simulator.moves.side_effect_damaging_move import SideEffectDamagingMove
from simulator.status import Status
from simulator.type import Type

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class StatusDamagingMove(SideEffectDamagingMove):
    """A damaging Pokemon move that can apply a non-volatile status condition to its target."""

    def __init__(
            self,
            name: str,
            pp: int,
            move_type: Type,
            power: int,
            accuracy: Optional[int],
            status: Status,
            status_chance: int,
            priority
    ):
        super().__init__(name, pp, move_type, power, accuracy, status_chance, priority)
        self.status = status

    def side_effect(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        if target.status == Status.FREEZE and self.status == Status.BURN:
            target.status = Status.NONE
        elif self.status == Status.POISON and Type.POISON in (
                target.pokemon.pokemon.species.primary_type,
                target.pokemon.pokemon.species.secondary_type
        ):
            return
        elif self.status == Status.BURN and Type.FIRE in (
                target.pokemon.pokemon.species.primary_type,
                target.pokemon.pokemon.species.secondary_type
        ):
            return
        elif target.status == Status.NONE:
            target.status = self.status
