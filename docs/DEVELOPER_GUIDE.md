# Developer Guide - Adversarial Comparator

## 🛠️ Development Setup

### Prerequisites
- **Python 3.8+**: Core runtime environment
- **Git**: Version control
- **Virtual Environment**: Isolated dependencies
- **IDE**: VS Code, PyCharm, or similar (recommended)

### System Requirements
- **Minimum**: 4GB RAM, Dual-core CPU
- **Recommended**: 8GB RAM, Quad-core CPU
- **Development**: 16GB RAM, SSD storage

### Initial Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/ninomirabile/adversarialComparator.git
   cd adversarialComparator
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   python -c "import torch, streamlit, torchattacks; print('Setup successful!')"
   ```

## 🏗️ Project Architecture

### Directory Structure
```
adversarialComparator/
├── app.py                 # Main Streamlit application
├── src/
│   ├── __init__.py
│   ├── models/           # Model loading and inference
│   │   ├── __init__.py
│   │   ├── model_factory.py
│   │   ├── resnet_model.py
│   │   └── model_cache.py
│   ├── attacks/          # Adversarial attack implementations
│   │   ├── __init__.py
│   │   ├── attack_factory.py
│   │   ├── fgsm_attack.py
│   │   └── pgd_attack.py
│   ├── utils/            # Utility functions
│   │   ├── __init__.py
│   │   ├── image_processing.py
│   │   ├── visualization.py
│   │   └── validation.py
│   └── config/           # Configuration files
│       ├── __init__.py
│       ├── settings.py
│       └── constants.py
├── docs/                 # Documentation
├── tests/                # Test files
├── requirements.txt      # Python dependencies
├── requirements-dev.txt  # Development dependencies
├── setup.py             # Package setup
├── LICENSE.md           # License file
└── README.md            # Project overview
```

### Core Components

#### 1. Model Factory (`src/models/model_factory.py`)
```python
class ModelFactory:
    """Factory for creating and managing ML models."""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model_cache = {}
    
    def get_model(self, model_type: str) -> BaseModel:
        """Get model instance based on type."""
        if model_type not in self.model_cache:
            self.model_cache[model_type] = self._create_model(model_type)
        return self.model_cache[model_type]
    
    def _create_model(self, model_type: str) -> BaseModel:
        """Create model instance."""
        if model_type == "resnet18":
            return ResNet18Model()
        elif model_type == "mobilenet":
            return MobileNetModel()
        else:
            raise ValueError(f"Unknown model type: {model_type}")
```

#### 2. Attack Factory (`src/attacks/attack_factory.py`)
```python
class AttackFactory:
    """Factory for creating adversarial attacks."""
    
    def __init__(self, config: AttackConfig):
        self.config = config
    
    def get_attack(self, attack_type: str, **kwargs) -> BaseAttack:
        """Get attack instance based on type."""
        if attack_type == "fgsm":
            return FGSMAttack(**kwargs)
        elif attack_type == "pgd":
            return PGDAttack(**kwargs)
        else:
            raise ValueError(f"Unknown attack type: {attack_type}")
```

#### 3. Configuration System (`src/config/settings.py`)
```python
@dataclass
class AppConfig:
    """Application configuration."""
    
    # Model settings
    model_type: str = "resnet18"
    model_cache_size: int = 1
    
    # Attack settings
    default_epsilon: float = 0.1
    max_epsilon: float = 0.3
    default_iterations: int = 50
    
    # Performance settings
    max_image_size: int = 10 * 1024 * 1024  # 10MB
    supported_formats: List[str] = field(default_factory=lambda: [".jpg", ".jpeg", ".png", ".webp"])
    
    # UI settings
    max_predictions: int = 5
    confidence_threshold: float = 0.01
```

## 🔧 Development Workflow

### Code Quality Standards

#### 1. Type Hints
```python
from typing import List, Optional, Tuple, Union
import torch
from PIL import Image

def process_image(
    image: Image.Image,
    target_size: Tuple[int, int] = (224, 224)
) -> torch.Tensor:
    """Process image for model input."""
    # Implementation
    pass
