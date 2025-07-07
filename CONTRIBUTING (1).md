# Contributing to WikiFit

Thank you for your interest in contributing to the WikiFit project! This document provides guidelines and instructions for contributing to make the process smooth and effective.

## Code of Conduct

By participating in this project, you agree to abide by the following principles:

- Be respectful and inclusive of all contributors regardless of background or experience level
- Provide constructive feedback and be open to receiving it
- Focus on what is best for the community and users of the application
- Show empathy towards other community members

## Getting Started

### Setting Up Your Development Environment

1. **Fork the repository** to your GitHub account
2. **Clone your fork** to your local machine
   ```bash
   git clone https://github.com/YOUR-USERNAME/wikifit.git
   cd wikifit
   ```
3. **Set up a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Project Structure

Before making changes, familiarize yourself with the project structure:

- `ai.py` - Main Streamlit application with full features
- `wikifit_basic.py` - Simplified version without AI dependencies
- `wikimedia.py` - Core module containing all Wikimedia API integrations
- `wiki.py` - Backward-compatibility adapter
- `requirements.txt` - Package dependencies
- `README.md` - Project overview and user documentation
- `CHANGELOG.md` - History of changes by version
- `DOCUMENTATION.md` - Detailed technical documentation
- `CONTRIBUTING.md` - This file

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to see if the bug has already been reported
2. **Use the bug report template** when creating a new issue
3. Include:
   - Clear description of the bug
   - Steps to reproduce
   - Expected behavior
   - Screenshots (if applicable)
   - Environment details (OS, Python version, etc.)
   - Possible solution (if you have ideas)

### Suggesting Enhancements

1. **Check existing issues** to avoid duplicates
2. **Use the feature request template** when creating a new issue
3. Include:
   - Clear description of the proposed feature
   - Justification (why this would be useful)
   - Possible implementation approach
   - Any relevant examples or mockups

### Pull Requests

1. **Create a branch** for your changes
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes**, following the coding standards
3. **Add tests** for new functionality
4. **Update documentation** to reflect your changes
5. **Commit your changes** with clear, descriptive commit messages
   ```bash
   git commit -m "Add feature: brief description of what you did"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a pull request** from your branch to the main repository

## Development Guidelines

### Coding Standards

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Include docstrings for all functions, classes, and modules
- Keep functions focused on a single responsibility
- Add comments for complex logic

### Testing

- Add tests for any new functionality
- Make sure all existing tests pass before submitting a PR
- Include both unit tests and integration tests where appropriate

### Documentation

- Update the relevant documentation for any changes you make
- Document any new features or API changes in `DOCUMENTATION.md`
- Add significant changes to `CHANGELOG.md` under the "Unreleased" section

## API Integration Guidelines

When working with Wikimedia API integrations:

1. **Follow the pattern** in `wikimedia.py` for consistency
2. **Include proper error handling**:
   - Handle HTTP status codes appropriately
   - Catch and log exceptions
   - Return user-friendly error messages
3. **Add caching** to wrapper functions in application files
4. **Update the unified search function** to include any new sources

## Review Process

1. At least one maintainer will review your PR
2. Automated tests must pass
3. Code must comply with the project's coding standards
4. Documentation must be updated appropriately
5. Changes may be requested before a PR is merged

## Release Process

1. The maintainers will periodically create releases
2. Version numbers follow [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH)
3. All changes for a release will be documented in the `CHANGELOG.md` file

## Questions?

If you have any questions about contributing, feel free to:
- Open an issue with your question
- Contact the project maintainers directly

Thank you for contributing to WikiFit!


