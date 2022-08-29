from typing import Dict

from simulator.moves.repeating_move import RepeatingMove


class DoubleHitMove(RepeatingMove):

    @property
    def repetitions(self) -> Dict[int, float]:
        return {2: 1.0}
