"""
Attack Factory for creating different types of adversarial attacks
"""

from typing import Dict, Type

from .base_attack import BaseAttack
from .fgsm_attack import FGSMAttack
from .pgd_attack import PGDAttack
from .targeted_fgsm import TargetedFGSMAttack


class AttackFactory:
    """Factory for creating adversarial attacks."""

    def __init__(self, config):
        """
        Initialize attack factory.

        Args:
            config: Attack configuration
        """
        self.config = config
        self._attacks: Dict[str, Type[BaseAttack]] = {
            "fgsm": FGSMAttack,
            "pgd": PGDAttack,
            "targeted_fgsm": TargetedFGSMAttack,
        }

    def list_available_attacks(self) -> list:
        """List available attack types."""
        return list(self._attacks.keys())

    def get_attack(self, attack_type: str, **kwargs) -> BaseAttack:
        """
        Create an attack instance.

        Args:
            attack_type: Type of attack to create
            **kwargs: Additional arguments for the attack

        Returns:
            Attack instance
        """
        if attack_type not in self._attacks:
            raise ValueError(f"Unknown attack type: {attack_type}")

        # Get default parameters from config
        default_params = {
            "epsilon": self.config.default_epsilon,
        }

        # Update with provided kwargs
        default_params.update(kwargs)

        # Create attack instance
        attack_class = self._attacks[attack_type]
        return attack_class(**default_params)
