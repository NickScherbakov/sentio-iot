#!/bin/bash

# Sentio IoT - Development Environment Setup Script
# This script sets up the development environment for contributing to Sentio IoT

set -e

echo "🚀 Setting up Sentio IoT Development Environment"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo ""
echo "📋 Checking prerequisites..."

check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 is installed"
        return 0
    else
        echo -e "${RED}✗${NC} $1 is not installed"
        return 1
    fi
}

PREREQ_MET=true

if ! check_command docker; then
    echo -e "${YELLOW}Please install Docker: https://docs.docker.com/get-docker/${NC}"
    PREREQ_MET=false
fi

if ! check_command docker-compose; then
    echo -e "${YELLOW}Please install Docker Compose: https://docs.docker.com/compose/install/${NC}"
    PREREQ_MET=false
fi

if ! check_command python3; then
    echo -e "${YELLOW}Please install Python 3.11+: https://www.python.org/downloads/${NC}"
    PREREQ_MET=false
fi

if ! check_command node; then
    echo -e "${YELLOW}Please install Node.js 18+: https://nodejs.org/${NC}"
    PREREQ_MET=false
fi

if ! check_command git; then
    echo -e "${YELLOW}Please install Git: https://git-scm.com/downloads${NC}"
    PREREQ_MET=false
fi

if [ "$PREREQ_MET" = false ]; then
    echo ""
    echo -e "${RED}❌ Prerequisites not met. Please install missing dependencies.${NC}"
    exit 1
fi

# Create virtual environment for Python
echo ""
echo "🐍 Setting up Python environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Created virtual environment"
else
    echo -e "${YELLOW}⚠${NC} Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
echo -e "${GREEN}✓${NC} Activated virtual environment"

# Install Python development dependencies
echo ""
echo "📦 Installing Python development dependencies..."
pip install --upgrade pip
pip install black isort flake8 mypy pytest pytest-cov pytest-asyncio pre-commit

# Install project dependencies
for dir in api collectors connectors ai-engine; do
    if [ -f "$dir/requirements.txt" ]; then
        echo "  Installing dependencies for $dir..."
        pip install -r "$dir/requirements.txt"
    fi
done

echo -e "${GREEN}✓${NC} Python dependencies installed"

# Setup Node.js environment
echo ""
echo "📦 Setting up Node.js environment..."
cd dashboard
if [ ! -d "node_modules" ]; then
    npm install
    echo -e "${GREEN}✓${NC} Installed Node.js dependencies"
else
    echo -e "${YELLOW}⚠${NC} Node.js dependencies already installed"
fi
cd ..

# Setup pre-commit hooks
echo ""
echo "🔧 Setting up pre-commit hooks..."
pre-commit install
pre-commit install --hook-type commit-msg
echo -e "${GREEN}✓${NC} Pre-commit hooks installed"

# Create required directories
echo ""
echo "📁 Creating required directories..."
mkdir -p data/victoriametrics data/loki data/tempo data/postgres data/redis
mkdir -p models certs
mkdir -p api/tests collectors/tests connectors/tests ai-engine/tests dashboard/src/__tests__

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    # Generate a random JWT secret
    JWT_SECRET=$(openssl rand -hex 32)
    sed -i "s/change-me-in-production/$JWT_SECRET/" .env
    echo -e "${GREEN}✓${NC} Created .env file with secure JWT secret"
else
    echo -e "${YELLOW}⚠${NC} .env file already exists"
fi

# Create pytest configuration
echo ""
echo "🧪 Setting up test configuration..."
cat > pytest.ini << 'EOF'
[pytest]
testpaths = api/tests collectors/tests connectors/tests ai-engine/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --strict-markers
    --cov=.
    --cov-report=term-missing
    --cov-report=html
    --cov-report=xml
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
EOF
echo -e "${GREEN}✓${NC} Created pytest.ini"

# Create sample test files
echo ""
echo "🧪 Creating sample test files..."

# API tests
cat > api/tests/__init__.py << 'EOF'
"""API tests package"""
EOF

cat > api/tests/test_main.py << 'EOF'
"""Sample tests for API service"""
import pytest
from fastapi.testclient import TestClient


def test_placeholder():
    """Placeholder test - replace with actual tests"""
    assert True


# Uncomment when main.py is ready
# from main import app
# 
# client = TestClient(app)
# 
# def test_health_endpoint():
#     response = client.get("/health")
#     assert response.status_code == 200
#     assert "status" in response.json()
EOF

# Create similar test files for other services
for service in collectors connectors ai-engine; do
    mkdir -p "$service/tests"
    cat > "$service/tests/__init__.py" << 'EOF'
"""Tests package"""
EOF
    cat > "$service/tests/test_main.py" << 'EOF'
"""Sample tests"""
import pytest


def test_placeholder():
    """Placeholder test - replace with actual tests"""
    assert True
EOF
done

echo -e "${GREEN}✓${NC} Created sample test files"

# Create development docker-compose override
echo ""
echo "🐳 Creating development docker-compose override..."
cat > docker-compose.dev.yml << 'EOF'
version: '3.8'

# Development overrides for docker-compose.yml
# Use: docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

services:
  api:
    volumes:
      - ./api:/app:cached
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug
    ports:
      - "5678:5678"  # debugpy

  collectors:
    volumes:
      - ./collectors:/app:cached
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug

  connectors:
    volumes:
      - ./connectors:/app:cached
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug

  ai-engine:
    volumes:
      - ./ai-engine:/app:cached
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug

  dashboard:
    volumes:
      - ./dashboard/src:/app/src:cached
    command: npm run dev
    ports:
      - "3000:3000"
      - "5173:5173"  # Vite HMR
EOF
echo -e "${GREEN}✓${NC} Created docker-compose.dev.yml"

# Display helpful information
echo ""
echo "=============================================="
echo -e "${GREEN}✅ Development environment setup complete!${NC}"
echo "=============================================="
echo ""
echo "📚 Next steps:"
echo ""
echo "1. Start the development environment:"
echo "   docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d"
echo ""
echo "2. Run tests:"
echo "   source venv/bin/activate"
echo "   pytest"
echo ""
echo "3. Run linters:"
echo "   black ."
echo "   isort ."
echo "   flake8 ."
echo ""
echo "4. Access services:"
echo "   Dashboard: http://localhost:3000"
echo "   API: http://localhost:8080"
echo "   API Docs: http://localhost:8080/docs"
echo ""
echo "5. View logs:"
echo "   docker-compose logs -f [service_name]"
echo ""
echo "📖 Documentation:"
echo "   docs/README.md - Full documentation"
echo "   CONTRIBUTING.md - Contribution guidelines"
echo ""
echo "💡 Tips:"
echo "   - Pre-commit hooks will run automatically on commit"
echo "   - Run 'pre-commit run --all-files' to check all files"
echo "   - Use 'docker-compose down -v' to reset data volumes"
echo ""
echo "Happy coding! 🚀"
