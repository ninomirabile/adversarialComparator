"""
Base model class for all ML models
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image

from config.settings import ModelConfig


class BaseModel(ABC):
    """Abstract base class for all models."""

    def __init__(self, config: ModelConfig):
        """
        Initialize the base model.

        Args:
            config: Model configuration
        """
        self.config = config
        self.model: Optional[nn.Module] = None
        self.transform = self._create_transform()
        self.class_names: List[str] = []

        # Load the model
        self._load_model()
        self._load_class_names()

    @abstractmethod
    def _load_model(self):
        """Load the specific model implementation."""
        pass

    @abstractmethod
    def _load_class_names(self):
        """Load class names for the model."""
        pass

    def _create_transform(self) -> transforms.Compose:
        """Create image transformation pipeline."""
        return transforms.Compose(
            [
                transforms.Resize(self.config.input_size),
                transforms.ToTensor(),
                transforms.Normalize(mean=self.config.mean, std=self.config.std),
            ]
        )

    def preprocess(self, image: Image.Image) -> torch.Tensor:
        """
        Preprocess image for model input.

        Args:
            image: PIL Image

        Returns:
            Preprocessed tensor
        """
        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Apply transformations
        tensor = self.transform(image)

        # Add batch dimension
        tensor = tensor.unsqueeze(0)

        return tensor

    def predict(self, image: torch.Tensor) -> torch.Tensor:
        """
        Make prediction on input image.

        Args:
            image: Input image tensor (B, C, H, W)

        Returns:
            Prediction logits (B, num_classes)
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")

        # Set model to evaluation mode
        self.model.eval()

        # Move to device
        device = torch.device(self.config.device)
        image = image.to(device)
        self.model = self.model.to(device)

        # Make prediction
        with torch.no_grad():
            output = self.model(image)

        return output

    def get_predictions(self, image: torch.Tensor, top_k: int = 5) -> List[dict]:
        """
        Get top-k predictions with class names and confidence scores.

        Args:
            image: Input image tensor
            top_k: Number of top predictions to return

        Returns:
            List of prediction dictionaries
        """
        # Get raw predictions
        logits = self.predict(image)

        # Apply softmax to get probabilities
        probabilities = torch.softmax(logits, dim=1)

        # Get top-k predictions
        top_probs, top_indices = torch.topk(probabilities, top_k, dim=1)

        # Convert to list of dictionaries
        predictions = []
        for i in range(top_k):
            class_id = top_indices[0, i].item()
            confidence = top_probs[0, i].item()

            # Get class name (handle index out of range)
            class_name = self.class_names[class_id] if class_id < len(self.class_names) else f"Class_{class_id}"

            predictions.append({"class_id": class_id, "class_name": class_name, "confidence": confidence})

        return predictions

    def get_class_names(self) -> List[str]:
        """
        Get list of class names.

        Returns:
            List of class names
        """
        return self.class_names

    def get_model_info(self) -> dict:
        """
        Get model information.

        Returns:
            Dictionary with model information
        """
        if self.model is None:
            return {}

        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)

        return {
            "model_type": self.config.model_type,
            "total_parameters": total_params,
            "trainable_parameters": trainable_params,
            "input_size": self.config.input_size,
            "num_classes": self.config.num_classes,
            "device": self.config.device,
        }


class ModelLoadError(Exception):
    """Exception raised when model loading fails."""

    pass


class PredictionError(Exception):
    """Exception raised when prediction fails."""

    pass
