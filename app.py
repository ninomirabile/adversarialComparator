"""
Adversarial Comparator - Main Streamlit Application
Phase 1: Ultra-Lightweight Implementation
"""

import streamlit as st
import torch
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional, Tuple
import logging
import sys
import traceback
import os

# Add src to Python path
try:
    current_dir = os.path.dirname(__file__)
except NameError:
    # __file__ is not defined when using exec()
    current_dir = os.getcwd()
sys.path.insert(0, os.path.join(current_dir, 'src'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Import our modules
from config.settings import config
from models.model_factory import ModelFactory
from attacks.attack_factory import AttackFactory
from utils.image_processing import ImageProcessor, ImageValidator


class AdversarialComparatorApp:
    """Main Streamlit application class."""
    
    def __init__(self):
        """Initialize the application."""
        logger.info("🚀 Initializing AdversarialComparatorApp")
        
        self.config = config
        logger.info(f"📋 Config loaded: phase={self.config.phase}, model={self.config.model.model_type}")
        
        self.model_factory = ModelFactory(config.model)
        self.attack_factory = AttackFactory(config.attack)
        self.image_processor = ImageProcessor(config.ui)
        self.image_validator = ImageValidator(config.ui)
        
        logger.info("🏭 Factories and processors initialized")
        
        # Initialize model immediately
        self.model = None
        logger.info("🤖 Model initialized as None (will be loaded on demand)")
        
        # Initialize session state
        if 'model_loaded' not in st.session_state:
            st.session_state.model_loaded = False
            logger.info("📝 Session state: model_loaded initialized as False")
        if 'current_image' not in st.session_state:
            st.session_state.current_image = None
            logger.info("📝 Session state: current_image initialized as None")
        if 'current_predictions' not in st.session_state:
            st.session_state.current_predictions = None
            logger.info("📝 Session state: current_predictions initialized as None")
        if 'adversarial_image' not in st.session_state:
            st.session_state.adversarial_image = None
            logger.info("📝 Session state: adversarial_image initialized as None")
        if 'adversarial_predictions' not in st.session_state:
            st.session_state.adversarial_predictions = None
            logger.info("📝 Session state: adversarial_predictions initialized as None")
        if 'image_processed' not in st.session_state:
            st.session_state.image_processed = False
            logger.info("📝 Session state: image_processed initialized as False")
        if 'force_sidebar_update' not in st.session_state:
            st.session_state.force_sidebar_update = False
            logger.info("📝 Session state: force_sidebar_update initialized as False")
        
        logger.info("✅ AdversarialComparatorApp initialization complete")
    
    def setup_page(self):
        """Setup page configuration."""
        st.set_page_config(
            page_title=self.config.ui.page_title,
            page_icon=self.config.ui.page_icon,
            layout=self.config.ui.layout
        )
    
    def render_header(self):
        """Render application header."""
        st.title("🎯 Adversarial Comparator")
        st.markdown("**Interactive tool for exploring adversarial attacks on AI models**")
        st.markdown(f"*Phase {self.config.phase}: {self.config.phase_name}*")
        
        # Educational disclaimer
        if self.config.show_disclaimer:
            with st.expander("⚠️ Educational Disclaimer", expanded=False):
                st.warning("""
                **This tool is for EDUCATIONAL and RESEARCH purposes ONLY.**
                
                - Use only for learning about AI vulnerabilities and robustness
                - Do not attempt to harm any real-world systems
                - Respect ethical guidelines and responsible AI practices
                - See [DISCLAIMER.md](DISCLAIMER.md) for complete guidelines
                """)
    
    def render_sidebar(self):
        """Render sidebar controls."""
        logger.info("⚙️ Rendering sidebar controls")
        logger.info(f"📊 Session state - current_image: {st.session_state.current_image is not None}")
        logger.info(f"📊 Session state - model_loaded: {st.session_state.model_loaded}")
        logger.info(f"📊 Session state - image_processed: {st.session_state.image_processed}")
        
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # Model selection
            st.subheader("Model")
            model_type = st.selectbox(
                "Model Type",
                self.model_factory.list_available_models(),
                index=0
            )
            
            # Attack configuration
            st.subheader("Attack Settings")
            attack_type = st.selectbox(
                "Attack Type",
                self.attack_factory.list_available_attacks(),
                index=0
            )
            
            epsilon = st.slider(
                "Epsilon (ε)",
                min_value=self.config.attack.min_epsilon,
                max_value=self.config.attack.max_epsilon,
                value=self.config.attack.default_epsilon,
                step=0.01,
                help="Attack strength parameter"
            )
            
            # Generate attack button
            button_disabled = st.session_state.current_image is None
            logger.info(f"🔘 Button disabled state: {button_disabled}")
            
            if st.button("🚀 Generate Attack", type="primary", disabled=button_disabled):
                logger.info("🔘 Generate Attack button clicked!")
                if st.session_state.current_image is not None:
                    logger.info("✅ Image available, starting attack generation...")
                    self.generate_adversarial_attack(attack_type, epsilon)
                else:
                    logger.error("❌ No image available for attack generation")
                    st.error("Please upload an image first!")
            
            # Show status
            if st.session_state.current_image is None:
                status_msg = "📁 Upload an image to start"
                logger.info("📊 Status: Upload an image to start")
            elif not st.session_state.model_loaded:
                status_msg = "🤖 Loading model..."
                logger.info("📊 Status: Loading model...")
            else:
                status_msg = "✅ Ready to generate attack"
                logger.info("📊 Status: Ready to generate attack")
            
            st.info(status_msg)
            
            # Educational content
            if self.config.show_educational_content:
                st.header("📚 Educational Content")
                with st.expander("What are Adversarial Attacks?"):
                    st.markdown("""
                    **Adversarial attacks** are carefully crafted perturbations that can fool AI models into making incorrect predictions.
                    
                    **FGSM (Fast Gradient Sign Method)**
                    - Single-step gradient-based attack
                    - Fast but less effective than iterative methods
                    - Good for understanding basic adversarial examples
                    - Uses the sign of gradients to create perturbations
                    """)
                
                with st.expander("Understanding Epsilon"):
                    st.markdown("""
                    **Epsilon (ε)** controls the maximum perturbation size:
                    
                    - **Low (0.01-0.05)**: Subtle changes, may not fool the model
                    - **Medium (0.05-0.1)**: Visible changes, good balance
                    - **High (0.1-0.3)**: Obvious changes, high success rate
                    """)
        
        logger.info("✅ Sidebar rendering complete")
    
    def render_main_content(self):
        """Render main content area."""
        logger.info("🎨 Rendering main content area")
        
        # File upload
        st.header("📁 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png', 'webp'],
            help="Upload an image to analyze and attack"
        )
        
        # Reset processed flag if no file is uploaded
        if uploaded_file is None:
            logger.info("📁 No file uploaded, resetting session state")
            st.session_state.image_processed = False
            st.session_state.current_image = None
            st.session_state.current_predictions = None
            st.session_state.adversarial_image = None
            st.session_state.adversarial_predictions = None
            st.session_state.force_sidebar_update = False
        else:
            logger.info(f"📁 File uploaded: {uploaded_file.name}")
        
        if uploaded_file is not None:
            # Process uploaded image
            logger.info("🔄 Processing uploaded image...")
            self.process_uploaded_image(uploaded_file)
        
        # Display results if we have an image
        if st.session_state.current_image is not None:
            logger.info("📊 Displaying results...")
            self.display_results()
        else:
            logger.info("📊 No image to display results for")
        
        # Force sidebar update if needed
        if st.session_state.force_sidebar_update:
            logger.info("🔄 Force sidebar update triggered")
            st.session_state.force_sidebar_update = False
            st.rerun()
    
    def process_uploaded_image(self, uploaded_file):
        """Process uploaded image."""
        logger.info(f"📁 Processing uploaded file: {uploaded_file.name}")
        logger.info(f"📊 File size: {uploaded_file.size} bytes")
        logger.info(f"📊 File type: {uploaded_file.type}")
        
        try:
            # Check if we've already processed this file
            if st.session_state.image_processed:
                logger.info("⏭️ File already processed, skipping...")
                return
            
            logger.info("🔍 Starting file validation...")
            
            # Validate file
            if not self.image_validator.validate_uploaded_file(uploaded_file):
                logger.error("❌ File validation failed!")
                st.error("Invalid file type or size!")
                return
            
            logger.info("✅ File validation passed")
            
            # Read file content once
            logger.info("📖 Reading file content...")
            file_content = uploaded_file.read()
            logger.info(f"📖 File content read: {len(file_content)} bytes")
            
            # Load image
            logger.info("🖼️ Loading image from bytes...")
            image = self.image_processor.load_image_from_bytes(file_content)
            logger.info(f"🖼️ Image loaded: {image.size} {image.mode}")
            
            # Validate image
            logger.info("🔍 Validating image...")
            self.image_processor.validate_image(image)
            logger.info("✅ Image validation passed")
            
            # Store in session state
            logger.info("💾 Storing image in session state...")
            st.session_state.current_image = image
            logger.info("✅ Image stored in session state")
            
            # Show immediate preview
            st.success(f"✅ Image uploaded successfully: {uploaded_file.name}")
            st.image(image, caption="Uploaded Image", use_container_width=True)
            logger.info("🖼️ Image preview displayed")
            
            # Load model if not already loaded
            if self.model is None:
                logger.info("🤖 Model not loaded, loading now...")
                with st.spinner("Loading model..."):
                    self.model = self.model_factory.get_model()
                    st.session_state.model_loaded = True
                    st.success("Model loaded successfully!")
                    logger.info("✅ Model loaded successfully")
            else:
                logger.info("🤖 Model already loaded, skipping...")
            
            # Get predictions
            logger.info("🔮 Getting model predictions...")
            with st.spinner("Analyzing image..."):
                image_tensor = self.model.preprocess(image)
                logger.info(f"🔮 Image preprocessed to tensor: {image_tensor.shape}")
                
                st.session_state.current_predictions = self.model.get_predictions(image_tensor)
                logger.info(f"🔮 Predictions obtained: {len(st.session_state.current_predictions)} predictions")
                
                # Log top prediction
                if st.session_state.current_predictions:
                    top_pred = st.session_state.current_predictions[0]
                    logger.info(f"🏆 Top prediction: {top_pred['class_name']} ({top_pred['confidence']:.3f})")
            
            # Mark as processed to avoid reprocessing
            st.session_state.image_processed = True
            st.session_state.force_sidebar_update = True
            logger.info("✅ Image processing complete, marked as processed")
            logger.info("🔄 Setting force_sidebar_update flag")
            
        except Exception as e:
            logger.error(f"❌ Error processing image: {str(e)}")
            logger.error(f"🔍 Technical details: {traceback.format_exc()}")
            st.error(f"Error processing image: {str(e)}")
            st.error(f"Technical details: {traceback.format_exc()}")
    
    def generate_adversarial_attack(self, attack_type: str, epsilon: float):
        """Generate adversarial attack."""
        logger.info(f"🎯 Starting adversarial attack generation")
        logger.info(f"⚙️ Attack type: {attack_type}")
        logger.info(f"⚙️ Epsilon: {epsilon}")
        
        try:
            # Check if we have an image
            if st.session_state.current_image is None:
                logger.error("❌ No image available for attack generation")
                st.error("Please upload an image first!")
                return
            
            logger.info("✅ Image available for attack generation")
            logger.info(f"🖼️ Current image: {st.session_state.current_image.size} {st.session_state.current_image.mode}")
            
            # Ensure model is loaded
            if self.model is None:
                logger.info("🤖 Model not loaded, loading now...")
                with st.spinner("Loading model..."):
                    self.model = self.model_factory.get_model()
                    st.session_state.model_loaded = True
                    logger.info("✅ Model loaded for attack generation")
            else:
                logger.info("🤖 Model already loaded")
            
            logger.info("🚀 Starting adversarial example generation...")
            with st.spinner("Generating adversarial example..."):
                # Get current image tensor
                logger.info("🔮 Preprocessing image for attack...")
                image_tensor = self.model.preprocess(st.session_state.current_image)
                logger.info(f"🔮 Image tensor shape: {image_tensor.shape}")
                
                # Create attack
                logger.info(f"⚔️ Creating {attack_type} attack with epsilon={epsilon}")
                attack = self.attack_factory.get_attack(attack_type, epsilon=epsilon)
                logger.info(f"⚔️ Attack created: {type(attack).__name__}")
                
                # Generate adversarial example
                logger.info("🎯 Generating adversarial example...")
                adversarial_tensor = attack(image_tensor, self.model.model)
                logger.info(f"🎯 Adversarial tensor generated: {adversarial_tensor.shape}")
                
                # Convert back to PIL image
                logger.info("🖼️ Converting adversarial tensor to PIL image...")
                adversarial_image = self.image_processor.tensor_to_pil(adversarial_tensor)
                logger.info(f"🖼️ Adversarial image created: {adversarial_image.size} {adversarial_image.mode}")
                
                # Store in session state
                logger.info("💾 Storing adversarial image in session state...")
                st.session_state.adversarial_image = adversarial_image
                logger.info("✅ Adversarial image stored in session state")
                
                # Get adversarial predictions
                logger.info("🔮 Getting adversarial predictions...")
                st.session_state.adversarial_predictions = self.model.get_predictions(adversarial_tensor)
                logger.info(f"🔮 Adversarial predictions obtained: {len(st.session_state.adversarial_predictions)} predictions")
                
                # Log adversarial predictions
                if st.session_state.adversarial_predictions:
                    adv_top_pred = st.session_state.adversarial_predictions[0]
                    logger.info(f"🎯 Adversarial top prediction: {adv_top_pred['class_name']} ({adv_top_pred['confidence']:.3f})")
                    
                    # Compare with original
                    if st.session_state.current_predictions:
                        orig_top_pred = st.session_state.current_predictions[0]
                        logger.info(f"🔄 Original vs Adversarial:")
                        logger.info(f"   Original: {orig_top_pred['class_name']} ({orig_top_pred['confidence']:.3f})")
                        logger.info(f"   Adversarial: {adv_top_pred['class_name']} ({adv_top_pred['confidence']:.3f})")
                        
                        if orig_top_pred['class_id'] != adv_top_pred['class_id']:
                            logger.info("🎯 SUCCESS: Attack changed the prediction!")
                        else:
                            logger.info("🛡️ Attack did not change the prediction")
                
                st.success("🎯 Adversarial example generated successfully!")
                st.balloons()
                logger.info("🎉 Adversarial attack generation completed successfully")
                
        except Exception as e:
            logger.error(f"❌ Error generating adversarial example: {str(e)}")
            logger.error(f"🔍 Technical details: {traceback.format_exc()}")
            st.error(f"Error generating adversarial example: {str(e)}")
            st.error(f"Technical details: {traceback.format_exc()}")
    
    def display_results(self):
        """Display comparison results."""
        st.header("📊 Results")
        
        # Show original predictions immediately
        if st.session_state.current_predictions:
            st.subheader("🔍 Original Image Analysis")
            self.display_predictions(st.session_state.current_predictions)
        
        # Create two columns for image comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Original Image")
            st.image(st.session_state.current_image, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Adversarial Image")
            if st.session_state.adversarial_image is not None:
                st.image(st.session_state.adversarial_image, use_container_width=True)
                
                if st.session_state.adversarial_predictions:
                    st.subheader("Adversarial Predictions")
                    self.display_predictions(st.session_state.adversarial_predictions)
            else:
                st.info("Generate an attack to see the adversarial image")
        
        # Comparison analysis
        if (st.session_state.current_predictions and 
            st.session_state.adversarial_predictions):
            self.display_comparison_analysis()
    
    def display_predictions(self, predictions: list):
        """Display prediction results."""
        # Create bar chart
        class_names = [pred['class_name'] for pred in predictions]
        confidences = [pred['confidence'] for pred in predictions]
        
        fig = go.Figure(data=[
            go.Bar(
                x=class_names,
                y=confidences,
                text=[f"{conf:.3f}" for conf in confidences],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Prediction Confidence",
            xaxis_title="Classes",
            yaxis_title="Confidence",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display top prediction
        top_pred = predictions[0]
        st.metric(
            label="Top Prediction",
            value=top_pred['class_name'],
            delta=f"{top_pred['confidence']:.3f}"
        )
    
    def display_comparison_analysis(self):
        """Display comparison analysis."""
        st.header("🔍 Analysis")
        
        original_pred = st.session_state.current_predictions[0]
        adversarial_pred = st.session_state.adversarial_predictions[0]
        
        # Create comparison metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Original Confidence",
                value=f"{original_pred['confidence']:.3f}",
                delta=None
            )
        
        with col2:
            st.metric(
                label="Adversarial Confidence",
                value=f"{adversarial_pred['confidence']:.3f}",
                delta=f"{adversarial_pred['confidence'] - original_pred['confidence']:.3f}"
            )
        
        with col3:
            confidence_drop = original_pred['confidence'] - adversarial_pred['confidence']
            st.metric(
                label="Confidence Drop",
                value=f"{confidence_drop:.3f}",
                delta=None
            )
        
        # Check if attack was successful
        if original_pred['class_id'] != adversarial_pred['class_id']:
            st.success("🎯 Attack Successful! The model's prediction changed.")
        else:
            st.info("🛡️ Attack Unsuccessful. The model's prediction remained the same.")
        
        # Display class change
        st.subheader("Prediction Change")
        st.write(f"**Original**: {original_pred['class_name']} ({original_pred['confidence']:.3f})")
        st.write(f"**Adversarial**: {adversarial_pred['class_name']} ({adversarial_pred['confidence']:.3f})")
    
    def run(self):
        """Run the application."""
        logger.info("🚀 Starting AdversarialComparatorApp")
        
        self.setup_page()
        logger.info("📄 Page setup complete")
        
        self.render_header()
        logger.info("📋 Header rendered")
        
        self.render_sidebar()
        logger.info("⚙️ Sidebar rendered")
        
        self.render_main_content()
        logger.info("🎨 Main content rendered")
        
        logger.info("✅ AdversarialComparatorApp run complete")


def main():
    """Main application entry point."""
    logger.info("🎯 Adversarial Comparator - Application Starting")
    logger.info("=" * 50)
    
    try:
        app = AdversarialComparatorApp()
        app.run()
        logger.info("✅ Application completed successfully")
    except Exception as e:
        logger.error(f"❌ Application failed: {str(e)}")
        logger.error(f"🔍 Technical details: {traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main() 