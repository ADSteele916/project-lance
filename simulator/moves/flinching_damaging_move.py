from typing import TYPE_CHECKING, Optional

from simulator.moves.side_effect_damaging_move import SideEffectDamagingMove
from simulator.type import Type

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class FlinchingDamagingMove(SideEffectDamagingMove):

    def __init__(
            self,
            name: str,
            pp: int,
            move_type: Type,
            power: int,
            accuracy: Optional[int],
            flinch_chance: int,
            priority,
            *args,
            **kwargs
    ):
        super().__init__(name, pp, move_type, power, accuracy, flinch_chance, priority, *args, **kwargs)

    def side_effect(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        target.flinch = True
