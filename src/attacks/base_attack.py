"""
Base attack class for Adversarial Comparator
"""

import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import torch
import torch.nn as nn


class BaseAttack(ABC):
    """Abstract base class for all adversarial attacks."""

    def __init__(self, **kwargs):
        """
        Initialize the base attack.

        Args:
            **kwargs: Attack-specific parameters
        """
        self.parameters = kwargs
        self.attack_time: Optional[float] = None

    @abstractmethod
    def __call__(self, image: torch.Tensor, model: nn.Module) -> torch.Tensor:
        """
        Generate adversarial example.

        Args:
            image: Input image tensor (B, C, H, W)
            model: Target model to attack

        Returns:
            Adversarial image tensor
        """
        pass

    def get_parameters(self) -> Dict[str, Any]:
        """
        Get attack parameters.

        Returns:
            Dictionary of attack parameters
        """
        return self.parameters.copy()

    def get_attack_time(self) -> Optional[float]:
        """
        Get the time taken for the last attack.

        Returns:
            Attack time in seconds, or None if no attack has been performed
        """
        return self.attack_time

    def _measure_time(self, func):
        """
        Decorator to measure attack execution time.

        Args:
            func: Function to measure

        Returns:
            Wrapped function
        """

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            self.attack_time = time.time() - start_time
            return result

        return wrapper

    def validate_inputs(self, image: torch.Tensor, model: nn.Module) -> bool:
        """
        Validate input parameters.

        Args:
            image: Input image tensor
            model: Target model

        Returns:
            True if inputs are valid

        Raises:
            ValueError: If inputs are invalid
        """
        # Check image tensor
        if not isinstance(image, torch.Tensor):
            raise ValueError("Image must be a torch.Tensor")

        if image.dim() != 4:
            raise ValueError("Image must be 4-dimensional (B, C, H, W)")

        if image.size(0) != 1:
            raise ValueError("Currently only supports batch size of 1")

        # Check model
        if not isinstance(model, nn.Module):
            raise ValueError("Model must be a torch.nn.Module")

        return True

    def clip_to_valid_range(self, image: torch.Tensor) -> torch.Tensor:
        """
        Clip image to valid range [0, 1].

        Args:
            image: Input image tensor

        Returns:
            Clipped image tensor
        """
        return torch.clamp(image, 0, 1)

    def compute_perturbation_norm(self, original: torch.Tensor, adversarial: torch.Tensor) -> float:
        """
        Compute L2 norm of perturbation.

        Args:
            original: Original image tensor
            adversarial: Adversarial image tensor

        Returns:
            L2 norm of perturbation
        """
        perturbation = adversarial - original
        return torch.norm(perturbation, p=2).item()

    def compute_perturbation_linf(self, original: torch.Tensor, adversarial: torch.Tensor) -> float:
        """
        Compute L-infinity norm of perturbation.

        Args:
            original: Original image tensor
            adversarial: Adversarial image tensor

        Returns:
            L-infinity norm of perturbation
        """
        perturbation = adversarial - original
        return torch.norm(perturbation, p=float("inf")).item()


class AttackGenerationError(Exception):
    """Exception raised when attack generation fails."""

    pass


class InvalidAttackParametersError(Exception):
    """Exception raised when attack parameters are invalid."""

    pass
