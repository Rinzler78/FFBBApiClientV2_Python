#!/bin/bash
# FFBB API Client V2 - Development Environment Setup Script
# This script sets up a complete development environment with all dependencies

set -e  # Exit on any error

echo "🚀 Setting up FFBB API Client V2 Development Environment"
echo "======================================================"

# Check if Python 3.10+ is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION detected. Python $REQUIRED_VERSION or higher is required."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install core dependencies
echo "📚 Installing core dependencies..."
pip install -e .

# Install development and testing dependencies
echo "🛠️  Installing development dependencies..."
pip install -r requirements.txt

# Install pre-commit hooks
if command -v pre-commit &> /dev/null; then
    echo "🔗 Installing pre-commit hooks..."
    pre-commit install
    echo "✅ Pre-commit hooks installed"
else
    echo "⚠️  pre-commit not found. Install with: pip install pre-commit"
fi

# Create .env template if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env template..."
    cat > .env << 'EOF'
# FFBB API Client V2 - Environment Configuration
# Copy this file and replace with your actual tokens

# Optional: Override automatic token retrieval
# API_FFBB_APP_BEARER_TOKEN=your_ffbb_api_token_here
# MEILISEARCH_BEARER_TOKEN=your_meilisearch_token_here

# Development settings
DEBUG=True
EOF
    echo "✅ .env template created"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup Complete!"
echo "================="
echo ""
echo "To activate the virtual environment in new terminal sessions:"
echo "  source .venv/bin/activate"
echo ""
echo "To run tests:"
echo "  python -m pytest"
echo ""
echo "To run the example notebook:"
echo "  jupyter notebook examples/team_analysis_notebook.ipynb"
echo ""
echo "To build documentation:"
echo "  cd docs && make html"
echo ""
echo "Happy coding! 🏀"
