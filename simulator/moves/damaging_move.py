"""Functionality for a move that deals damage to the opposing ActivePokemon."""

from typing import Optional, TYPE_CHECKING

import numpy as np

from simulator.moves.move import Move

if TYPE_CHECKING:
    from simulator.battle.active_pokemon import ActivePokemon


class InvalidDamageException(Exception):

    def __init__(self, damage: int):
        super().__init__(
            f"{damage} is not a valid damage. It must be a postive integer.")


class DamagingMove(Move):
    """A Pokemon move that deals damage to its target."""

    def __init__(self,
                 name: str,
                 pp: int,
                 move_type: str,
                 power: int,
                 accuracy: Optional[int],
                 *args,
                 priority: int = 0,
                 **kwargs):
        if power <= 0:
            raise InvalidDamageException(power)
        super().__init__(name, pp, move_type, accuracy, priority, *args,
                         **kwargs)
        self.power = power

    def apply_effects(self, attacker: "ActivePokemon", target: "ActivePokemon"):
        critical = self.is_critical_hit(attacker)
        target.deal_damage(self.get_damage(attacker, target, critical))

    @staticmethod
    def is_critical_hit(attacker: "ActivePokemon") -> bool:
        """Randomly determines whether this attack is a critical hit.

        Args:
            attacker: The Pokemon who is currently attacking with this move.

        Returns:
            Whether the attack is a critical hit.
        """
        crit_roll = np.random.randint(0, high=256)
        threshold = attacker.pokemon.pokemon.species.critical_hit_threshold(
            False, attacker.focus_energy)
        return crit_roll < threshold

    def get_damage(self, attacker: "ActivePokemon", target: "ActivePokemon",
                   critical: bool) -> int:
        """Produces the total HP damage that will be dealt to the target.

        Args:
            attacker: The Pokemon using this move.
            target: The Pokemon being attacked by this move.
            critical: Whether this move is a critical hit.

        Returns:
            The damage (in HP) that this move will do to its target.
        """
        level = (attacker.party_member.level if not critical else 2 *
                 attacker.party_member.level)
        if critical:
            effective_attack = (attacker.pokemon.attack
                                if self.move_type.is_physical else
                                attacker.pokemon.special)
            effective_defense = (target.pokemon.defense
                                 if self.move_type.is_physical else
                                 target.pokemon.special)
        else:
            effective_attack = (attacker.attack if self.move_type.is_physical
                                else attacker.special)
            effective_defense = (target.defense if self.move_type.is_physical
                                 else target.special)
        stab = (1.5
                if self.move_type in (attacker.species.primary_type,
                                      attacker.species.secondary_type) else 1.0)
        type_effectiveness = target.species.attack_effectiveness(self.move_type)
        rand = np.random.randint(217, high=256)

        adjusted_level = (2 * level) // 5 + 2
        attack_defense_ratio = effective_attack / effective_defense
        unmodified_damage = (
            adjusted_level * int(self.power * attack_defense_ratio) // 50 + 2)

        return (int(unmodified_damage * stab) * type_effectiveness *
                rand) // 255


class HighCriticalChanceDamagingMove(DamagingMove):
    """A damaging move that is more likely to result in critical hits."""

    @staticmethod
    def is_critical_hit(attacker: "ActivePokemon"):
        crit_roll = np.random.randint(0, high=256)
        threshold = attacker.species.critical_hit_threshold(
            True, attacker.focus_energy)
        return crit_roll < threshold


class ConstantDamageMove(DamagingMove):

    @staticmethod
    def is_critical_hit(attacker: "ActivePokemon") -> bool:
        return False

    def get_damage(self, attacker: "ActivePokemon", target: "ActivePokemon",
                   critical: bool) -> int:
        return self.power


class LevelDamagingMove(DamagingMove):

    @staticmethod
    def is_critical_hit(attacker: "ActivePokemon") -> bool:
        return False

    def get_damage(self, attacker: "ActivePokemon", target: "ActivePokemon",
                   critical: bool) -> int:
        return attacker.party_member.level
