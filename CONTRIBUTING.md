# Contributing to Compytroller

Thank you for your interest in contributing to Compytroller! This document covers guidelines specific to contributing. For development setup, project structure, and detailed coding standards, see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

## Import Path Convention

**Always use `src.data` imports**, not bare `data` imports.

```python
# Correct
from src.data.resources.sales_tax.active_permits import ActivePermits

# Wrong — causes circular imports
from data.resources.sales_tax.active_permits import ActivePermits
```

The project's `pyproject.toml` maps the `data` package to `src/data/` via `package-dir = {"" = "src"}`. This means `data.foo` and `src.data.foo` resolve to the same physical module, but Python treats them as separate modules. Mixing both styles causes circular imports and `isinstance` failures because classes loaded via different paths have different identities.

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
