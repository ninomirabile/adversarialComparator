# 🚀 CI/CD Pipeline Guide

## Overview

This project uses GitHub Actions for Continuous Integration and Continuous Deployment (CI/CD). The pipeline ensures code quality, security, and automated testing for every commit and pull request.

## 🔄 Workflows

### 1. **Main CI/CD Pipeline** (`.github/workflows/ci-cd.yml`)

**Triggers**: Push to `main`/`develop`, Pull Requests to `main`

**Jobs**:
- **Test**: Multi-Python version testing (3.8, 3.9, 3.10)
- **Security**: Vulnerability scanning
- **Deploy**: Automatic deployment (main branch only)
- **Documentation**: Documentation validation
- **Performance**: Basic performance checks

### 2. **PR Check** (`.github/workflows/pr-check.yml`)

**Triggers**: Pull Requests to `main`/`develop`

**Jobs**:
- **PR Quality Check**: Fast checks for PR validation

## 🧪 Testing Strategy

### **Multi-Version Testing**
- Tests run on Python 3.8, 3.9, and 3.10
- Each version uses compatible PyTorch version
- Ensures broad compatibility

### **Test Types**
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Memory and speed validation

### **Coverage Reporting**
- Code coverage tracked with pytest-cov
- Reports uploaded to Codecov
- Minimum coverage thresholds enforced

## 🔒 Security Checks

### **Static Analysis**
- **Bandit**: Security vulnerability scanning
- **Safety**: Known vulnerability checking
- **pip-audit**: Dependency vulnerability scanning

### **Code Quality**
- **Flake8**: Style and error checking
- **Black**: Code formatting validation
- **isort**: Import sorting validation
- **MyPy**: Type checking

## 📚 Documentation Validation

### **Markdown Quality**
- **markdownlint**: Markdown syntax validation
- **Link checking**: Broken link detection
- **Completeness check**: Required files validation

### **Required Files**
- `README.md`
- `QUICKSTART.md`
- `DISCLAIMER.md`
- `LICENSE.md`

## 🚀 Deployment

### **Automatic Deployment**
- Triggers on push to `main` branch
- Creates deployment package
- Generates GitHub releases for tags

### **Deployment Package**
- Source code
- Documentation
- Requirements
- License files

## 📊 Performance Monitoring

### **Performance Tests**
- Model loading time validation
- Memory usage monitoring
- Response time checks

### **Thresholds**
- Model loading: < 10 seconds
- Memory usage: < 2GB
- UI responsiveness: < 100ms

## 🛠️ Local Development

### **Pre-commit Setup**
```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run all checks locally
pre-commit run --all-files
```

### **Manual Testing**
```bash
# Run tests
python -m pytest tests/ -v

# Run linting
flake8 src/
black --check src/
isort --check-only src/

# Run type checking
mypy src/

# Run security scan
bandit -r src/
```

## 📈 Metrics and Reporting

### **Coverage Reports**
- HTML coverage reports generated
- Uploaded as artifacts
- Available in GitHub Actions

### **Security Reports**
- Bandit security scan results
- Safety vulnerability reports
- pip-audit dependency reports

### **Performance Metrics**
- Model loading times
- Memory usage statistics
- Response time measurements

## 🔧 Configuration Files

### **Code Quality Tools**
- `.flake8`: Flake8 configuration
- `pyproject.toml`: Black, isort, mypy, pytest configuration
- `.markdownlint.json`: Markdown linting rules

### **GitHub Actions**
- `.github/workflows/ci-cd.yml`: Main pipeline
- `.github/workflows/pr-check.yml`: PR validation

## 🚨 Troubleshooting

### **Common Issues**

#### **Test Failures**
```bash
# Check test output
python -m pytest tests/ -v -s

# Run specific test
python -m pytest tests/test_specific.py -v
```

#### **Linting Issues**
```bash
# Auto-fix formatting
black src/
isort src/

# Check specific issues
flake8 src/ --select=E9,F63,F7,F82
```

#### **Type Checking Issues**
```bash
# Run mypy with verbose output
mypy src/ --verbose

# Ignore specific modules
mypy src/ --ignore-missing-imports
```

### **Performance Issues**
```bash
# Profile memory usage
python -m memory_profiler your_script.py

# Check system resources
python -c "import psutil; print(psutil.virtual_memory())"
```

## 🎯 Best Practices

### **For Contributors**
1. **Run tests locally** before pushing
2. **Follow code style** (Black, isort)
3. **Add tests** for new features
4. **Update documentation** when needed
5. **Check security** with bandit

### **For Maintainers**
1. **Monitor CI/CD** pipeline health
2. **Review security reports** regularly
3. **Update dependencies** when needed
4. **Maintain test coverage** above 80%
5. **Document changes** in releases

## 📞 Support

### **CI/CD Issues**
- Check GitHub Actions logs
- Review configuration files
- Test locally first

### **Performance Issues**
- Monitor resource usage
- Check model loading times
- Validate memory consumption

### **Security Concerns**
- Review security scan reports
- Update vulnerable dependencies
- Follow security best practices

---

**🎯 This CI/CD pipeline ensures the Adversarial Comparator maintains high quality, security, and reliability for educational use.** 