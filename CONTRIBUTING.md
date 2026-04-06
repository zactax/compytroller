# Contributing to Compytroller

Thank you for your interest in contributing to Compytroller! This document covers guidelines specific to contributing. For development setup, project structure, and detailed coding standards, see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

## Import Path Convention

**Always use `compytroller` imports**, not `src.compytroller` imports.

```python
# Correct
from compytroller.resources.sales_tax.active_permits import ActivePermits

# Wrong — won't work in the published package
from src.compytroller.resources.sales_tax.active_permits import ActivePermits
```

The project uses a `src` layout (`src/compytroller/`) with `package-dir = {"" = "src"}` in `pyproject.toml`. During development, pytest is configured with `pythonpath = ["src"]` so that `from compytroller.` resolves correctly. Never use the `src.` prefix — it won't exist in the installed package.

This applies to all source code in `src/` and `tests/`.

## Quick Start

1. Fork and clone the repository
2. Install dependencies: `pip install -e ".[dev]"`
3. Run tests: `pytest`
4. Make your changes on a feature branch
5. Ensure all tests pass and coverage remains high
6. Submit a pull request

## Pull Request Process

See the [Contributing Guidelines](docs/DEVELOPMENT.md#contributing-guidelines) section in the Development Guide for details on branch naming, commit messages, and the review process.