```

#### 2. Documentation
```python
def generate_adversarial_example(
    image: torch.Tensor,
    model: torch.nn.Module,
    attack_type: str,
    epsilon: float = 0.1,
    **kwargs
) -> Tuple[torch.Tensor, dict]:
    """
    Generate adversarial example for given image and model.
    
    Args:
        image: Input image tensor (C, H, W)
        model: Target model to attack
        attack_type: Type of attack ('fgsm', 'pgd', etc.)
        epsilon: Attack strength parameter
        **kwargs: Additional attack parameters
    
    Returns:
        Tuple of (adversarial_image, attack_metadata)
    
    Raises:
        ValueError: If attack_type is not supported
        RuntimeError: If attack generation fails
    """
    # Implementation
    pass
```

#### 3. Error Handling
```python
class ModelLoadError(Exception):
    """Raised when model loading fails."""
    pass

class AttackGenerationError(Exception):
    """Raised when attack generation fails."""
    pass

def load_model(model_type: str) -> torch.nn.Module:
    """Load model with proper error handling."""
    try:
        model = ModelFactory().get_model(model_type)
        return model
    except Exception as e:
        raise ModelLoadError(f"Failed to load model {model_type}: {str(e)}")
```

### Testing Strategy

#### 1. Unit Tests
```python
# tests/test_models.py
import pytest
import torch
from src.models.model_factory import ModelFactory

class TestModelFactory:
    def test_resnet18_creation(self):
        """Test ResNet18 model creation."""
        factory = ModelFactory()
        model = factory.get_model("resnet18")
        assert model is not None
        assert isinstance(model, torch.nn.Module)
    
    def test_invalid_model_type(self):
        """Test invalid model type handling."""
        factory = ModelFactory()
        with pytest.raises(ValueError):
            factory.get_model("invalid_model")
```

#### 2. Integration Tests
```python
# tests/test_integration.py
import pytest
from src.models.model_factory import ModelFactory
from src.attacks.attack_factory import AttackFactory

class TestIntegration:
    def test_end_to_end_workflow(self):
        """Test complete workflow from image to adversarial example."""
        # Load model
        model = ModelFactory().get_model("resnet18")
        
        # Create dummy image
        dummy_image = torch.randn(3, 224, 224)
        
        # Generate attack
        attack = AttackFactory().get_attack("fgsm", epsilon=0.1)
        adversarial_image = attack(dummy_image, model)
        
        # Verify results
        assert adversarial_image.shape == dummy_image.shape
        assert torch.allclose(adversarial_image, dummy_image, atol=0.3)
```

#### 3. Performance Tests
```python
# tests/test_performance.py
import time
import pytest
from src.models.model_factory import ModelFactory

class TestPerformance:
    def test_model_loading_time(self):
        """Test model loading performance."""
        start_time = time.time()
        model = ModelFactory().get_model("resnet18")
        load_time = time.time() - start_time
        
        assert load_time < 2.0  # Should load in under 2 seconds
    
    def test_inference_time(self):
        """Test inference performance."""
        model = ModelFactory().get_model("resnet18")
        dummy_image = torch.randn(1, 3, 224, 224)
        
        start_time = time.time()
        with torch.no_grad():
            _ = model(dummy_image)
        inference_time = time.time() - start_time
        
        assert inference_time < 0.5  # Should infer in under 500ms
```

### Running Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest tests/ -v
```

## 🚀 Progressive Development

### Phase 1 Implementation (Ultra-Lightweight)

#### 1. Basic Model Loading
```python
# src/models/resnet_model.py
import torch
import torchvision.models as models

class ResNet18Model:
    def __init__(self):
        self.model = models.resnet18(pretrained=True)
        self.model.eval()
    
    def predict(self, image: torch.Tensor) -> torch.Tensor:
        """Make prediction on input image."""
        with torch.no_grad():
            return self.model(image)
```

