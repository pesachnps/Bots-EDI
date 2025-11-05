# Contributing to Bots EDI Environment

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/bots-edi-environment.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit and push
7. Create a Pull Request

## Development Setup

### Prerequisites

- Python 3.8+
- Bots EDI framework
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/bots-edi-environment.git
cd bots-edi-environment

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Set up environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
cd env/default
python manage_users.py create admin admin123
```

## Code Style

### Python

We follow PEP 8 style guidelines with some modifications:

- Line length: 100 characters (not 79)
- Use 4 spaces for indentation
- Use double quotes for strings
- Add docstrings to all functions and classes

### Formatting

Use `black` for automatic formatting:

```bash
black env/default/usersys/*.py
```

### Linting

Use `flake8` for linting:

```bash
flake8 env/default/usersys/ --max-line-length=100
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api_auth.py

# Run with coverage
pytest --cov=usersys --cov-report=html

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names
- Include docstrings
- Test both success and failure cases

Example:

```python
def test_api_key_creation():
    """Test that API keys are created with valid format"""
    api_key = APIKey.objects.create(name="Test", user=user)
    assert len(api_key.key) > 40
    assert api_key.is_active is True
```

## Commit Messages

Follow conventional commit format:

```
type(scope): subject

body (optional)

footer (optional)
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(api): add file deletion endpoint

Add DELETE endpoint for removing files from the system.
Includes permission checking and audit logging.

Closes #123
```

```
fix(auth): correct rate limit reset logic

Rate limit was not resetting properly after one hour.
Fixed by using timezone-aware datetime comparison.
```

## Pull Request Process

1. **Update Documentation**: Update README.md, API_DOCUMENTATION.md, or other docs as needed
2. **Add Tests**: Include tests for new features or bug fixes
3. **Update Changelog**: Add entry to CHANGELOG.md (if exists)
4. **Check CI**: Ensure all CI checks pass
5. **Request Review**: Request review from maintainers
6. **Address Feedback**: Make requested changes
7. **Squash Commits**: Squash commits before merge (if requested)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Backward compatible (or breaking changes documented)
```

## Feature Requests

Submit feature requests as GitHub issues with:

- Clear description of the feature
- Use case and benefits
- Proposed implementation (optional)
- Examples (optional)

## Bug Reports

Submit bug reports as GitHub issues with:

- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Error messages and logs
- Screenshots (if applicable)

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
1. Step 1
2. Step 2
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Python: [e.g., 3.9.5]
- Bots: [e.g., 4.0.0]
- Django: [e.g., 3.2.5]

**Logs**
```
Paste relevant logs here
```

**Screenshots**
If applicable
```

## Code Review Guidelines

### For Reviewers

- Be respectful and constructive
- Focus on code, not the person
- Explain reasoning for suggestions
- Approve when satisfied
- Request changes if needed

### For Contributors

- Respond to all comments
- Ask questions if unclear
- Make requested changes
- Mark conversations as resolved
- Be patient and professional

## Documentation

### API Documentation

Update `API_DOCUMENTATION.md` when:

- Adding new endpoints
- Changing request/response formats
- Modifying authentication
- Adding permissions

### Code Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings
- Include parameter types and return types
- Provide examples for complex functions

Example:

```python
def create_api_key(name, user, permissions=None):
    """
    Create a new API key for a user.
    
    Args:
        name (str): Descriptive name for the API key
        user (User): Django user object
        permissions (list, optional): List of permission codes
        
    Returns:
        APIKey: The created API key object
        
    Raises:
        ValueError: If name is empty or user is invalid
        
    Example:
        >>> api_key = create_api_key("Production", user, ["file_upload"])
        >>> print(api_key.key)
        'abc123...'
    """
    # Implementation
```

## Security

- Never commit sensitive data (API keys, passwords, etc.)
- Report security vulnerabilities privately (see SECURITY.md)
- Follow security best practices
- Review SECURITY.md before contributing

## Questions?

- Open a GitHub issue for questions
- Tag with `question` label
- Check existing issues first
- Be specific and provide context

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
