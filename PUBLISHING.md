# Publishing Guide for Compytroller

This guide covers how to publish the `compytroller` package to PyPI.

## Prerequisites

1. **Install build tools:**
   ```bash
   pip install build twine
   ```

2. **PyPI Account:**
   - Create an account at [https://pypi.org/account/register/](https://pypi.org/account/register/)
   - Verify your email address
   - Set up 2FA (recommended)

3. **API Token:**
   - Go to [https://pypi.org/manage/account/](https://pypi.org/manage/account/)
   - Create an API token with appropriate scope
   - Save it securely

## Pre-Publication Checklist

Before publishing, ensure:

- [ ] All tests pass: `pytest tests/`
- [ ] Coverage is acceptable: `pytest --cov=src/data tests/`
- [ ] Version number is updated in `pyproject.toml`
- [ ] `CHANGELOG.md` is updated with release notes
- [ ] README.md is up to date
- [ ] All dependencies are correctly specified in `pyproject.toml`
- [ ] Documentation is complete
- [ ] License file is present
- [ ] No sensitive information (API keys, tokens) in code

## Building the Package

### Clean Previous Builds

```bash
rm -rf dist/ build/ src/*.egg-info
```

### Build Distribution Files

```bash
python -m build
```

This creates:
- `dist/compytroller-X.Y.Z.tar.gz` (source distribution)
- `dist/compytroller-X.Y.Z-py3-none-any.whl` (wheel distribution)

### Verify the Build

Check the contents:
```bash
tar tzf dist/compytroller-*.tar.gz
unzip -l dist/compytroller-*.whl
```

Ensure:
- All source files are included
- No test files or development artifacts
- LICENSE and README are included

## Testing the Package Locally

### Install from Local Build

```bash
pip install dist/compytroller-*.whl
```

### Test Import

```python
from data import ComptrollerClient
print(ComptrollerClient.__module__)
```

### Uninstall After Testing

```bash
pip uninstall compytroller
```

## Publishing to Test PyPI (Recommended First)

### Configure Test PyPI

Create/edit `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = your-testpypi-token-here
```

### Upload to Test PyPI

```bash
python -m twine upload --repository testpypi dist/*
```

### Test Installation from Test PyPI

```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps compytroller
```

Note: Use `--no-deps` because Test PyPI may not have all dependencies.

### Install with Dependencies

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ compytroller
```

## Publishing to PyPI (Production)

### Final Checks

1. Ensure Test PyPI installation works
2. Verify all functionality with test installation
3. Double-check version number

### Upload to PyPI

```bash
python -m twine upload dist/*
```

Or with explicit credentials:
```bash
python -m twine upload --repository pypi dist/*
```

### Verify Publication

1. Check package page: `https://pypi.org/project/compytroller/`
2. Test installation:
   ```bash
   pip install compytroller
   ```

## Post-Publication

### Tag the Release

```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

### Create GitHub Release

1. Go to repository's Releases page
2. Click "Create a new release"
3. Select the tag you just created
4. Title: `v0.1.0`
5. Description: Copy from CHANGELOG.md
6. Attach dist files (optional)
7. Publish release

### Update Documentation

- Update README if needed
- Update docs/ if you have separate documentation
- Announce on relevant channels

## Version Bumping

For the next release, update version in:
1. `pyproject.toml`: `version = "X.Y.Z"`
2. `src/data/__init__.py`: `__version__ = "X.Y.Z"`
3. `CHANGELOG.md`: Add new [Unreleased] section

### Semantic Versioning

Follow [SemVer](https://semver.org/):
- `MAJOR.MINOR.PATCH` (e.g., 1.2.3)
- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

Examples:
- Bug fix: `0.1.0` → `0.1.1`
- New feature: `0.1.1` → `0.2.0`
- Breaking change: `0.2.0` → `1.0.0`

## Automation with GitHub Actions (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

Add your PyPI API token to GitHub repository secrets as `PYPI_API_TOKEN`.

## Troubleshooting

### Upload Fails with "File already exists"

- You cannot re-upload the same version
- Bump the version number and rebuild
- Consider using Test PyPI for testing

### Import Errors After Installation

- Check package structure in dist files
- Verify `__init__.py` files are present
- Check pyproject.toml `[tool.setuptools.packages.find]` configuration

### Missing Dependencies

- Verify all dependencies are listed in `pyproject.toml`
- Test in a fresh virtual environment

### Build Warnings

- Review and fix any warnings during build
- Common issues: missing files in MANIFEST.in, deprecated configurations

## Helpful Commands

```bash
# Check package metadata
python -m twine check dist/*

# List package contents
tar -tzf dist/*.tar.gz | less

# Verify package structure
unzip -l dist/*.whl | less

# Test installation in isolated environment
python -m venv test_env
source test_env/bin/activate  # or `test_env\Scripts\activate` on Windows
pip install dist/*.whl
python -c "from data import ComptrollerClient; print('Success!')"
deactivate
rm -rf test_env
```

## Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [setuptools Documentation](https://setuptools.pypa.io/)
- [twine Documentation](https://twine.readthedocs.io/)
- [Semantic Versioning](https://semver.org/)
