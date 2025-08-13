#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "🚀 Starting local CI replication for FFBBApiClientV2..."
echo "=================================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_step() {
    echo -e "${BLUE}📋 Step: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ Success: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  Warning: $1${NC}"
}

print_error() {
    echo -e "${RED}❌ Error: $1${NC}"
}

print_step "1. Environment Setup"
# Set up environment variables
export PYTHONPATH="${PWD}/src:${PWD}"

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    set -a
    source .env
    set +a
    print_success "Environment variables loaded from .env file"
else
    print_warning ".env file not found, using system environment"
fi

# Verify critical environment variables
if [ -z "$API_FFBB_APP_BEARER_TOKEN" ]; then
    print_error "API_FFBB_APP_BEARER_TOKEN not set"
    exit 1
fi

if [ -z "$MEILISEARCH_BEARER_TOKEN" ]; then
    print_error "MEILISEARCH_BEARER_TOKEN not set"
    exit 1
fi

print_success "Environment variables are properly configured"

print_step "2. Python Environment Verification"
# Check Python version
PYTHON_VERSION=$(python3.11 --version 2>/dev/null || python3 --version)
echo "Using Python: $PYTHON_VERSION"

# Verify required tools
if ! command -v tox &> /dev/null; then
    print_error "tox is not installed. Please install it with: pip install tox or pipx install tox"
    exit 1
fi

if ! command -v pre-commit &> /dev/null; then
    print_error "pre-commit is not installed. Please install it with: pip install pre-commit or pipx install pre-commit"
    exit 1
fi

print_success "All required tools are available"

print_step "3. Pre-commit Hooks Installation"
pre-commit install
print_success "Pre-commit hooks installed"

print_step "4. Running Pre-commit Checks (Code Quality)"
echo "Running all pre-commit hooks on all files..."
pre-commit run --all-files --show-diff-on-failure
print_success "Pre-commit checks passed"

print_step "5. Cleaning Previous Builds"
tox -e clean
print_success "Previous builds cleaned"

print_step "6. Building Package"
echo "Building source distribution and wheel..."
tox -e build
print_success "Package built successfully"

print_step "7. Package Validation with twine"
echo "Validating package distribution files..."
if command -v twine &> /dev/null; then
    twine check dist/*
    print_success "Package validation passed"
else
    print_warning "twine not found, skipping package validation"
fi

print_step "8. Listing Built Artifacts"
echo "Built files in dist/:"
ls -la dist/

# Get the wheel file name
WHEEL_FILE=$(ls dist/*.whl | head -n 1)
if [ -z "$WHEEL_FILE" ]; then
    print_error "No wheel file found in dist/ directory"
    exit 1
fi
echo "Using wheel file: $WHEEL_FILE"

print_step "9. Running Tests with Built Package"
echo "Installing wheel and running tests..."
tox --installpkg "$WHEEL_FILE"
print_success "Tests completed successfully"

print_step "10. Coverage Report Generation"
echo "Generating coverage reports..."
if command -v coverage &> /dev/null; then
    coverage lcov -o coverage.lcov 2>/dev/null || true
    coverage html 2>/dev/null || true
    coverage report
    print_success "Coverage report generated"
else
    print_warning "Coverage tool not found, skipping coverage report"
fi

print_step "11. Final Verification"
echo ""
echo "🎉 LOCAL CI PIPELINE COMPLETED SUCCESSFULLY! 🎉"
echo "=============================================="
echo ""
echo "📊 Results Summary:"
echo "  ✅ Pre-commit checks: PASSED"
echo "  ✅ Package build: PASSED"
echo "  ✅ Tests: PASSED"
echo "  ✅ Code coverage: GENERATED"
echo ""
echo "📁 Generated Files:"
echo "  📦 Package: $WHEEL_FILE"
echo "  📄 Coverage: coverage.lcov"
echo "  🌐 HTML Coverage: htmlcov/index.html"
echo ""
echo "🔍 To view coverage report:"
echo "  open htmlcov/index.html"
echo ""
echo "✨ Your code is ready for production!"
