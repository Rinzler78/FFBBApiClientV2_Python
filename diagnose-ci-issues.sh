#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_title() {
    echo -e "${BLUE}====== $1 ======${NC}"
}

print_check() {
    echo -e "${GREEN}✓${NC} $1"
}

print_issue() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

echo "🔍 GitHub Actions CI Diagnostic Tool"
echo "====================================="
echo ""

print_title "SYSTEM ENVIRONMENT"
echo "Operating System: $(uname -s)"
echo "Architecture: $(uname -m)"
echo "Working Directory: $(pwd)"
echo ""

print_title "PYTHON ENVIRONMENT"
echo "Available Python versions:"
for py in python python3 python3.11 python3.10 python3.9; do
    if command -v $py &> /dev/null; then
        version=$($py --version 2>&1)
        echo "  ✓ $py: $version"
    fi
done

echo ""
echo "Python path configuration:"
echo "  PYTHONPATH: ${PYTHONPATH:-'Not set'}"
echo "  PYTHON_PATH: ${PYTHON_PATH:-'Not set'}"
echo ""

print_title "REQUIRED TOOLS CHECK"
tools=("tox" "pre-commit" "git" "pip" "pipx" "twine")
for tool in "${tools[@]}"; do
    if command -v $tool &> /dev/null; then
        version=$($tool --version 2>&1 | head -n1)
        print_check "$tool is available: $version"
    else
        print_issue "$tool is NOT available"
    fi
done
echo ""

print_title "ENVIRONMENT VARIABLES CHECK"
env_vars=("API_FFBB_APP_BEARER_TOKEN" "MEILISEARCH_BEARER_TOKEN")
for var in "${env_vars[@]}"; do
    if [ -n "${!var}" ]; then
        # Show only first 10 characters for security
        value_preview="${!var:0:10}..."
        print_check "$var is set: $value_preview"
    else
        print_issue "$var is NOT set"
    fi
done
echo ""

