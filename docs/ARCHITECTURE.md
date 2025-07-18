# Architecture - Adversarial Comparator

## 🏗️ System Overview

The Adversarial Comparator is designed as a modular, scalable web application that demonstrates adversarial attacks on image classification models. The architecture follows a factory pattern with clear separation of concerns and progressive development phases.

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Streamlit UI  │  │   File Upload   │  │   Results   │  │
│  │   (Frontend)    │  │   & Validation  │  │  Display    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │  StreamlitApp   │  │  ImageProcessor │  │  ResultMgr  │  │
│  │   (Controller)  │  │   (Processor)   │  │  (Manager)  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │  ModelFactory   │  │  AttackFactory  │  │  Validation │  │
│  │   (Factory)     │  │    (Factory)    │  │   (Utils)   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   PyTorch       │  │   Torchvision   │  │  TorchAttacks│  │
│  │   (Framework)   │  │   (Models)      │  │  (Attacks)  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Core Components

### 1. Factory Pattern Implementation

#### Model Factory Architecture
```
ModelFactory
├── ModelCache (Singleton)
│   ├── ResNet18Model
│   ├── MobileNetModel
│   └── CustomModel
├── ModelLoader
│   ├── PretrainedLoader
│   ├── CustomLoader
│   └── QuantizedLoader
└── ModelConfig
    ├── ModelType
    ├── PreprocessingParams
    └── PerformanceSettings
```

#### Attack Factory Architecture
```
AttackFactory
├── AttackRegistry
│   ├── FGSMAttack
│   ├── PGDAttack
│   ├── DeepFoolAttack
│   └── CustomAttack
├── AttackConfig
│   ├── EpsilonRange
│   ├── IterationSettings
│   └── OptimizationParams
└── AttackValidator
    ├── ParameterValidation
    ├── ResourceValidation
    └── SafetyValidation
```

### 2. Progressive Development Architecture

#### Phase 1: Ultra-Lightweight
```
┌─────────────────────────────────────────────────────────────┐
│                    Phase 1 Architecture                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Basic UI      │  │   ResNet18      │  │   FGSM      │  │
│  │   (Streamlit)   │  │   (CPU Only)    │  │   (Single)  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Simple        │  │   Basic         │  │   Minimal   │  │
│  │   Validation    │  │   Processing    │  │   Caching   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

#### Phase 2: Standard
```
┌─────────────────────────────────────────────────────────────┐
│                    Phase 2 Architecture                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Enhanced UI   │  │   Multiple      │  │   Multiple  │  │
│  │   (Advanced)    │  │   Models        │  │   Attacks   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Advanced      │  │   Optimized     │  │   Smart     │  │
│  │   Validation    │  │   Processing    │  │   Caching   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

#### Phase 3: Full-Featured
```
┌─────────────────────────────────────────────────────────────┐
│                    Phase 3 Architecture                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Advanced UI   │  │   Custom        │  │   Complete  │  │
│  │   (Analytics)   │  │   Models        │  │   Attacks   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Real-time     │  │   GPU           │  │   Advanced  │  │
│  │   Processing    │  │   Acceleration  │  │   Analytics │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Architecture

### 1. Image Upload Flow
```
User Upload → Validation → Preprocessing → Model Input
     │            │             │              │
     ▼            ▼             ▼              ▼
FileSystem → Validator → ImageProcessor → TensorConverter
```

### 2. Prediction Flow
```
Model Input → Model Inference → Post-processing → Results
     │              │                │              │
     ▼              ▼                ▼              ▼
TensorConverter → Model.predict() → Softmax → PredictionResult
```

### 3. Attack Generation Flow
```
Original Image → Attack Configuration → Attack Generation → Adversarial Image
      │                    │                    │                    │
      ▼                    ▼                    ▼                    ▼
ImageTensor → AttackParams → AttackAlgorithm → PerturbedTensor
```

### 4. Comparison Flow
```
Original + Adversarial → Analysis → Visualization → Display
      │                        │              │              │
      ▼                        ▼              ▼              ▼
BothImages → MetricsCalculator → ChartGenerator → StreamlitUI
```

## 🏛️ Component Details

### 1. User Interface Layer

#### StreamlitApp Controller
```python
class StreamlitApp:
    """Main application controller."""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.model_factory = ModelFactory(config)
        self.attack_factory = AttackFactory(config)
        self.image_processor = ImageProcessor(config)
        self.result_manager = ResultManager()
    
    def run(self):
        """Main application loop."""
        self.setup_page()
        self.render_sidebar()
        self.render_main_content()
    
    def handle_user_interaction(self):
        """Handle user interactions and state management."""
        # File upload handling
        # Parameter updates
        # Attack generation
        # Results display