#### 2. Simple FGSM Attack
```python
# src/attacks/fgsm_attack.py
import torch
import torch.nn.functional as F

class FGSMAttack:
    def __init__(self, epsilon: float = 0.1):
        self.epsilon = epsilon
    
    def __call__(self, image: torch.Tensor, model: torch.nn.Module) -> torch.Tensor:
        """Generate FGSM adversarial example."""
        image.requires_grad_(True)
        
        # Forward pass
        output = model(image)
        loss = F.cross_entropy(output, output.argmax(dim=1))
        
        # Backward pass
        loss.backward()
        
        # Generate perturbation
        perturbation = self.epsilon * image.grad.sign()
        
        # Apply perturbation
        adversarial_image = image + perturbation
        adversarial_image = torch.clamp(adversarial_image, 0, 1)
        
        return adversarial_image.detach()
```

#### 3. Basic Streamlit App
```python
# app.py
import streamlit as st
from src.models.model_factory import ModelFactory
from src.attacks.attack_factory import AttackFactory

def main():
    st.title("Adversarial Comparator")
    
    # File upload
    uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        # Load model
        model = ModelFactory().get_model("resnet18")
        
        # Process image
        image = process_uploaded_image(uploaded_file)
        
        # Show original prediction
        original_pred = model.predict(image)
        st.write("Original Prediction:", original_pred)
        
        # Attack parameters
        epsilon = st.slider("Epsilon", 0.01, 0.3, 0.1)
        
        if st.button("Generate Attack"):
            # Generate adversarial example
            attack = AttackFactory().get_attack("fgsm", epsilon=epsilon)
            adversarial_image = attack(image, model)
            
            # Show results
            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption="Original")
            with col2:
                st.image(adversarial_image, caption="Adversarial")

if __name__ == "__main__":
    main()
```

### Phase 2 Enhancements

#### 1. Multiple Attack Types
```python
# src/attacks/pgd_attack.py
class PGDAttack:
    def __init__(self, epsilon: float = 0.1, iterations: int = 50, step_size: float = 0.01):
        self.epsilon = epsilon
        self.iterations = iterations
        self.step_size = step_size
    
    def __call__(self, image: torch.Tensor, model: torch.nn.Module) -> torch.Tensor:
        """Generate PGD adversarial example."""
        adversarial_image = image.clone()
        
        for _ in range(self.iterations):
            adversarial_image.requires_grad_(True)
            
            # Forward pass
            output = model(adversarial_image)
            loss = F.cross_entropy(output, output.argmax(dim=1))
            
            # Backward pass
            loss.backward()
            
            # Update image
            with torch.no_grad():
                perturbation = self.step_size * adversarial_image.grad.sign()
                adversarial_image = adversarial_image + perturbation
                
                # Project to epsilon ball
                delta = adversarial_image - image
                delta = torch.clamp(delta, -self.epsilon, self.epsilon)
                adversarial_image = image + delta
                adversarial_image = torch.clamp(adversarial_image, 0, 1)
        
        return adversarial_image.detach()
```

#### 2. Enhanced UI
```python
# Enhanced app.py with better UI
def main():
    st.set_page_config(page_title="Adversarial Comparator", layout="wide")
    
    st.title("🎯 Adversarial Comparator")
    st.markdown("Interactive tool for exploring adversarial attacks on AI models")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("⚙️ Attack Configuration")
        attack_type = st.selectbox("Attack Type", ["FGSM", "PGD"])
        epsilon = st.slider("Epsilon (ε)", 0.01, 0.3, 0.1, 0.01)
        
        if attack_type == "PGD":
            iterations = st.slider("Iterations", 10, 100, 50)
            step_size = st.slider("Step Size", 0.001, 0.05, 0.01, 0.001)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("📁 Upload Image", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file is not None:
            # Process and display results
            display_results(uploaded_file, attack_type, epsilon)
    
    with col2:
        st.header("📚 Educational Content")
        st.markdown("""
        **What are Adversarial Attacks?**
        
        Adversarial attacks are carefully crafted perturbations that can fool AI models into making incorrect predictions.
        
        **FGSM (Fast Gradient Sign Method)**
        - Single-step attack
        - Fast but less effective
        - Good for demonstrations
        
        **PGD (Projected Gradient Descent)**
        - Multi-step iterative attack
        - More effective but slower
        - Better for realistic scenarios
        """)
```

### Phase 3 Advanced Features

