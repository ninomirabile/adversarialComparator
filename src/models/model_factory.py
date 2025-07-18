"""
Model factory for creating and managing models
"""

from typing import Dict, Optional

from config.settings import ModelConfig
from .base_model import BaseModel, ModelLoadError
from .resnet_model import ResNet18Model, ResNet50Model


class ModelFactory:
    """Factory for creating and managing ML models."""

    def __init__(self, config: ModelConfig):
        """
        Initialize the model factory.

        Args:
            config: Model configuration
        """
        self.config = config
        self.model_cache: Dict[str, BaseModel] = {}
        self._model_registry = {
            "resnet18": ResNet18Model,
            "resnet50": ResNet50Model,
        }

    def get_model(self, model_type: Optional[str] = None) -> BaseModel:
        """
        Get model instance based on type.

        Args:
            model_type: Type of model to load (defaults to config.model_type)

        Returns:
            Model instance

        Raises:
            ModelLoadError: If model loading fails
            ValueError: If model type is not supported
        """
        # Use default model type if not specified
        if model_type is None:
            model_type = self.config.model_type

        # Check if model is already cached
        if model_type in self.model_cache:
            return self.model_cache[model_type]

        # Create new model instance
        model = self._create_model(model_type)

        # Cache the model
        self.model_cache[model_type] = model

        return model

    def _create_model(self, model_type: str) -> BaseModel:
        """
        Create model instance.

        Args:
            model_type: Type of model to create

        Returns:
            Model instance

        Raises:
            ValueError: If model type is not supported
            ModelLoadError: If model creation fails
        """
        if model_type not in self._model_registry:
            available_models = list(self._model_registry.keys())
            raise ValueError(f"Unsupported model type: {model_type}. " f"Available models: {available_models}")

        try:
            model_class = self._model_registry[model_type]
            return model_class(self.config)
        except Exception as e:
            raise ModelLoadError(f"Failed to create model {model_type}: {str(e)}")

    def list_available_models(self) -> list:
        """
        Get list of available model types.

        Returns:
            List of supported model types
        """
        return list(self._model_registry.keys())

    def clear_cache(self):
        """Clear the model cache."""
        self.model_cache.clear()

    def get_cached_models(self) -> list:
        """
        Get list of currently cached models.

        Returns:
            List of cached model types
        """
        return list(self.model_cache.keys())

    def remove_from_cache(self, model_type: str):
        """
        Remove specific model from cache.

        Args:
            model_type: Type of model to remove
        """
        if model_type in self.model_cache:
            del self.model_cache[model_type]

    def get_model_info(self, model_type: Optional[str] = None) -> dict:
        """
        Get information about a model.

        Args:
            model_type: Type of model (defaults to config.model_type)

        Returns:
            Dictionary with model information
        """
        model = self.get_model(model_type)
        return model.get_model_info()
