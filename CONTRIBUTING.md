# Contributing to Tim

Thank you for your interest in contributing to Tim! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## 📜 Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of terminal/command line usage

### Areas for Contribution

We welcome contributions in the following areas:

- 🐛 **Bug fixes**
- ✨ **New features**
- 📚 **Documentation improvements**
- 🧪 **Test coverage**
- 🎨 **UI/UX enhancements**
- 🌐 **Internationalization**
- 📦 **Package management**

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/tim.git
cd tim
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### 4. Verify Installation

```bash
# Run tests to ensure everything is working
pytest

# Try running the application
python -m tim --help
```

## 🔄 Making Changes

### 1. Create a Branch

```bash
# Create a new branch for your feature/fix
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number
```

### 2. Branch Naming Conventions

- `feature/feature-name` - for new features
- `fix/issue-number` - for bug fixes
- `docs/section-name` - for documentation updates
- `refactor/component-name` - for refactoring
- `test/test-description` - for test improvements

### 3. Making Commits

We use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:

```bash
# Examples
git commit -m "feat: add weekly summary command"
git commit -m "fix: handle timezone conversion properly"
git commit -m "docs: update installation instructions"
git commit -m "test: add tests for streak calculation"
```

#### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=tim

# Run specific test file
pytest tests/test_commands.py

# Run tests matching a pattern
pytest -k "test_streak"
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with the pattern `test_*.py`
- Use descriptive test function names
- Include both positive and negative test cases
- Mock external dependencies (database, file system, etc.)

#### Example Test

```python
def test_add_tag_success(mock_db):
    """Test that add_tag creates a new tag successfully."""
    result = runner.invoke(app, ["add-tag", "Python"])
    assert result.exit_code == 0
    assert "Added tag:" in result.stdout
```

### Test Coverage

We aim for at least 80% test coverage. You can check coverage with:

```bash
pytest --cov=tim --cov-report=html
# Open htmlcov/index.html in your browser
```

## 🎨 Code Style

### Formatting and Linting

We use several tools to maintain code quality:

- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking

These run automatically with pre-commit hooks, but you can also run them manually:

```bash
# Format code
black tim/ tests/

# Sort imports
isort tim/ tests/

# Lint
flake8 tim/ tests/

# Type check
mypy tim/
```

### Style Guidelines

#### Python Code Style

- Follow [PEP 8](https://pep8.org/)
- Use type hints for all function parameters and return values
- Maximum line length: 88 characters (Black's default)
- Use descriptive variable and function names
- Add docstrings to all public functions and classes

#### Example Function

```python
def calculate_streak(sessions: List[Session], tag: str) -> int:
    """Calculate current streak for a specific tag.
    
    Args:
        sessions: List of completed sessions
        tag: Tag name to calculate streak for
        
    Returns:
        Number of consecutive days with activity
        
    Raises:
        ValueError: If tag is empty or None
    """
    if not tag:
        raise ValueError("Tag cannot be empty")
    
    # Implementation here
    return streak_count
```

#### Documentation Style

- Use [Google Style](https://google.github.io/styleguide/pyguide.html) docstrings
- Include type information in docstrings
- Provide examples for complex functions
- Keep README and other docs up to date

### Rich/Terminal UI Guidelines

- Use consistent colors from the Catppuccin palette
- Ensure text is readable in both light and dark terminals
- Include proper spacing and alignment
- Use appropriate Rich components (Tables, Panels, etc.)
- Test UI changes in different terminal sizes

## 📤 Submitting Changes

### 1. Before Submitting

Make sure your changes:

- [ ] Pass all existing tests
- [ ] Include tests for new functionality
- [ ] Follow the code style guidelines
- [ ] Have clear, descriptive commit messages
- [ ] Include documentation updates if needed
- [ ] Don't break existing functionality

### 2. Creating a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a Pull Request on GitHub with:
   - Clear, descriptive title
   - Detailed description of changes
   - Link to related issues
   - Screenshots for UI changes
   - Checklist of completed items

### 3. Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (specify):

## Testing
- [ ] All tests pass
- [ ] Added new tests for new functionality
- [ ] Manual testing completed

## Screenshots
(If applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

### 4. Review Process

- All PRs require at least one review
- Address feedback promptly and professionally
- Keep PRs focused and reasonably sized
- Be patient - maintainers volunteer their time

## 🚀 Release Process

### Version Numbers

We follow [Semantic Versioning](https://semver.org/):

- `MAJOR.MINOR.PATCH`
- MAJOR: Breaking changes
- MINOR: New features (backwards compatible)
- PATCH: Bug fixes (backwards compatible)

### Release Steps (Maintainers Only)

1. Update version in `tim/__init__.py`
2. Update CHANGELOG.md
3. Create release tag
4. Build and publish to PyPI
5. Create GitHub release

## 💬 Communication

### Getting Help

- 💬 **Discussions**: Use [GitHub Discussions](https://github.com/yourusername/tim/discussions) for questions
- 🐛 **Issues**: Use [GitHub Issues](https://github.com/yourusername/tim/issues) for bug reports
- 📧 **Email**: maintainer@tim-tracker.com for security issues

### Proposing Major Changes

For significant changes:

1. Open an issue to discuss the proposal
2. Wait for maintainer feedback
3. Create a detailed design document if needed
4. Implement after agreement

## 🎯 Issue Labels

We use labels to categorize issues and PRs:

- `bug` - Something isn't working
- `enhancement` - New feature request
- `documentation` - Documentation improvements
- `good first issue` - Good for new contributors
- `help wanted` - Looking for contributors
- `question` - Further information requested
- `wontfix` - Won't be implemented

## 🏆 Recognition

Contributors are recognized in:

- GitHub contributors list
- CONTRIBUTORS.md file
- Release notes
- Annual contributor highlights

## 📚 Resources

### Learning Resources

- [Python Developer's Guide](https://devguide.python.org/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Typer Documentation](https://typer.tiangolo.com/)
- [pytest Documentation](https://docs.pytest.org/)

### Tools

- [GitHub CLI](https://cli.github.com/) - Command line GitHub operations
- [pre-commit](https://pre-commit.com/) - Git hooks
- [Black](https://black.readthedocs.io/) - Code formatter
- [mypy](https://mypy.readthedocs.io/) - Type checker

---

Thank you for contributing to Tim! 🙏

If you have any questions about this guide, please open an issue or discussion.