```

#### UI Components
- **FileUploader**: Handles image upload and validation
- **ParameterControls**: Manages attack parameters
- **ResultsDisplay**: Shows comparison and analysis
- **EducationalContent**: Provides learning resources

### 2. Application Layer

#### ImageProcessor
```python
class ImageProcessor:
    """Handles image processing and validation."""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.validator = ImageValidator(config)
        self.preprocessor = ImagePreprocessor(config)
    
    def process_upload(self, uploaded_file) -> torch.Tensor:
        """Process uploaded file to model-ready tensor."""
        # Validation
        # Preprocessing
        # Conversion
        pass
    
    def validate_image(self, image: Image.Image) -> bool:
        """Validate image format and size."""
        pass
```

#### ResultManager
```python
class ResultManager:
    """Manages result storage and retrieval."""
    
    def __init__(self):
        self.results_cache = {}
        self.comparison_history = []
    
    def store_result(self, result: AttackResult):
        """Store attack result."""
        pass
    
    def get_comparison(self, original_id: str, adversarial_id: str) -> ComparisonResult:
        """Get comparison between two results."""
        pass
```

### 3. Business Logic Layer

#### ModelFactory Implementation
```python
class ModelFactory:
    """Factory for creating and managing models."""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model_cache = ModelCache()
        self.model_loader = ModelLoader()
    
    def get_model(self, model_type: str) -> BaseModel:
        """Get model instance with caching."""
        if model_type in self.model_cache:
            return self.model_cache.get(model_type)
        
        model = self.model_loader.load_model(model_type, self.config)
        self.model_cache.store(model_type, model)
        return model
```

#### AttackFactory Implementation
```python
class AttackFactory:
    """Factory for creating adversarial attacks."""
    
    def __init__(self, config: AttackConfig):
        self.config = config
        self.attack_registry = AttackRegistry()
        self.parameter_validator = ParameterValidator()
    
    def get_attack(self, attack_type: str, **kwargs) -> BaseAttack:
        """Get attack instance with parameter validation."""
        # Validate parameters
        # Create attack instance
        # Return configured attack
        pass
```

### 4. Data Layer

#### Model Implementations
```python
class ResNet18Model(BaseModel):
    """ResNet18 model implementation."""
    
    def __init__(self, config: ModelConfig):
        self.model = torchvision.models.resnet18(pretrained=True)
        self.preprocessor = ResNetPreprocessor(config)
        self.postprocessor = ResNetPostprocessor(config)
    
    def predict(self, image: torch.Tensor) -> torch.Tensor:
        """Make prediction with preprocessing and postprocessing."""
        processed_image = self.preprocessor(image)
        with torch.no_grad():
            output = self.model(processed_image)
        return self.postprocessor(output)
```

#### Attack Implementations
```python
class FGSMAttack(BaseAttack):
    """FGSM attack implementation."""
    
    def __init__(self, epsilon: float = 0.1):
        self.epsilon = epsilon
        self.validator = AttackValidator()
    
    def __call__(self, image: torch.Tensor, model: torch.nn.Module) -> torch.Tensor:
        """Generate FGSM adversarial example."""
        # Validate inputs
        # Generate perturbation
        # Apply perturbation
        # Return result
        pass
```

## 🔧 Configuration Architecture

### Configuration Hierarchy
```
AppConfig (Root)
├── ModelConfig
│   ├── ModelType
│   ├── PreprocessingParams
│   └── PerformanceSettings
├── AttackConfig
│   ├── AttackType
│   ├── ParameterRanges
│   └── SafetyLimits
├── UIConfig
│   ├── DisplaySettings
│   ├── LayoutOptions
│   └── ThemeSettings
└── PerformanceConfig
    ├── MemoryLimits
    ├── TimeoutSettings
    └── CachingOptions
```

### Configuration Management
```python
@dataclass
class AppConfig:
    """Application configuration with validation."""
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        self.validate_model_config()
        self.validate_attack_config()
        self.validate_performance_config()
    
    def validate_model_config(self):
        """Validate model configuration."""
        if self.model_type not in SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model type: {self.model_type}")
    
    def validate_attack_config(self):
        """Validate attack configuration."""
        if self.default_epsilon > self.max_epsilon:
            raise ValueError("Default epsilon cannot exceed max epsilon")
