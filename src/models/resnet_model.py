"""
ResNet model implementations
"""

import requests
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

from config.settings import ModelConfig
from .base_model import BaseModel, ModelLoadError


class ResNet18Model(BaseModel):
    """ResNet18 model implementation."""

    def __init__(self, config: ModelConfig):
        """
        Initialize ResNet18 model.

        Args:
            config: Model configuration
        """
        super().__init__(config)

    def _load_model(self):
        """Load ResNet18 model."""
        try:
            # Load pretrained ResNet18 with updated API
            if self.config.pretrained:
                self.model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
            else:
                self.model = models.resnet18(weights=None)

            # Set to evaluation mode
            self.model.eval()

            # Move to device
            device = torch.device(self.config.device)
            self.model = self.model.to(device)

        except Exception as e:
            raise ModelLoadError(f"Failed to load ResNet18 model: {str(e)}")

    def _load_class_names(self):
        """Load ImageNet class names."""
        try:
            # ImageNet class names URL
            url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"

            # Download class names
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Parse class names
            self.class_names = [line.strip() for line in response.text.split("\n") if line.strip()]

            # Ensure we have the right number of classes
            if len(self.class_names) != self.config.num_classes:
                print(f"Warning: Expected {self.config.num_classes} classes, got {len(self.class_names)}")

        except Exception as e:
            print(f"Warning: Failed to load ImageNet class names: {str(e)}")
            # Fallback: create generic class names
            self.class_names = [f"Class_{i}" for i in range(self.config.num_classes)]


class ResNet50Model(BaseModel):
    """ResNet50 model implementation (for future phases)."""

    def __init__(self, config: ModelConfig):
        """
        Initialize ResNet50 model.

        Args:
            config: Model configuration
        """
        super().__init__(config)

    def _load_model(self):
        """Load ResNet50 model."""
        try:
            # Load pretrained ResNet50 with updated API
            if self.config.pretrained:
                self.model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
            else:
                self.model = models.resnet50(weights=None)

            # Set to evaluation mode
            self.model.eval()

            # Move to device
            device = torch.device(self.config.device)
            self.model = self.model.to(device)

        except Exception as e:
            raise ModelLoadError(f"Failed to load ResNet50 model: {str(e)}")

    def _load_class_names(self):
        """Load ImageNet class names."""
        try:
            # ImageNet class names URL
            url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"

            # Download class names
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Parse class names
            self.class_names = [line.strip() for line in response.text.split("\n") if line.strip()]

            # Ensure we have the right number of classes
            if len(self.class_names) != self.config.num_classes:
                print(f"Warning: Expected {self.config.num_classes} classes, got {len(self.class_names)}")

        except Exception as e:
            print(f"Warning: Failed to load ImageNet class names: {str(e)}")
            # Fallback: create generic class names
            self.class_names = [f"Class_{i}" for i in range(self.config.num_classes)]
