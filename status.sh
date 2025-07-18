#!/bin/bash

# 🎯 Adversarial Comparator - Status Script
# Phase 1: Ultra-Lightweight Implementation

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

print_header() {
    echo -e "${CYAN}$1${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check application processes
check_processes() {
    print_header "🔍 Process Status"
    
    # Check for Streamlit processes
    STREAMLIT_PIDS=$(pgrep -f "streamlit.*app.py" 2>/dev/null || true)
    if [ -n "$STREAMLIT_PIDS" ]; then
        print_success "Streamlit processes running: $STREAMLIT_PIDS"
    else
        print_status "No Streamlit processes found"
    fi
    
    # Check for Python processes
    PYTHON_PIDS=$(pgrep -f "python.*app.py" 2>/dev/null || true)
    if [ -n "$PYTHON_PIDS" ]; then
        print_success "Python processes running: $PYTHON_PIDS"
    else
        print_status "No Python processes found"
    fi
    
    # Overall status
    if [ -n "$STREAMLIT_PIDS" ] || [ -n "$PYTHON_PIDS" ]; then
        print_success "Application is RUNNING"
        return 0
    else
        print_status "Application is NOT RUNNING"
        return 1
    fi
}

# Function to check port usage
check_port() {
    print_header "🌐 Port Status"
    
    if command_exists netstat; then
        if netstat -tuln | grep -q ":8501 "; then
            print_success "Port 8501 is IN USE"
            print_status "Application should be accessible at http://localhost:8501"
            return 0
        else
            print_status "Port 8501 is FREE"
            return 1
        fi
    elif command_exists ss; then
        if ss -tuln | grep -q ":8501 "; then
            print_success "Port 8501 is IN USE"
            print_status "Application should be accessible at http://localhost:8501"
            return 0
        else
            print_status "Port 8501 is FREE"
            return 1
        fi
    else
        print_warning "Cannot check port usage (netstat/ss not available)"
        return 1
    fi
}

# Function to check virtual environment
check_venv() {
    print_header "🐍 Virtual Environment"
    
    if [ -d "venv" ]; then
        print_success "Virtual environment exists"
        
        # Check if it's activated
        if [ -n "$VIRTUAL_ENV" ]; then
            print_success "Virtual environment is ACTIVATED"
            print_status "Path: $VIRTUAL_ENV"
        else
            print_status "Virtual environment is NOT ACTIVATED"
        fi
    else
        print_warning "Virtual environment does not exist"
        return 1
    fi
}

# Function to check dependencies
check_dependencies() {
    print_header "📦 Dependencies"
    
    if [ -n "$VIRTUAL_ENV" ]; then
        # Activate virtual environment if not already activated
        source venv/bin/activate 2>/dev/null || true
        
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
        INSTALLED_PACKAGES=()
        
        for package in "${REQUIRED_PACKAGES[@]}"; do
            if python3 -c "import ${package//-/_}" 2>/dev/null; then
                INSTALLED_PACKAGES+=("$package")
            else
                MISSING_PACKAGES+=("$package")
            fi
        done
        
        if [ ${#MISSING_PACKAGES[@]} -eq 0 ]; then
            print_success "All dependencies are installed (${#INSTALLED_PACKAGES[@]} packages)"
        else
            print_warning "Missing packages: ${MISSING_PACKAGES[*]}"
            print_status "Installed packages: ${INSTALLED_PACKAGES[*]}"
        fi
    else
        print_warning "Cannot check dependencies (virtual environment not activated)"
    fi
}

# Function to check system resources
check_resources() {
    print_header "💻 System Resources"
    
    # Check memory
    if command_exists free; then
        MEMORY_TOTAL=$(free -g | awk '/^Mem:/{print $2}')
        MEMORY_AVAILABLE=$(free -g | awk '/^Mem:/{print $7}')
        MEMORY_USED=$((MEMORY_TOTAL - MEMORY_AVAILABLE))
        
        print_status "Memory: ${MEMORY_USED}GB used / ${MEMORY_TOTAL}GB total"
        
        if [ "$MEMORY_TOTAL" -lt 4 ]; then
            print_warning "Low memory: ${MEMORY_TOTAL}GB (4GB+ recommended)"
        else
            print_success "Memory: Sufficient (${MEMORY_TOTAL}GB)"
        fi
    fi
    
    # Check disk space
    DISK_TOTAL=$(df -BG . | awk 'NR==2 {print $2}' | sed 's/G//')
    DISK_AVAILABLE=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
    DISK_USED=$((DISK_TOTAL - DISK_AVAILABLE))
    
    print_status "Disk: ${DISK_USED}GB used / ${DISK_TOTAL}GB total (${DISK_AVAILABLE}GB free)"
    
    if [ "$DISK_AVAILABLE" -lt 1 ]; then
        print_warning "Low disk space: ${DISK_AVAILABLE}GB free (1GB+ recommended)"
    else
        print_success "Disk space: Sufficient (${DISK_AVAILABLE}GB free)"
    fi
}

# Function to check Python version
check_python() {
    print_header "🐍 Python Environment"
    
    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        PYTHON_FULL=$(python3 -c 'import sys; print(sys.version)')
        
        print_status "Python version: $PYTHON_VERSION"
        
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            print_success "Python version is compatible (>= 3.8)"
        else
            print_error "Python version is too old (< 3.8)"
        fi
    else
        print_error "Python 3 not found"
    fi
}

# Function to show application info
show_app_info() {
    print_header "📋 Application Information"
    
    if [ -f "app.py" ]; then
        print_success "Main application file exists"
        
        # Get file size
        FILE_SIZE=$(du -h app.py | cut -f1)
        print_status "App size: $FILE_SIZE"
        
        # Get last modified
        LAST_MODIFIED=$(stat -c %y app.py 2>/dev/null || stat -f %Sm app.py 2>/dev/null || echo "Unknown")
        print_status "Last modified: $LAST_MODIFIED"
    else
        print_error "Main application file (app.py) not found"
    fi
    
    # Check configuration
    if [ -f "src/config/settings.py" ]; then
        print_success "Configuration file exists"
    else
        print_warning "Configuration file not found"
    fi
}

# Function to show quick actions
show_actions() {
    print_header "⚡ Quick Actions"
    
    echo "  🚀 Start application:   ./start.sh"
    echo "  🛑 Stop application:    ./stop.sh"
    echo "  🔍 Check status:        ./status.sh"
    echo "  🧪 Run tests:           python3 tests/test_simple.py"
    echo "  📚 View docs:           cat QUICKSTART.md"
}

# Main execution
main() {
    echo "🎯 Adversarial Comparator - Status Report"
    echo "========================================"
    echo ""
    
    # Check application processes
    APP_RUNNING=false
    if check_processes; then
        APP_RUNNING=true
    fi
    
    echo ""
    
    # Check port usage
    PORT_IN_USE=false
    if check_port; then
        PORT_IN_USE=true
    fi
    
    echo ""
    
    # Check virtual environment
    check_venv
    
    echo ""
    
    # Check dependencies
    check_dependencies
    
    echo ""
    
    # Check system resources
    check_resources
    
    echo ""
    
    # Check Python environment
    check_python
    
    echo ""
    
    # Show application info
    show_app_info
    
    echo ""
    
    # Show quick actions
    show_actions
    
    echo ""
    
    # Summary
    print_header "📊 Summary"
    if [ "$APP_RUNNING" = true ]; then
        print_success "✅ Application is RUNNING and ready to use"
        print_status "🌐 Access at: http://localhost:8501"
    else
        print_status "⏸️  Application is NOT RUNNING"
        print_status "🚀 To start: ./start.sh"
    fi
    
    echo ""
    print_status "Status check completed"
}

# Run main function
main "$@" 