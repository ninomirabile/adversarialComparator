#!/bin/bash

# 🎯 Adversarial Comparator - Stop Script
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

# Function to find and kill Streamlit processes
kill_streamlit_processes() {
    print_status "Looking for Streamlit processes..."
    
    # Find Streamlit processes
    STREAMLIT_PIDS=$(pgrep -f "streamlit.*app.py" 2>/dev/null || true)
    
    if [ -n "$STREAMLIT_PIDS" ]; then
        print_status "Found Streamlit processes: $STREAMLIT_PIDS"
        
        # Kill processes gracefully first
        for pid in $STREAMLIT_PIDS; do
            print_status "Sending SIGTERM to process $pid..."
            kill -TERM "$pid" 2>/dev/null || true
        done
        
        # Wait a bit for graceful shutdown
        sleep 2
        
        # Check if processes are still running and force kill if necessary
        REMAINING_PIDS=$(pgrep -f "streamlit.*app.py" 2>/dev/null || true)
        if [ -n "$REMAINING_PIDS" ]; then
            print_warning "Some processes still running, force killing..."
            for pid in $REMAINING_PIDS; do
                print_status "Force killing process $pid..."
                kill -KILL "$pid" 2>/dev/null || true
            done
        fi
        
        print_success "Streamlit processes terminated"
    else
        print_status "No Streamlit processes found"
    fi
}

# Function to kill Python processes related to our app
kill_python_processes() {
    print_status "Looking for Python processes related to Adversarial Comparator..."
    
    # Find Python processes that might be running our app
    PYTHON_PIDS=$(pgrep -f "python.*app.py\|python.*streamlit.*app.py" 2>/dev/null || true)
    
    if [ -n "$PYTHON_PIDS" ]; then
        print_status "Found Python processes: $PYTHON_PIDS"
        
        for pid in $PYTHON_PIDS; do
            print_status "Terminating Python process $pid..."
            kill -TERM "$pid" 2>/dev/null || true
        done
        
        sleep 1
        
        # Force kill if still running
        REMAINING_PIDS=$(pgrep -f "python.*app.py\|python.*streamlit.*app.py" 2>/dev/null || true)
        if [ -n "$REMAINING_PIDS" ]; then
            for pid in $REMAINING_PIDS; do
                print_status "Force killing Python process $pid..."
                kill -KILL "$pid" 2>/dev/null || true
            done
        fi
        
        print_success "Python processes terminated"
    else
        print_status "No related Python processes found"
    fi
}

# Function to check if port 8501 is still in use
check_port_usage() {
    print_status "Checking if port 8501 is still in use..."
    
    if command_exists netstat; then
        if netstat -tuln | grep -q ":8501 "; then
            print_warning "Port 8501 is still in use"
            return 1
        else
            print_success "Port 8501 is now free"
            return 0
        fi
    elif command_exists ss; then
        if ss -tuln | grep -q ":8501 "; then
            print_warning "Port 8501 is still in use"
            return 1
        else
            print_success "Port 8501 is now free"
            return 0
        fi
    else
        print_status "Cannot check port usage (netstat/ss not available)"
        return 0
    fi
}

# Function to cleanup temporary files
cleanup_temp_files() {
    print_status "Cleaning up temporary files..."
    
    # Remove any temporary files created by Streamlit
    if [ -d ".streamlit" ]; then
        rm -rf .streamlit/cache 2>/dev/null || true
        print_status "Cleared Streamlit cache"
    fi
    
    # Remove any Python cache files
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    
    print_success "Temporary files cleaned up"
}

# Function to show application status
show_status() {
    print_status "Checking application status..."
    
    # Check for running processes
    STREAMLIT_RUNNING=$(pgrep -f "streamlit.*app.py" 2>/dev/null || true)
    PYTHON_RUNNING=$(pgrep -f "python.*app.py" 2>/dev/null || true)
    
    if [ -n "$STREAMLIT_RUNNING" ] || [ -n "$PYTHON_RUNNING" ]; then
        print_warning "Application is still running"
        echo "  Streamlit PIDs: $STREAMLIT_RUNNING"
        echo "  Python PIDs: $PYTHON_RUNNING"
        return 1
    else
        print_success "Application is not running"
        return 0
    fi
}

# Function to deactivate virtual environment
deactivate_venv() {
    print_status "Deactivating virtual environment..."
    
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate 2>/dev/null || true
        print_success "Virtual environment deactivated"
    else
        print_status "No virtual environment to deactivate"
    fi
}

# Main execution
main() {
    echo "🛑 Adversarial Comparator - Stop Script"
    echo "======================================"
    echo ""
    
    # Kill Streamlit processes
    kill_streamlit_processes
    
    # Kill Python processes
    kill_python_processes
    
    # Wait a moment for processes to terminate
    sleep 1
    
    # Check if port is free
    check_port_usage
    
    # Cleanup temporary files
    cleanup_temp_files
    
    # Show final status
    if show_status; then
        print_success "Application stopped successfully"
    else
        print_warning "Some processes may still be running"
        print_status "You can run this script again to force stop them"
    fi
    
    echo ""
    print_status "Adversarial Comparator has been stopped"
    print_status "To start again, run: ./start.sh"
}

# Run main function
main "$@" 