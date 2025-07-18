# 🚀 Quick Start Guide - Adversarial Comparator

## ⚡ Fast Setup (5 minutes)

### 1. **Prerequisites**
- Python 3.8 or higher
- 4GB+ RAM
- Internet connection (for model download)

### 2. **Installation**
```bash
# Clone the repository
git clone <repository-url>
cd adversarialComparator

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install streamlit torch torchvision torchattacks Pillow opencv-python numpy pandas plotly matplotlib tqdm
```

### 3. **Run the Application**
```bash
# Option 1: Direct launch
streamlit run app.py

# Option 2: Using launcher script
python3 run_app.py
```

### 4. **Open Browser**
Navigate to: `http://localhost:8501`

## 🎯 **How to Use**

### **Step 1: Upload Image**
- Click "Browse files" to upload an image (JPG, PNG, WebP)
- Wait for the model to analyze your image

### **Step 2: Configure Attack**
- Select attack type (FGSM for Phase 1)
- Adjust epsilon (ε) - attack strength:
  - **0.01-0.05**: Subtle changes
  - **0.05-0.1**: Visible changes (recommended)
  - **0.1-0.3**: Obvious changes

### **Step 3: Generate Attack**
- Click "🚀 Generate Attack"
- Wait for the adversarial example to be created

### **Step 4: Analyze Results**
- Compare original vs adversarial images
- See prediction changes and confidence drops
- Learn about the attack effectiveness

## 📊 **What You'll See**

### **Original Image**
- AI model's prediction with confidence scores
- Top 5 class predictions with visualizations

### **Adversarial Image**
- Perturbed version of your image
- New predictions after the attack
- Visual comparison with original

### **Analysis**
- Confidence drop metrics
- Attack success/failure indication
- Educational explanations

## ⚠️ **Important Notes**

### **Educational Purpose Only**
- This tool is for **learning and research**
- Do not use for malicious purposes
- See [DISCLAIMER.md](DISCLAIMER.md) for complete guidelines

### **Performance**
- **First run**: Model download (~50MB) may take 1-2 minutes
- **CPU-only**: Optimized for modest hardware
- **Memory usage**: ~2GB RAM recommended

### **Supported Images**
- **Formats**: JPG, JPEG, PNG, WebP
- **Size**: Up to 10MB
- **Resolution**: Any size (automatically resized)

## 🔧 **Troubleshooting**

### **Import Errors**
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies if needed
pip install -r requirements.txt
```

### **Model Loading Issues**
- Check internet connection
- Ensure sufficient disk space (~100MB)
- Wait for first-time download to complete

### **Memory Issues**
- Close other applications
- Use smaller images
- Restart the application

## 📚 **Learning Resources**

### **Understanding Adversarial Attacks**
- **FGSM**: Fast, single-step gradient-based attack
- **Epsilon**: Controls maximum perturbation size
- **Success Rate**: Higher epsilon = higher success but more visible changes

### **Educational Content**
- Built-in explanations in the sidebar
- Interactive parameter adjustment
- Real-time visualization of effects

## 🎓 **Next Steps**

### **Phase 2 Features** (Coming Soon)
- **PGD Attack**: More effective iterative attack
- **DeepFool**: Minimal perturbation attack
- **Enhanced Visualizations**: Better comparison tools

### **Advanced Usage**
- **Custom Models**: Upload your own models
- **Batch Processing**: Multiple images at once
- **Research Tools**: Export results and analysis

---

## 🆘 **Need Help?**

- **Documentation**: See [docs/](docs/) folder
- **Issues**: Check GitHub issues
- **Support**: Contact project maintainers

---

**🎯 Ready to explore AI vulnerabilities responsibly!** 