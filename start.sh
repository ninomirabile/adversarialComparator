#!/bin/bash

# 🎯 Adversarial Comparator - Start Script
# Phase 1: Ultra-Lightweight Implementation

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        REQUIRED_VERSION="3.8"
        
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            print_success "Python $PYTHON_VERSION found (>= $REQUIRED_VERSION required)"
            return 0
        else
            print_error "Python $PYTHON_VERSION found, but $REQUIRED_VERSION or higher is required"
            return 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.8 or higher"
        return 1
    fi
}

# Function to check system requirements
check_system_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python version
    if ! check_python_version; then
        exit 1
    fi
    
    # Check available memory (rough estimate)
    if command_exists free; then
        MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')
        if [ "$MEMORY_GB" -lt 4 ]; then
            print_warning "Only ${MEMORY_GB}GB RAM detected. 4GB+ recommended for optimal performance"
        else
            print_success "Memory: ${MEMORY_GB}GB RAM available"
        fi
    fi
    
    # Check disk space
    DISK_SPACE=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$DISK_SPACE" -lt 1 ]; then
        print_error "Less than 1GB free disk space. Please free up some space"
        exit 1
    else
        print_success "Disk space: ${DISK_SPACE}GB available"
    fi
}

# Function to setup virtual environment
setup_venv() {
    print_status "Setting up virtual environment..."
    
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip >/dev/null 2>&1
}

# Function to check and install dependencies
check_dependencies() {
    print_status "Checking dependencies..."
    
    # List of required packages
    REQUIRED_PACKAGES=(
        "streamlit"
        "torch"
        "torchvision"
        "torchattacks"
        "Pillow"
        "opencv-python"
        "numpy"
        "pandas"
        "plotly"
        "matplotlib"
        "tqdm"
    )
    
    MISSING_PACKAGES=()
    
    for package in "${REQUIRED_PACKAGES[@]}"; do
        if ! python3 -c "import ${package//-/_}" 2>/dev/null; then
            MISSING_PACKAGES+=("$package")
        fi
    done
    
    if [ ${#MISSING_PACKAGES[@]} -eq 0 ]; then
        print_success "All dependencies are installed"
        return 0
    else
        print_warning "Missing packages: ${MISSING_PACKAGES[*]}"
        return 1
    fi
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Install core dependencies
    pip install streamlit torch torchvision torchattacks Pillow opencv-python numpy pandas plotly matplotlib tqdm
    
    print_success "Dependencies installed successfully"
}

# Function to run tests
run_tests() {
    print_status "Running basic tests..."
    
    if python3 test_simple.py; then
        print_success "All tests passed"
        return 0
    else
        print_error "Tests failed"
        return 1
    fi
}

# Function to start the application
start_application() {
    print_status "Starting Adversarial Comparator..."
    
    # Check if port 8501 is available
    if command_exists netstat; then
        if netstat -tuln | grep -q ":8501 "; then
            print_warning "Port 8501 is already in use. The app might not start properly"
        fi
    fi
    
    print_success "Application starting..."
    print_status "The app will open in your browser at: http://localhost:8501"
    print_status "Press Ctrl+C to stop the application"
    echo ""
    
    # Start the application
    streamlit run app.py
}

# Function to cleanup on exit
cleanup() {
    print_status "Cleaning up..."
    # Add any cleanup tasks here if needed
}

# Main execution
main() {
    echo "🎯 Adversarial Comparator - Phase 1"
    echo "=================================="
    echo ""
    
    # Set up signal handlers
    trap cleanup EXIT
    
    # Check system requirements
    check_system_requirements
    
    # Setup virtual environment
    setup_venv
    
    # Check dependencies
    if ! check_dependencies; then
        print_status "Installing missing dependencies..."
        install_dependencies
    fi
    
    # Run tests
    if ! run_tests; then
        print_error "Tests failed. Please check the installation"
        exit 1
    fi
    
    # Start application
    start_application
}

# Run main function
main "$@" 