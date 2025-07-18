"""
PGD (Projected Gradient Descent) Attack Implementation
"""

from typing import Optional

import torch
import torch.nn.functional as F

from .base_attack import BaseAttack


class PGDAttack(BaseAttack):
    """PGD (Projected Gradient Descent) Attack."""

    def __init__(
        self,
        epsilon: float = 0.3,
        alpha: float = 0.01,
        steps: int = 40,
        random_start: bool = True,
        targeted: bool = False,
        **kwargs,
    ):
        """
        Initialize PGD Attack.

        Args:
            epsilon: Maximum perturbation size
            alpha: Step size for each iteration
            steps: Number of iterations
            random_start: Whether to start from random perturbation
            targeted: Whether to perform targeted attack
            **kwargs: Additional arguments for base class
        """
        super().__init__(epsilon=epsilon, alpha=alpha, steps=steps, random_start=random_start, targeted=targeted, **kwargs)
        self.epsilon = epsilon
        self.alpha = alpha
        self.steps = steps
        self.random_start = random_start
        self.targeted = targeted

    def __call__(self, x: torch.Tensor, model: torch.nn.Module) -> torch.Tensor:
        """
        Generate adversarial example using PGD.

        Args:
            x: Input tensor [batch_size, channels, height, width]
            model: Target model

        Returns:
            Adversarial tensor
        """
        model.eval()

        # Clone input to avoid modifying original
        x_adv = x.clone().detach()

        # Random start
        if self.random_start:
            x_adv = x_adv + torch.randn_like(x_adv) * 0.001

        # PGD iterations
        for _ in range(self.steps):
            x_adv.requires_grad_(True)

            # Forward pass
            outputs = model(x_adv)

            # Calculate loss
            if self.targeted:
                # For targeted attack, we would need target labels
                # For now, we'll use untargeted attack
                loss = F.cross_entropy(outputs, outputs.argmax(dim=1))
            else:
                # Untargeted attack: maximize loss
                loss = -F.cross_entropy(outputs, outputs.argmax(dim=1))

            # Backward pass
            loss.backward()

            # Update perturbation
            with torch.no_grad():
                grad = x_adv.grad.sign()
                x_adv = x_adv + self.alpha * grad

                # Project to epsilon ball
                delta = x_adv - x
                delta = torch.clamp(delta, -self.epsilon, self.epsilon)
                x_adv = x + delta

                # Clamp to valid range [0, 1]
                x_adv = torch.clamp(x_adv, 0, 1)

            # Clear gradient (check if it exists)
            if x_adv.grad is not None:
                x_adv.grad.zero_()

        return x_adv.detach()