#### 1. Model Comparison
```python
# src/models/model_comparison.py
class ModelComparison:
    def __init__(self):
        self.models = {
            "resnet18": ModelFactory().get_model("resnet18"),
            "resnet50": ModelFactory().get_model("resnet50"),
            "mobilenet": ModelFactory().get_model("mobilenet")
        }
    
    def compare_robustness(self, image: torch.Tensor, attack: BaseAttack) -> dict:
        """Compare model robustness to attacks."""
        results = {}
        
        for name, model in self.models.items():
            adversarial_image = attack(image, model)
            original_pred = model.predict(image)
            adversarial_pred = model.predict(adversarial_image)
            
            results[name] = {
                "original_confidence": original_pred.max().item(),
                "adversarial_confidence": adversarial_pred.max().item(),
                "confidence_drop": original_pred.max().item() - adversarial_pred.max().item(),
                "prediction_changed": original_pred.argmax() != adversarial_pred.argmax()
            }
        
        return results
```

#### 2. Advanced Visualizations
```python
# src/utils/visualization.py
import plotly.graph_objects as go
import plotly.express as px

class AdvancedVisualization:
    @staticmethod
    def confidence_comparison_chart(original_preds, adversarial_preds, class_names):
        """Create interactive confidence comparison chart."""
        fig = go.Figure()
        
        # Original predictions
        fig.add_trace(go.Bar(
            name='Original',
            x=class_names,
            y=original_preds,
            marker_color='blue'
        ))
        
        # Adversarial predictions
        fig.add_trace(go.Bar(
            name='Adversarial',
            x=class_names,
            y=adversarial_preds,
            marker_color='red'
        ))
        
        fig.update_layout(
            title="Confidence Comparison",
            xaxis_title="Classes",
            yaxis_title="Confidence",
            barmode='group'
        )
        
        return fig
    
    @staticmethod
    def perturbation_heatmap(original_image, adversarial_image):
        """Create perturbation heatmap."""
        perturbation = torch.abs(adversarial_image - original_image)
        perturbation = perturbation.mean(dim=0)  # Average across channels
        
        fig = px.imshow(
            perturbation.numpy(),
            title="Perturbation Heatmap",
            color_continuous_scale="Reds"
        )
        
        return fig
```

## 🔍 Debugging and Troubleshooting

### Common Issues

#### 1. Model Loading Problems
```python
# Debug model loading
import torch
import torchvision

def debug_model_loading():
    try:
        model = torchvision.models.resnet18(pretrained=True)
        print("✅ Model loaded successfully")
        print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        print("Check internet connection and PyTorch installation")
```

#### 2. Memory Issues
```python
# Monitor memory usage
import psutil
import torch

def monitor_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    print(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
    
    if torch.cuda.is_available():
        print(f"GPU memory: {torch.cuda.memory_allocated() / 1024 / 1024:.2f} MB")
```

#### 3. Performance Bottlenecks
```python
# Profile performance
import time
import functools

def profile_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.3f} seconds")
        return result
    return wrapper

@profile_time
def slow_function():
    # Your slow code here
    pass
```

### Development Tools

#### 1. Code Formatting
```bash
# Install development tools
pip install black flake8 mypy

# Format code
black src/

# Check code quality
flake8 src/

# Type checking
mypy src/
```

#### 2. Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
```

#### 3. VS Code Configuration
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"]
}
```

## 📦 Deployment

### Local Development
```bash
# Run development server
streamlit run app.py --server.port 8501 --server.address localhost
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Hugging Face Spaces
```yaml
# .github/workflows/deploy.yml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Streamlit Cloud
        uses: streamlit/streamlit-sharing-deploy@v1
        with:
          repo_id: ninomirabile/adversarial-comparator
          streamlit_app_file: app.py
```

## 🤝 Contributing

### Development Guidelines
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** following the coding standards
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Submit a pull request**

### Code Review Process
1. **Automated checks** (tests, linting, type checking)
2. **Manual review** by maintainers
3. **Address feedback** and make changes
4. **Merge** when approved

### Release Process
1. **Version bump** in `setup.py`
2. **Update changelog**
3. **Create release tag**
4. **Deploy to production**

---

**Happy Coding! 🚀**

Remember: Good code is readable, testable, and maintainable. 