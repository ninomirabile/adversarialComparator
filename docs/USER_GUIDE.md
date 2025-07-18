# User Guide - Adversarial Comparator

## 📖 Overview

The Adversarial Comparator is an interactive web application designed to demonstrate and visualize adversarial attacks on image classification models. This guide will help you understand how to use the application effectively.

## 🚀 Getting Started

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for initial model download)
- Basic understanding of machine learning concepts (helpful but not required)

### Accessing the Application
1. **Local Installation**: Run `streamlit run app.py` and navigate to `http://localhost:8501`
2. **Cloud Deployment**: Access the hosted version (if available)

## 🎮 Basic Workflow

### Step 1: Upload an Image
1. **Click "Upload Image"** or drag and drop an image file
2. **Supported Formats**: JPG, PNG, WebP
3. **File Size**: Up to 10MB recommended
4. **Image Types**: Any image that can be classified by ImageNet models

**Tips for Best Results**:
- Use clear, high-quality images
- Ensure the main subject is clearly visible
- Avoid heavily compressed or low-resolution images

### Step 2: View Original Prediction
After uploading, you'll see:
- **Original Image**: Your uploaded image
- **Prediction**: Top 5 predicted classes with confidence scores
- **Confidence Bar**: Visual representation of prediction confidence

**Understanding the Results**:
- **Class Name**: The predicted object/category
- **Confidence Score**: Percentage indicating model certainty (0-100%)
- **Ranking**: Top predictions ordered by confidence

### Step 3: Configure Attack Parameters
Choose your attack settings:

#### Attack Type
- **FGSM (Fast Gradient Sign Method)**: Fast, single-step attack
  - **Best for**: Quick demonstrations, understanding basic adversarial examples
  - **Speed**: Very fast (< 1 second)
  - **Effectiveness**: Moderate

- **PGD (Projected Gradient Descent)**: Iterative, more effective attack
  - **Best for**: More realistic adversarial examples
  - **Speed**: Slower (2-5 seconds)
  - **Effectiveness**: High

#### Attack Parameters
- **Epsilon (ε)**: Controls attack strength
  - **Range**: 0.01 to 0.3
  - **Low (0.01-0.05)**: Subtle changes, may not fool the model
  - **Medium (0.05-0.1)**: Visible changes, good balance
  - **High (0.1-0.3)**: Obvious changes, high success rate

- **Iterations** (PGD only): Number of attack steps
  - **Range**: 10 to 100
  - **More iterations**: Better results, slower execution

### Step 4: Generate Adversarial Example
1. **Click "Generate Attack"** to create the adversarial image
2. **Wait for processing** (progress indicator will show)
3. **View results** in the comparison section

### Step 5: Analyze Results
Compare the original and adversarial images:

#### Visual Comparison
- **Side-by-side display** of original vs. adversarial
- **Zoom functionality** to examine details
- **Difference highlighting** (if available)

#### Prediction Changes
- **Before/After predictions** with confidence scores
- **Confidence changes** (increase/decrease percentages)
- **Class ranking changes** (new top predictions)

#### Attack Analysis
- **Success metrics**: Whether the attack fooled the model
- **Perturbation size**: How much the image changed
- **Attack efficiency**: Time taken vs. effectiveness

## 🎓 Educational Features

### Understanding Adversarial Attacks
The application includes educational content explaining:

#### What are Adversarial Attacks?
- **Definition**: Small, carefully crafted perturbations that fool AI models
- **Purpose**: Understanding AI vulnerabilities and improving robustness
- **Real-world Impact**: Safety-critical applications like autonomous vehicles

#### Attack Types Explained
- **FGSM**: Single-step gradient-based attack
- **PGD**: Multi-step iterative attack
- **DeepFool**: Minimal perturbation attack

#### Defense Mechanisms
- **Adversarial Training**: Training models on adversarial examples
- **Input Preprocessing**: Cleaning inputs before classification
- **Model Robustness**: Making models more resistant to attacks

### Interactive Learning
- **Parameter Experimentation**: Try different epsilon values
- **Visual Learning**: See how changes affect predictions
- **Real-time Feedback**: Immediate results for learning

## 🔧 Advanced Usage

### Experimenting with Parameters
1. **Start with low epsilon** (0.01-0.05) to see subtle changes
2. **Gradually increase** to observe how attack strength affects results
3. **Compare different attacks** on the same image
4. **Test various image types** to understand model vulnerabilities

### Best Practices
- **Systematic Testing**: Use consistent parameters across experiments
- **Documentation**: Keep notes of successful attacks
- **Reproducibility**: Use the same images for comparison
- **Ethical Use**: Remember this is for educational purposes only

### Troubleshooting
- **Slow Performance**: Reduce image size or use lower epsilon values
- **Attack Not Working**: Try higher epsilon or different attack type
- **Model Loading Issues**: Check internet connection for initial download
- **Browser Issues**: Try refreshing the page or using a different browser

## 📊 Interpreting Results

### Successful Attack Indicators
- **Confidence Drop**: Original prediction confidence decreases significantly
- **Class Change**: Top prediction changes to a different class
- **Visual Perturbation**: Noticeable but subtle changes in the image

### Attack Effectiveness Metrics
- **Success Rate**: Percentage of attacks that fool the model
- **Confidence Reduction**: How much the original prediction confidence drops
- **Perturbation Magnitude**: Size of changes made to the image

### Understanding Limitations
- **Model Dependencies**: Results vary with different models
- **Image Sensitivity**: Some images are more vulnerable than others
- **Attack Constraints**: Limited by epsilon bounds and model architecture

## 🛡️ Safety and Ethics

### Educational Purpose
- **Research Only**: This tool is for educational and research purposes
- **No Malicious Use**: Do not use for harmful purposes
- **Understanding Vulnerabilities**: Learn to improve AI robustness

### Responsible Usage
- **Respect Privacy**: Don't upload sensitive or personal images
- **Follow Guidelines**: Use within the application's intended scope
- **Report Issues**: Help improve the tool by reporting bugs

### Limitations
- **Demo Environment**: This is a controlled demonstration
- **Model Constraints**: Limited to specific models and attacks
- **Educational Focus**: Not designed for production use

## 📚 Additional Resources

### Further Reading
- **Adversarial Machine Learning**: Academic papers and research
- **AI Security**: Best practices for robust AI systems
- **Computer Vision**: Understanding image classification

### Related Tools
- **RobustBench**: Benchmarking adversarial robustness
- **Foolbox**: Adversarial attack library
- **CleverHans**: Adversarial example library

### Community
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Share experiences and ask questions
- **Contributions**: Help improve the tool

## 🆘 Getting Help

### Common Issues
- **Application not loading**: Check internet connection and browser compatibility
- **Slow performance**: Reduce image size or use lighter settings
- **Attack failures**: Try different parameters or attack types

### Support Channels
- **Documentation**: Check this guide and other docs
- **GitHub Issues**: Report technical problems
- **Community**: Ask questions in discussions

### Feedback
We welcome your feedback to improve the application:
- **Feature Requests**: Suggest new capabilities
- **Bug Reports**: Help identify and fix issues
- **User Experience**: Share your experience and suggestions

---

**Happy Learning! 🎓**

Remember: The goal is to understand AI vulnerabilities to build more robust and secure systems. 