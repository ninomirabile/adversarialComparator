"""
Targeted FGSM Attack Implementation
"""

from typing import Optional

import torch
import torch.nn.functional as F

from .base_attack import BaseAttack


class TargetedFGSMAttack(BaseAttack):
    """Targeted FGSM Attack that aims for specific target classes."""

    def __init__(self, epsilon: float = 0.3, target_class: Optional[int] = None, **kwargs):
        """
        Initialize Targeted FGSM Attack.

        Args:
            epsilon: Maximum perturbation size
            target_class: Target class to aim for (if None, will choose automatically)
            **kwargs: Additional arguments for base class
        """
        super().__init__(epsilon=epsilon, target_class=target_class, **kwargs)
        self.epsilon = epsilon
        self.target_class = target_class

    def __call__(self, x: torch.Tensor, model: torch.nn.Module) -> torch.Tensor:
        """
        Generate targeted adversarial example using FGSM.

        Args:
            x: Input tensor [batch_size, channels, height, width]
            model: Target model

        Returns:
            Adversarial tensor
        """
        model.eval()

        # Get current prediction
        with torch.no_grad():
            outputs = model(x)
            current_class = outputs.argmax(dim=1)

        # Choose target class if not specified
        if self.target_class is None:
            # Choose a different class (avoid current class)
            num_classes = outputs.shape[1]
            possible_targets = list(range(num_classes))
            if current_class.item() in possible_targets:
                possible_targets.remove(current_class.item())

            # Choose a target that's likely to be confused with street sign
            # Common confusions for traffic signs: traffic light, mailbox, birdhouse, etc.
            preferred_targets = [920, 919, 918, 917, 916]  # Some ImageNet classes
            for target in preferred_targets:
                if target in possible_targets:
                    self.target_class = target
                    break
            else:
                # Fallback to random target
                import random

                self.target_class = random.choice(possible_targets)

        # Create target tensor
        target = torch.tensor([self.target_class], device=x.device)

        # Clone input
        x_adv = x.clone().detach()
        x_adv.requires_grad_(True)

        # Forward pass
        outputs = model(x_adv)

        # Calculate loss (minimize loss for target class)
        loss = F.cross_entropy(outputs, target)

        # Backward pass
        loss.backward()

        # Update perturbation (opposite direction for targeted attack)
        with torch.no_grad():
            grad = x_adv.grad.sign()
            x_adv = x_adv - self.epsilon * grad  # Note the minus sign for targeted attack

            # Clamp to valid range [0, 1]
            x_adv = torch.clamp(x_adv, 0, 1)

        return x_adv.detach()
