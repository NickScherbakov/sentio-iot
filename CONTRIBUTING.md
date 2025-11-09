# Contributing to Sentio IoT

Thank you for your interest in contributing to Sentio IoT! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/NickScherbakov/sentio-iot/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Docker version, etc.)
   - Relevant logs or screenshots

### Suggesting Features

1. Check existing [feature requests](https://github.com/NickScherbakov/sentio-iot/issues?q=is%3Aissue+label%3Aenhancement)
2. Create a new issue with:
   - Clear use case
   - Expected behavior
   - Potential implementation approach (optional)

### Pull Requests

1. **Fork the repository**
```bash
git clone https://github.com/YOUR_USERNAME/sentio-iot.git
cd sentio-iot
```

2. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes**
   - Follow code style guidelines
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
```bash
# Run tests
pytest

# Test with Docker
docker-compose up --build
```

5. **Commit your changes**
```bash
git add .
git commit -m "feat: add new feature"
```

Use [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test additions or changes
- `chore:` - Build process or auxiliary tool changes

6. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

7. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Local Development

1. **API Server**
```bash
cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Run tests
pytest

# Format code
black .

# Lint
flake8 .
```

2. **Dashboard**
```bash
cd dashboard
npm install
npm run dev

# Run tests (if added)
npm test

# Lint
npm run lint
```

3. **Collectors**
```bash
cd collectors
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest
```

## Code Style

### Python
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use Black for formatting
- Maximum line length: 100 characters
- Use type hints where possible

### JavaScript/React
- Use ES6+ features
- Use functional components with hooks
- Follow Airbnb style guide
- Use Prettier for formatting

### Documentation
- Use Markdown for documentation
- Keep README files up to date
- Add docstrings to functions and classes
- Comment complex logic

## Testing Guidelines

### Python Tests
```python
def test_feature():
    """Test description"""
    # Arrange
    input_data = {"key": "value"}
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_value
```

### API Tests
```python
def test_api_endpoint(client):
    response = client.post('/api/v1/endpoint', json=data)
    assert response.status_code == 200
    assert 'expected_field' in response.json()
```

## Project Structure

```
sentio-iot/
├── api/              # FastAPI backend
├── collectors/       # Data collection service
├── connectors/       # Protocol connectors
├── ai-engine/        # ML models and AI features
├── dashboard/        # React frontend
├── config/           # Configuration files
├── docs/             # Documentation
├── scripts/          # Utility scripts
└── tests/            # Integration tests
```

## Commit Message Guidelines

Good commit messages:
```
feat: add Zigbee connector
fix: resolve memory leak in collectors
docs: update installation guide
test: add tests for metrics API
```

Bad commit messages:
```
Update code
Fix bug
WIP
asdfgh
```

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Add entry to CHANGELOG.md
4. Request review from maintainers
5. Address review comments
6. Wait for approval and merge

## Getting Help

- Join our [Discussions](https://github.com/NickScherbakov/sentio-iot/discussions)
- Check existing [documentation](docs/)
- Ask questions in issues (tag with "question")

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to Sentio IoT! 🎉
