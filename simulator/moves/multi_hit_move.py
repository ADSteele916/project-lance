from typing import Dict

from simulator.moves.repeating_move import RepeatingMove


class MultiHitMove(RepeatingMove):

    @property
    def repetitions(self) -> Dict[int, float]:
        return {2: 0.375, 3: 0.375, 4: 0.125, 5: 0.125}
