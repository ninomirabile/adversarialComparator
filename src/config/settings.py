"""
Configuration settings for Adversarial Comparator - Phase 1 (Ultra-Lightweight)
"""

import os
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class ModelConfig:
    """Model configuration settings."""

    # Model settings
    model_type: str = "resnet18"
    pretrained: bool = True
    num_classes: int = 1000
    input_size: Tuple[int, int] = (224, 224)

    # Preprocessing parameters (ImageNet normalization)
    mean: Tuple[float, float, float] = (0.485, 0.456, 0.406)
    std: Tuple[float, float, float] = (0.229, 0.224, 0.225)

    # Performance settings
    device: str = "cpu"  # Phase 1: CPU only for ultra-lightweight
    model_cache_size: int = 1


@dataclass
class AttackConfig:
    """Attack configuration settings."""

    # Attack parameters
    min_epsilon: float = 0.01
    max_epsilon: float = 0.50  # Increased from 0.30 to 0.50
    default_epsilon: float = 0.30  # Increased from 0.10 to 0.30

    # PGD specific parameters
    default_iterations: int = 50
    max_iterations: int = 100
    step_size: float = 0.01

    # Available attacks for Phase 1
    available_attacks: List[str] = field(default_factory=lambda: ["fgsm"])


@dataclass
class UIConfig:
    """UI configuration settings."""

    # Display settings
    max_predictions: int = 5
    confidence_threshold: float = 0.01

    # Image settings
    max_image_size: int = 50 * 1024 * 1024  # 50MB (increased from 10MB)
    supported_formats: List[str] = field(default_factory=lambda: [".jpg", ".jpeg", ".png", ".webp"])

    # Layout settings
    page_title: str = "Adversarial Comparator"
    page_icon: str = "🎯"
    layout: str = "wide"


@dataclass
class PerformanceConfig:
    """Performance configuration settings."""

    # Memory settings
    max_memory_usage: int = 2 * 1024 * 1024 * 1024  # 2GB
    enable_caching: bool = True

    # Timeout settings
    model_loading_timeout: int = 30  # seconds
    attack_generation_timeout: int = 60  # seconds

    # Optimization settings
    enable_quantization: bool = True  # Phase 1: Use quantized models
    batch_size: int = 1  # Phase 1: Single image processing


@dataclass
class AppConfig:
    """Main application configuration."""

    # Phase information
    phase: str = "1"
    phase_name: str = "Ultra-Lightweight"

    # Sub-configurations
    model: ModelConfig = field(default_factory=ModelConfig)
    attack: AttackConfig = field(default_factory=AttackConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)

    # Educational settings
    show_educational_content: bool = True
    show_disclaimer: bool = True

    def __post_init__(self):
        """Validate configuration after initialization."""
        self._validate_config()

    def _validate_config(self):
        """Validate configuration parameters."""
        # Validate epsilon range
        if self.attack.default_epsilon > self.attack.max_epsilon:
            raise ValueError("Default epsilon cannot exceed max epsilon")

        if self.attack.default_epsilon < self.attack.min_epsilon:
            raise ValueError("Default epsilon cannot be less than min epsilon")

        # Validate iterations
        if self.attack.default_iterations > self.attack.max_iterations:
            raise ValueError("Default iterations cannot exceed max iterations")

        # Validate image size
        if self.ui.max_image_size <= 0:
            raise ValueError("Max image size must be positive")


# Global configuration instance
config = AppConfig()


# Environment-specific overrides
def load_environment_config():
    """Load environment-specific configuration overrides."""
    # Check for environment variables
    if os.getenv("ADVERSARIAL_COMPARATOR_DEVICE"):
        config.model.device = os.getenv("ADVERSARIAL_COMPARATOR_DEVICE")

    if os.getenv("ADVERSARIAL_COMPARATOR_MODEL"):
        config.model.model_type = os.getenv("ADVERSARIAL_COMPARATOR_MODEL")

    if os.getenv("ADVERSARIAL_COMPARATOR_EPSILON"):
        try:
            config.attack.default_epsilon = float(os.getenv("ADVERSARIAL_COMPARATOR_EPSILON"))
        except ValueError:
            pass  # Keep default if invalid


# Load environment config on import
load_environment_config()
