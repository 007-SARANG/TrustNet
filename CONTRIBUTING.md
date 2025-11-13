# Contributing to TrustNet 2.0

Thank you for your interest in contributing to TrustNet 2.0! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/trustnet-2.0.git
   cd trustnet-2.0
   ```
3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

1. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

3. **Run tests**
   ```bash
   pytest tests/ -v
   ```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible

## Testing

- Write tests for all new features
- Maintain test coverage above 80%
- Run full test suite before submitting PR

```bash
pytest tests/ --cov=agents --cov=orchestration
```

## Pull Request Process

1. Update README.md with details of changes if needed
2. Update the CHANGELOG.md with a note describing your changes
3. Ensure all tests pass and code follows style guidelines
4. Request review from maintainers

## Agent Development Guidelines

When creating or modifying agents:

1. **Maintain Interface Consistency**: Each agent should have clear input/output contracts
2. **Logging**: Use structured logging for debugging
3. **Error Handling**: Gracefully handle errors and return fallback responses
4. **Performance**: Consider processing time - target <250ms per agent
5. **Metrics**: Track relevant metrics for monitoring

## Documentation

- Update docstrings when modifying functions
- Add examples for complex features
- Update architecture diagrams if structure changes

## Questions?

Open an issue or contact the maintainers.

Thank you for contributing! 🎉
