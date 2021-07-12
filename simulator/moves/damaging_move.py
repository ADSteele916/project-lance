"""Functionality for a move that deals damage to the opposing ActivePokemon."""

from typing import TYPE_CHECKING, Optional

import numpy as np

from simulator.moves.move import Move
from simulator.type import Type

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon
    from simulator.battle.battle import Battle, Player


class InvalidDamageException(Exception):

    def __init__(self, damage: int):
        super().__init__(f"{damage} is not a valid damage. It must be a postive integer.")


class DamagingMove(Move):
    """A Pokemon move that deals damage to its target."""

    def __init__(self, name: str, pp: int, move_type: Type, power: int, accuracy: Optional[int], priority: int = 0):
        if power <= 0:
            raise InvalidDamageException(power)
        super().__init__(name, pp, move_type, accuracy, priority)
        self.power = power

    def execute(self, battle: "Battle", player: "Player"):
        attacker: "ActivePokemon" = battle.teams[player][battle.team_cursors[player]]
        target: "ActivePokemon" = battle.teams[1 - player][battle.team_cursors[1 - player]]
        critical = self.is_critical_hit(attacker)

        target.deal_damage(self.get_damage(attacker, target, critical))

    @staticmethod
    def is_critical_hit(attacker: "ActivePokemon") -> bool:
        """Randomly determines whether this attack is a critical hit based on the attacker's base speed.

        Args:
            attacker (ActivePokemon): The Pokemon who is currently attacking with this move.

        Returns:
            bool: Whether or not the attack is a critical hit.
        """
        crit_roll = np.random.randint(0, high=256)
        threshold = attacker.pokemon.pokemon.species.critical_hit_threshold(False, attacker.focus_energy)
        return crit_roll < threshold

    def get_damage(self, attacker: "ActivePokemon", target: "ActivePokemon", critical: bool) -> int:
        """Produces the total HP damage that will be dealt to the target by the attacker using this move.

        Args:
            attacker (ActivePokemon): The Pokemon using this move.
            target (ActivePokemon): The Pokemon being attacked by this move.
            critical (bool): Whether or not this move is a critical hit.

        Returns:
            int: The damage (in HP) that this move will do to its target.
        """
        level = attacker.pokemon.pokemon.level if not critical else 2 * attacker.pokemon.pokemon.level
        if critical:
            effective_attack = attacker.pokemon.attack if self.move_type.is_physical else attacker.pokemon.special
            effective_defense = target.pokemon.defense if self.move_type.is_physical else target.pokemon.special
        else:
            effective_attack = attacker.attack if self.move_type.is_physical else attacker.special
            effective_defense = target.defense if self.move_type.is_physical else target.special
        stab = (
                1.5 if self.move_type == attacker.pokemon.pokemon.species.primary_type
                or self.move_type == attacker.pokemon.pokemon.species.secondary_type else 1.0
        )
        type_effectiveness = target.pokemon.pokemon.species.attack_effectiveness(self.move_type)
        rand = np.random.randint(217, high=256)

        adjusted_level = (2 * level) // 5 + 2
        attack_defense_ratio = effective_attack / effective_defense
        unmodified_damage = (adjusted_level * int(self.power * attack_defense_ratio) // 50 + 2)

        return (int(unmodified_damage * stab) * type_effectiveness * rand) // 255