```

## 🚀 Performance Architecture

### 1. Caching Strategy
```
┌─────────────────────────────────────────────────────────────┐
│                    Caching Architecture                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Model Cache   │  │   Result Cache  │  │   Image     │  │
│  │   (Singleton)   │  │   (Session)     │  │   Cache     │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Attack Cache  │  │   Config Cache  │  │   UI Cache  │  │
│  │   (Factory)     │  │   (Settings)    │  │   (State)   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2. Memory Management
```python
class MemoryManager:
    """Manages memory usage and optimization."""
    
    def __init__(self, config: PerformanceConfig):
        self.config = config
        self.memory_monitor = MemoryMonitor()
        self.garbage_collector = GarbageCollector()
    
    def optimize_memory(self):
        """Optimize memory usage."""
        # Monitor usage
        # Clear caches if needed
        # Force garbage collection
        pass
    
    def check_memory_limits(self) -> bool:
        """Check if memory usage is within limits."""
        pass
```

### 3. Performance Monitoring
```python
class PerformanceMonitor:
    """Monitors application performance."""
    
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.profiler = PerformanceProfiler()
    
    def track_operation(self, operation: str, start_time: float):
        """Track operation performance."""
        pass
    
    def get_performance_report(self) -> PerformanceReport:
        """Generate performance report."""
        pass
```

## 🔒 Security Architecture

### 1. Input Validation
```
┌─────────────────────────────────────────────────────────────┐
│                    Security Architecture                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   File          │  │   Parameter     │  │   Model     │  │
│  │   Validation    │  │   Validation    │  │   Validation│  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Size          │  │   Format        │  │   Content   │  │
│  │   Limits        │  │   Checking      │  │   Scanning  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2. Sandboxed Execution
```python
class SecurityManager:
    """Manages security and safety measures."""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.sandbox = ExecutionSandbox()
        self.rate_limiter = RateLimiter()
    
    def validate_operation(self, operation: str, params: dict) -> bool:
        """Validate operation for security."""
        pass
    
    def execute_safely(self, func: callable, *args, **kwargs):
        """Execute function in safe environment."""
        pass
```

## 📊 Scalability Architecture

### 1. Horizontal Scaling
```
┌─────────────────────────────────────────────────────────────┐
│                    Scalability Architecture                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Load          │  │   Session       │  │   Resource  │  │
│  │   Balancer      │  │   Management    │  │   Pooling   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Auto          │  │   Cache         │  │   Database  │  │
│  │   Scaling       │  │   Distribution  │  │   Sharding  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2. Vertical Scaling
```python
class ScalabilityManager:
    """Manages application scalability."""
    
    def __init__(self, config: ScalabilityConfig):
        self.config = config
        self.resource_monitor = ResourceMonitor()
        self.scaling_controller = ScalingController()
    
    def check_scaling_needs(self) -> ScalingDecision:
        """Check if scaling is needed."""
        pass
    
    def scale_up(self):
        """Scale up resources."""
        pass
    
    def scale_down(self):
        """Scale down resources."""
        pass
```

## 🔄 Deployment Architecture

### 1. Local Development
```
┌─────────────────────────────────────────────────────────────┐
│                    Local Development                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Development   │  │   Hot           │  │   Debug     │  │
│  │   Server        │  │   Reload        │  │   Mode      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2. Docker Deployment
```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Architecture                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Multi-stage   │  │   Volume        │  │   Network   │  │
│  │   Build         │  │   Mounting      │  │   Isolation │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 3. Cloud Deployment
```
┌─────────────────────────────────────────────────────────────┐
│                    Cloud Architecture                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Hugging Face  │  │   AWS/GCP/Azure │  │   Heroku    │  │
│  │   Spaces        │  │   Cloud         │  │   Platform  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🔮 Future Architecture Considerations

### 1. Microservices Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Microservices Architecture               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Model         │  │   Attack        │  │   UI        │  │
│  │   Service       │  │   Service       │  │   Service   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   API           │  │   Message       │  │   Database  │  │
│  │   Gateway       │  │   Queue         │  │   Service   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2. Event-Driven Architecture
```python
class EventBus:
    """Event-driven communication system."""
    
    def __init__(self):
        self.subscribers = {}
        self.event_queue = EventQueue()
    
    def publish(self, event: Event):
        """Publish event to subscribers."""
        pass
    
    def subscribe(self, event_type: str, handler: callable):
        """Subscribe to event type."""
        pass
```

---

**This architecture provides a solid foundation for building a scalable, maintainable, and educational adversarial attack demonstration tool.** 