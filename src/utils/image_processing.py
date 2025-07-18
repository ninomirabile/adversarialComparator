"""
Image processing utilities for Adversarial Comparator
"""

import io
from typing import Tuple, Optional, Union

import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image, UnidentifiedImageError

from config.settings import UIConfig


class ImageProcessor:
    """Utility class for image processing operations."""

    def __init__(self, config: UIConfig):
        """
        Initialize image processor.

        Args:
            config: UI configuration
        """
        self.config = config

    def load_image(self, file_path: str) -> Image.Image:
        """
        Load image from file path.

        Args:
            file_path: Path to image file

        Returns:
            PIL Image object

        Raises:
            ValueError: If image cannot be loaded
        """
        try:
            image = Image.open(file_path)
            return image
        except Exception as e:
            raise ValueError(f"Failed to load image from {file_path}: {str(e)}")

    def load_image_from_bytes(self, image_bytes: bytes) -> Image.Image:
        """
        Load image from bytes.

        Args:
            image_bytes: Image data as bytes

        Returns:
            PIL Image object

        Raises:
            ValueError: If image cannot be loaded
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            return image
        except Exception as e:
            raise ValueError(f"Failed to load image from bytes: {str(e)}")

    def validate_image(self, image: Image.Image) -> bool:
        """
        Validate image format and size.

        Args:
            image: PIL Image to validate

        Returns:
            True if image is valid

        Raises:
            ValueError: If image is invalid
        """
        # Check if image is None
        if image is None:
            raise ValueError("Image is None")

        # Check image mode
        if image.mode not in ["RGB", "RGBA", "L"]:
            raise ValueError(f"Unsupported image mode: {image.mode}. Supported modes: RGB, RGBA, L")

        # Check image size (basic validation)
        if image.size[0] <= 0 or image.size[1] <= 0:
            raise ValueError("Image has invalid dimensions")

        # Check if image is too large (rough estimate)
        image_size = len(image.tobytes())
        if image_size > self.config.max_image_size:
            raise ValueError(f"Image too large: {image_size} bytes (max: {self.config.max_image_size})")

        return True

    def resize_image(self, image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """
        Resize image to target size.

        Args:
            image: PIL Image
            size: Target size (width, height)

        Returns:
            Resized image
        """
        return image.resize(size, Image.Resampling.LANCZOS)

    def convert_to_rgb(self, image: Image.Image) -> Image.Image:
        """
        Convert image to RGB mode.

        Args:
            image: PIL Image

        Returns:
            RGB image
        """
        if image.mode != "RGB":
            return image.convert("RGB")
        return image

    def normalize_image(
        self, image: torch.Tensor, mean: Tuple[float, float, float], std: Tuple[float, float, float]
    ) -> torch.Tensor:
        """
        Normalize image tensor.

        Args:
            image: Image tensor (C, H, W)
            mean: Mean values for each channel
            std: Standard deviation values for each channel

        Returns:
            Normalized image tensor
        """
        mean_tensor = torch.tensor(mean).view(3, 1, 1)
        std_tensor = torch.tensor(std).view(3, 1, 1)

        return (image - mean_tensor) / std_tensor

    def denormalize_image(
        self, image: torch.Tensor, mean: Tuple[float, float, float], std: Tuple[float, float, float]
    ) -> torch.Tensor:
        """
        Denormalize image tensor.

        Args:
            image: Normalized image tensor (C, H, W)
            mean: Mean values for each channel
            std: Standard deviation values for each channel

        Returns:
            Denormalized image tensor
        """
        mean_tensor = torch.tensor(mean).view(3, 1, 1)
        std_tensor = torch.tensor(std).view(3, 1, 1)

        return image * std_tensor + mean_tensor

    def tensor_to_pil(self, tensor: torch.Tensor) -> Image.Image:
        """
        Convert tensor to PIL Image.

        Args:
            tensor: Image tensor (C, H, W) or (B, C, H, W)

        Returns:
            PIL Image
        """
        # Remove batch dimension if present
        if tensor.dim() == 4:
            tensor = tensor.squeeze(0)

        # Convert to numpy and transpose
        image_array = tensor.detach().cpu().numpy()
        image_array = np.transpose(image_array, (1, 2, 0))

        # Clip to valid range
        image_array = np.clip(image_array, 0, 1)

        # Convert to PIL Image
        image = Image.fromarray((image_array * 255).astype(np.uint8))

        return image

    def pil_to_tensor(self, image: Image.Image) -> torch.Tensor:
        """
        Convert PIL Image to tensor.

        Args:
            image: PIL Image

        Returns:
            Image tensor (C, H, W)
        """
        # Convert to RGB if necessary
        image = self.convert_to_rgb(image)

        # Convert to numpy and normalize
        image_array = np.array(image).astype(np.float32) / 255.0

        # Transpose to (C, H, W)
        image_array = np.transpose(image_array, (2, 0, 1))

        # Convert to tensor
        tensor = torch.from_numpy(image_array)

        return tensor

    def get_image_info(self, image: Image.Image) -> dict:
        """
        Get information about an image.

        Args:
            image: PIL Image

        Returns:
            Dictionary with image information
        """
        return {"size": image.size, "mode": image.mode, "format": image.format, "memory_size": len(image.tobytes())}


class ImageValidator:
    """Utility class for image validation."""

    def __init__(self, config: UIConfig):
        """
        Initialize image validator.

        Args:
            config: UI configuration
        """
        self.config = config

    def validate_file_type(self, filename: str) -> bool:
        """
        Validate file type.

        Args:
            filename: Name of file

        Returns:
            True if file type is supported
        """
        import os

        file_ext = os.path.splitext(filename)[1].lower()
        # Remove the dot from supported formats for comparison
        supported_formats = [fmt.lstrip(".") for fmt in self.config.supported_formats]
        return file_ext.lstrip(".") in supported_formats

    def validate_file_size(self, file_size: int) -> bool:
        """
        Validate file size.

        Args:
            file_size: Size of file in bytes

        Returns:
            True if file size is within limits
        """
        return file_size <= self.config.max_image_size

    def validate_uploaded_file(self, uploaded_file) -> bool:
        """
        Validate uploaded file.

        Args:
            uploaded_file: Streamlit uploaded file object

        Returns:
            True if file is valid
        """
        # Check file type
        if not self.validate_file_type(uploaded_file.name):
            return False

        # Check file size
        if not self.validate_file_size(uploaded_file.size):
            return False

        return True
