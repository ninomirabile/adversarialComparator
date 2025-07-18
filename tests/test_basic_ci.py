"""
Basic test for CI/CD pipeline
"""

import os
import sys


def test_project_structure():
    """Test that required files and directories exist."""
    required_files = [
        "README.md",
        "QUICKSTART.md", 
        "DISCLAIMER.md",
        "LICENSE.md",
        "requirements.txt",
        "app.py"
    ]
    
    required_dirs = [
        "src",
        "docs",
        "tests"
    ]
    
    for file in required_files:
        assert os.path.exists(file), f"Required file {file} not found"
    
    for dir in required_dirs:
        assert os.path.exists(dir), f"Required directory {dir} not found"
    
    print("✅ Project structure validation passed")


def test_src_structure():
    """Test that src directory has required structure."""
    src_dirs = [
        "src/config",
        "src/models", 
        "src/attacks",
        "src/utils"
    ]
    
    src_files = [
        "src/config/settings.py",
        "src/models/base_model.py",
        "src/models/model_factory.py",
        "src/attacks/base_attack.py",
        "src/attacks/attack_factory.py",
        "src/utils/image_processing.py"
    ]
    
    for dir in src_dirs:
        assert os.path.exists(dir), f"Required src directory {dir} not found"
    
    for file in src_files:
        assert os.path.exists(file), f"Required src file {file} not found"
    
    print("✅ Source code structure validation passed")


def test_documentation():
    """Test that documentation files are not empty."""
    doc_files = [
        "README.md",
        "QUICKSTART.md",
        "DISCLAIMER.md"
    ]
    
    for file in doc_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert len(content) > 100, f"Documentation file {file} is too short"
    
    print("✅ Documentation validation passed")


def test_ci_files():
    """Test that CI/CD files exist."""
    ci_files = [
        ".github/workflows/ci-cd.yml",
        ".github/workflows/pr-check.yml",
        ".flake8",
        "pyproject.toml",
        ".markdownlint.json",
        ".pre-commit-config.yaml",
        ".codecov.yml"
    ]
    
    for file in ci_files:
        assert os.path.exists(file), f"CI/CD file {file} not found"
    
    print("✅ CI/CD files validation passed")


def test_gitignore():
    """Test that .gitignore exists and contains required exclusions."""
    assert os.path.exists(".gitignore"), ".gitignore not found"
    
    with open(".gitignore", 'r') as f:
        content = f.read()
        required_exclusions = [
            "__pycache__",
            "venv",
            "ai/",
            "*.log"
        ]
        
        for exclusion in required_exclusions:
            assert exclusion in content, f"Required exclusion '{exclusion}' not found in .gitignore"
    
    print("✅ .gitignore validation passed")


if __name__ == "__main__":
    print("🧪 Running basic CI/CD tests...")
    
    test_project_structure()
    test_src_structure()
    test_documentation()
    test_ci_files()
    test_gitignore()
    
    print("🎉 All basic CI/CD tests passed!") 