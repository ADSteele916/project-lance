"""Moves that apply a non-volatile status condition to their targets"""

from typing import Optional, TYPE_CHECKING

from simulator.moves.move import Move
from simulator.status import Status

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class StatusEffectMove(Move):
    """A Move that applies a non-volatile status effect to its target."""

    def __init__(self,
                 name: str,
                 pp: int,
                 move_type: str,
                 accuracy: Optional[int],
                 status: Status,
                 *args,
                 priority: int = 0,
                 **kwargs):
        super().__init__(name, pp, move_type, accuracy, priority, *args,
                         **kwargs)
        self.status = status

    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        target.apply_status(self.status)
