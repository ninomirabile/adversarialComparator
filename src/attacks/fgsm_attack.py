"""
FGSM (Fast Gradient Sign Method) attack implementation
"""

from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

from .base_attack import AttackGenerationError, BaseAttack


class FGSMAttack(BaseAttack):
    """Fast Gradient Sign Method attack."""

    def __init__(self, epsilon: float = 0.1, **kwargs):
        """
        Initialize FGSM attack.

        Args:
            epsilon: Attack strength parameter (maximum perturbation)
            **kwargs: Additional parameters
        """
        super().__init__(epsilon=epsilon, **kwargs)
        self.epsilon = epsilon

    def __call__(self, image: torch.Tensor, model: nn.Module) -> torch.Tensor:
        """
        Generate FGSM adversarial example.

        Args:
            image: Input image tensor (B, C, H, W)
            model: Target model to attack

        Returns:
            Adversarial image tensor

        Raises:
            AttackGenerationError: If attack generation fails
        """
        try:
            # Validate inputs
            self.validate_inputs(image, model)

            # Ensure image requires gradients
            image = image.clone().detach().requires_grad_(True)

            # Forward pass
            output = model(image)

            # Get predicted class
            predicted_class = output.argmax(dim=1)

            # Compute loss
            loss = F.cross_entropy(output, predicted_class)

            # Backward pass to compute gradients
            loss.backward()

            # Generate perturbation using gradient sign
            perturbation = self.epsilon * image.grad.sign()

            # Apply perturbation
            adversarial_image = image + perturbation

            # Clip to valid range [0, 1]
            adversarial_image = self.clip_to_valid_range(adversarial_image)

            return adversarial_image.detach()

        except Exception as e:
            raise AttackGenerationError(f"FGSM attack failed: {str(e)}")

    def get_attack_info(self) -> dict:
        """
        Get information about the FGSM attack.

        Returns:
            Dictionary with attack information
        """
        return {
            "attack_type": "FGSM",
            "epsilon": self.epsilon,
            "description": "Fast Gradient Sign Method - single-step attack",
            "parameters": self.get_parameters(),
        }


class FGSMWithTargetAttack(BaseAttack):
    """FGSM attack with target class."""

    def __init__(self, epsilon: float = 0.1, target_class: Optional[int] = None, **kwargs):
        """
        Initialize targeted FGSM attack.

        Args:
            epsilon: Attack strength parameter
            target_class: Target class to fool the model into predicting
            **kwargs: Additional parameters
        """
        super().__init__(epsilon=epsilon, target_class=target_class, **kwargs)
        self.epsilon = epsilon
        self.target_class = target_class

    def __call__(self, image: torch.Tensor, model: nn.Module) -> torch.Tensor:
        """
        Generate targeted FGSM adversarial example.

        Args:
            image: Input image tensor (B, C, H, W)
            model: Target model to attack

        Returns:
            Adversarial image tensor
        """
        try:
            # Validate inputs
            self.validate_inputs(image, model)

            # Ensure image requires gradients
            image = image.clone().detach().requires_grad_(True)

            # Forward pass
            output = model(image)

            # Determine target class
            if self.target_class is None:
                # Use least likely class as target
                target_class = output.argmin(dim=1)
            else:
                target_class = torch.tensor([self.target_class], device=image.device)

            # Compute loss (negative because we want to maximize loss for target class)
            loss = -F.cross_entropy(output, target_class)

            # Backward pass to compute gradients
            loss.backward()

            # Generate perturbation using gradient sign
            perturbation = self.epsilon * image.grad.sign()

            # Apply perturbation
            adversarial_image = image + perturbation

            # Clip to valid range [0, 1]
            adversarial_image = self.clip_to_valid_range(adversarial_image)

            return adversarial_image.detach()

        except Exception as e:
            raise AttackGenerationError(f"Targeted FGSM attack failed: {str(e)}")

    def get_attack_info(self) -> dict:
        """
        Get information about the targeted FGSM attack.

        Returns:
            Dictionary with attack information
        """
        return {
            "attack_type": "FGSM (Targeted)",
            "epsilon": self.epsilon,
            "target_class": self.target_class,
            "description": "Fast Gradient Sign Method with target class",
            "parameters": self.get_parameters(),
        }
