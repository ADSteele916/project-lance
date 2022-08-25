from typing import TYPE_CHECKING, Optional

from simulator.moves.move import Move
from simulator.status import Status

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class StatusEffectMove(Move):

    def __init__(
            self,
            name: str,
            pp: int,
            move_type: str,
            accuracy: Optional[int],
            status: Status,
            priority: int = 0,
            *args,
            **kwargs
    ):
        super().__init__(name, pp, move_type, accuracy, priority, *args, **kwargs)
        self.status = status

    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        target.apply_status(self.status)