print_title ".ENV FILE CHECK"
if [ -f .env ]; then
    print_check ".env file exists"
    echo "Contents (sensitive values masked):"
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        if [[ ! "$key" =~ ^# ]] && [[ -n "$key" ]]; then
            if [[ "$key" == *"TOKEN"* ]] || [[ "$key" == *"KEY"* ]] || [[ "$key" == *"SECRET"* ]]; then
                echo "  $key=${value:0:10}..."
            else
                echo "  $key=$value"
            fi
        fi
    done < .env
else
    print_issue ".env file does NOT exist"
    echo "Consider creating a .env file with:"
    echo "  API_FFBB_APP_BEARER_TOKEN=your_token_here"
    echo "  MEILISEARCH_BEARER_TOKEN=your_token_here"
    echo "  PYTHONPATH=\${PWD}/src:\${PWD}"
fi
echo ""

print_title "PROJECT STRUCTURE CHECK"
required_files=(
    "setup.cfg"
    "pyproject.toml"
    "tox.ini"
    ".pre-commit-config.yaml"
    ".github/workflows/ci.yml"
    "src/ffbb_api_client_v2/__init__.py"
    "tests/"
)

for file in "${required_files[@]}"; do
    if [ -e "$file" ]; then
        print_check "$file exists"
    else
        print_issue "$file does NOT exist"
    fi
done
echo ""

print_title "TOX CONFIGURATION CHECK"
if [ -f tox.ini ]; then
    print_check "tox.ini exists"
    echo "Available tox environments:"
    tox -l 2>/dev/null | sed 's/^/  /'
else
    print_issue "tox.ini does NOT exist"
fi
echo ""

print_title "PRE-COMMIT CONFIGURATION CHECK"
if [ -f .pre-commit-config.yaml ]; then
    print_check ".pre-commit-config.yaml exists"
    if [ -d .git/hooks ] && [ -f .git/hooks/pre-commit ]; then
        print_check "Pre-commit hooks are installed"
    else
        print_warning "Pre-commit hooks are NOT installed (run: pre-commit install)"
    fi
else
    print_issue ".pre-commit-config.yaml does NOT exist"
fi
echo ""

print_title "GIT CONFIGURATION CHECK"
if [ -d .git ]; then
    print_check "Git repository detected"
    echo "Current branch: $(git branch --show-current 2>/dev/null || echo 'unknown')"
    echo "Git status:"
    git status --porcelain | head -5 | sed 's/^/  /'
    uncommitted=$(git status --porcelain | wc -l)
    if [ $uncommitted -gt 0 ]; then
        print_warning "$uncommitted files have uncommitted changes"
    fi
else
    print_issue "NOT a git repository"
fi
echo ""

print_title "GITHUB ACTIONS WORKFLOW CHECK"
if [ -f .github/workflows/ci.yml ]; then
    print_check "GitHub Actions workflow exists"
    echo "Workflow steps configured:"
    grep -E "^\s*-\s*name:" .github/workflows/ci.yml | sed 's/^/  /' || echo "  No named steps found"
else
    print_issue "GitHub Actions workflow does NOT exist"
fi
echo ""

print_title "PACKAGE DEPENDENCIES CHECK"
if [ -f setup.cfg ]; then
    print_check "setup.cfg exists"
    echo "Install requires:"
    grep -A 10 "install_requires" setup.cfg | tail -n +2 | head -10 | sed 's/^/  /' || echo "  Not found in setup.cfg"
fi

if [ -f requirements.txt ]; then
    print_check "requirements.txt exists"
elif [ -f pyproject.toml ]; then
    print_check "pyproject.toml exists (modern Python packaging)"
fi
echo ""

print_title "QUICK IMPORT TEST"
echo "Testing basic imports:"
export PYTHONPATH="${PWD}/src:${PWD}"

# Test basic Python import
if python3 -c "import sys; print('Python import successful')" 2>/dev/null; then
    print_check "Basic Python import works"
else
    print_issue "Basic Python import failed"
fi

# Test package import
if python3 -c "import ffbb_api_client_v2" 2>/dev/null; then
    print_check "Package import works"
else
    print_issue "Package import failed (this is expected if package is not installed)"
fi
echo ""

print_title "PACKAGE VALIDATION TEST"
if [ -d dist/ ] && [ "$(ls -A dist/)" ]; then
    echo "Testing package validation with twine:"
    if command -v twine &> /dev/null; then
        if twine check dist/* 2>/dev/null; then
            print_check "Package validation passes"
        else
            print_issue "Package validation fails - check dist/ contents"
            echo "  Run 'twine check dist/*' for detailed errors"
        fi
    else
        print_warning "twine not available for package validation"
    fi
else
    print_warning "No dist/ directory found - run 'tox -e build' first"
fi
echo ""

print_title "DIAGNOSTIC SUMMARY"
echo "Common GitHub Actions failures and solutions:"
echo ""
echo "1. Environment Variables Missing:"
echo "   - Ensure API_FFBB_APP_BEARER_TOKEN and MEILISEARCH_BEARER_TOKEN are set in GitHub Secrets"
echo "   - Check that secret names match exactly in workflow file"
echo ""
echo "2. Pre-commit Hook Failures:"
echo "   - Run: pre-commit run --all-files locally to fix formatting"
echo "   - Commit formatting changes before pushing"
echo ""
echo "3. Test Failures:"
echo "   - Run tests locally: ./run-ci-locally.sh"
echo "   - Check API token validity"
echo "   - Verify internet connectivity for API calls"
echo ""
echo "4. Package Build Issues:"
echo "   - Verify setup.cfg and pyproject.toml are correct"
echo "   - Check for missing dependencies in install_requires"
echo ""
echo "5. Python Version Issues:"
echo "   - Ensure GitHub Actions uses Python 3.11 (as configured)"
echo "   - Update local Python to match CI version"
echo ""
echo "🔧 To run full local CI simulation: ./run-ci-locally.sh"
echo ""
