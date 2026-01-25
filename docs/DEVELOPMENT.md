# Development Guide

Guide for contributing to and developing Compytroller.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Code Style](#code-style)
- [Testing](#testing)
- [Adding New Features](#adding-new-features)
- [Debugging](#debugging)
- [Release Process](#release-process)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Clone the Repository

```bash
git clone https://github.com/your-org/compytroller.git
cd compytroller
```

## Development Setup

### Install Dependencies

```bash
# Install runtime dependencies
pip install httpx pandas selectolax

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

### Configure Python Path

The project uses `src/` layout. Set your Python path:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

Or use the pytest configuration which sets this automatically.

### Get a Socrata App Token

For testing against live data:

1. Sign up at https://data.texas.gov
2. Generate an app token at https://data.texas.gov/profile/edit/developer_settings
3. Set environment variable:

```bash
export SOCRATA_APP_TOKEN="your-token-here"
```

## Project Structure

```
compytroller-project/
├── src/data/                      # Main source code
│   ├── __init__.py                # Package exports
│   ├── client.py                  # ComptrollerClient
│   ├── socrata.py                 # SocrataClient (HTTP layer)
│   ├── exceptions.py              # Custom exceptions
│   ├── utils.py                   # Utility functions
│   ├── resources/                 # Resource factories
│   │   ├── resources.py           # Main resource classes
│   │   ├── sales_tax/             # Sales tax data sources
│   │   ├── franchise/             # Franchise tax data sources
│   │   └── mixed_beverage/        # Mixed beverage tax data sources
│   └── responses/                 # Data model classes
│       ├── sales_tax.py
│       ├── franchise_tax.py
│       └── mixed_beverage_tax.py
├── tests/                         # Test suite
│   ├── conftest.py                # Shared fixtures
│   ├── test_*.py                  # Test modules
│   ├── sales_tax/                 # Sales tax tests
│   ├── franchise_tax/             # Franchise tax tests
│   └── mixed_beverage_tax/        # Mixed beverage tax tests
├── docs/                          # Documentation
│   ├── API.md
│   ├── EXAMPLES.md
│   ├── DATA_SOURCES.md
│   └── DEVELOPMENT.md (this file)
├── pyproject.toml                 # Project configuration
└── README.md                      # Main documentation
```

## Code Style

### Python Style Guide

Follow PEP 8 with these conventions:

- **Line length**: 100 characters max
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Type hints**: Required for all public functions
- **Docstrings**: Google style for public APIs

### Type Hints

All public functions must have type hints:

```python
def parse_date(x: str) -> Optional[date]:
    """Parse a date string into a date object."""
    pass
```

### Naming Conventions

- **Classes**: PascalCase (`ComptrollerClient`, `ActivePermits`)
- **Functions/Methods**: snake_case (`get_data`, `for_taxpayer`)
- **Constants**: UPPER_SNAKE_CASE (`DATASET_ID`, `BASE_URL`)
- **Private members**: Leading underscore (`_build_params`)

### Formatting

Use Black for automatic formatting:

```bash
black src/ tests/
```

### Linting

```bash
# Check code style
flake8 src/ tests/

# Type checking
mypy src/
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_client.py

# Run specific test
pytest tests/test_client.py::test_factory_method

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run tests in a specific directory
pytest tests/sales_tax/
```

### Test Structure

Tests are organized by module:

```
tests/
├── conftest.py              # Shared fixtures (DummyClient, etc.)
├── test_client.py           # ComptrollerClient tests
├── test_socrata_client.py   # SocrataClient tests
├── test_utils.py            # Utility function tests
├── test_exceptions.py       # Exception class tests
├── test_resources.py        # Resource factory tests
└── [domain]/                # Domain-specific tests
    └── test_[source].py     # Individual data source tests
```

### Writing Tests

#### Unit Tests

Test individual components in isolation:

```python
from data.utils import parse_date

def test_parse_date_valid():
    result = parse_date("2024-01-15")
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 15

def test_parse_date_invalid():
    result = parse_date("invalid")
    assert result is None
```

#### Integration Tests

Test components working together:

```python
from unittest.mock import Mock, patch
from data.resources.sales_tax.active_permits import ActivePermits

def test_active_permits_query():
    mock_client = Mock()
    mock_client.get.return_value = [
        {"taxpayer_number": "12345", "taxpayer_name": "Test Corp"}
    ]

    permits = ActivePermits(mock_client).for_taxpayer("12345").get()

    assert len(permits) == 1
    assert permits[0].taxpayer_number == "12345"
```

#### Fixture Usage

Use the DummyClient fixture for tests:

```python
def test_with_dummy_client(dummy_client):
    # dummy_client is provided by conftest.py
    resource = dummy_client.sales_tax().active_permits()
    assert resource is not None
```

### Test Coverage

Maintain >99% code coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

Focus on:
- All public methods
- Error handling paths
- Edge cases (null values, empty results, etc.)
- Data parsing and transformation

## Adding New Features

### Adding a New Data Source

1. **Identify the data source**
   - Socrata dataset ID, web form URL, or CSV URL
   - Available fields
   - Update frequency

2. **Create the data model** (in `src/data/responses/`)

```python
from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class NewDataSourceData:
    """Description of the data."""
    field1: str
    field2: Optional[str] = None
    field3: Optional[date] = None

    @classmethod
    def from_dict(cls, data: dict) -> "NewDataSourceData":
        return cls(
            field1=data.get("field1", ""),
            field2=data.get("field2"),
            field3=parse_date(data.get("field3"))
        )
```

3. **Create the data source class** (in `src/data/resources/[domain]/`)

```python
from typing import List, Optional
from data.responses.domain import NewDataSourceData

class NewDataSource:
    """Query new data source."""

    DATASET_ID = "abcd-1234"  # Socrata dataset ID

    def __init__(self, client):
        self._client = client
        self._params = {}

    def for_something(self, value: str) -> "NewDataSource":
        """Filter by something."""
        self._params["field"] = value
        return self

    def limit(self, n: int) -> "NewDataSource":
        """Limit results."""
        self._params["$limit"] = n
        return self

    def reset(self) -> "NewDataSource":
        """Clear all filters."""
        self._params = {}
        return self

    def get(self) -> List[NewDataSourceData]:
        """Execute query."""
        raw_data = self._client.get(self.DATASET_ID, self._params)
        return [NewDataSourceData.from_dict(item) for item in raw_data]
```

4. **Add to resource factory** (in `src/data/resources/resources.py`)

```python
def new_data_source(self) -> NewDataSource:
    """Access new data source."""
    return NewDataSource(self._client)
```

5. **Write tests** (in `tests/[domain]/test_new_data_source.py`)

```python
from unittest.mock import Mock
from data.resources.domain.new_data_source import NewDataSource

def test_new_data_source_filter():
    mock_client = Mock()
    mock_client.get.return_value = [{"field1": "value"}]

    source = NewDataSource(mock_client)
    results = source.for_something("test").get()

    assert len(results) == 1
    mock_client.get.assert_called_once()
```

6. **Update documentation**
   - Add to README.md data source list
   - Add API reference in docs/API.md
   - Add examples in docs/EXAMPLES.md
   - Add data source details in docs/DATA_SOURCES.md

### Adding a New Filter Method

Add filter methods to existing data source classes:

```python
def for_new_field(self, value: str) -> "DataSource":
    """Filter by new field."""
    self._params["new_field"] = value
    return self
```

Ensure:
- Method returns `self` for chaining
- Parameter is validated if needed
- Method is documented with docstring
- Tests are added

### Adding Utility Functions

Add to `src/data/utils.py`:

```python
def parse_new_type(value: Any) -> Optional[NewType]:
    """Parse a new type from various inputs."""
    try:
        # Parsing logic
        return result
    except (ValueError, TypeError):
        return None
```

Requirements:
- Type hints
- Error handling (return None on error)
- Unit tests
- Docstring

## Debugging

### Debug Logging

Add debug prints during development:

```python
def get(self):
    params = self._params
    print(f"DEBUG: Querying with params: {params}")
    result = self._client.get(self.DATASET_ID, params)
    print(f"DEBUG: Got {len(result)} results")
    return [...]
```

### Interactive Testing

Use IPython or Jupyter for interactive development:

```python
from data import ComptrollerClient

client = ComptrollerClient.factory("your-token")

# Test queries interactively
permits = client.sales_tax().active_permits().limit(5).get()
print(permits)
```

### Mock HTTP Calls

For debugging without hitting real APIs:

```python
from unittest.mock import Mock

mock_client = Mock()
mock_client.get.return_value = [{"test": "data"}]

source = DataSource(mock_client)
results = source.get()
```

### Inspecting Socrata Queries

Check what parameters are being sent:

```python
source = client.sales_tax().active_permits()
source.for_city("Austin").limit(10)

# Access internal params
print(source._params)
# Output: {'outlet_city': 'Austin', '$limit': 10}
```

### Testing Web Scraping

For web scraping sources, save HTML responses for testing:

```bash
curl -X POST https://mycpa.cpa.state.tx.us/allocation/ \
  -d "city=Austin" > test_response.html
```

Then write tests against saved HTML.

## Release Process

### Version Numbering

Follow Semantic Versioning (semver):
- **Major**: Breaking changes (2.0.0)
- **Minor**: New features, backwards compatible (1.1.0)
- **Patch**: Bug fixes (1.0.1)

### Pre-Release Checklist

- [ ] All tests passing
- [ ] Code coverage >99%
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in setup.py/pyproject.toml
- [ ] No debug code or print statements

### Release Steps

1. **Update version number**

```python
# In setup.py or pyproject.toml
version = "1.2.0"
```

2. **Update CHANGELOG.md**

```markdown
## [1.2.0] - 2024-01-15

### Added
- New data source for XYZ
- Filter method for ABC

### Fixed
- Bug in date parsing
```

3. **Commit changes**

```bash
git add .
git commit -m "Release v1.2.0"
git tag v1.2.0
```

4. **Push to repository**

```bash
git push origin main
git push origin v1.2.0
```

5. **Build and publish** (if publishing to PyPI)

```bash
python -m build
python -m twine upload dist/*
```

## Contributing Guidelines

### Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**

```bash
git checkout -b feature/new-data-source
```

3. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

4. **Run tests and linting**

```bash
pytest
black src/ tests/
flake8 src/ tests/
```

5. **Commit with clear messages**

```bash
git commit -m "Add support for new data source"
```

6. **Push and create PR**

```bash
git push origin feature/new-data-source
```

### Commit Message Format

Use conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `test`: Adding tests
- `refactor`: Code refactoring
- `style`: Formatting changes
- `chore`: Maintenance tasks

Examples:
```
feat(sales-tax): add quarterly sales data source
fix(parsing): handle null values in date fields
docs(api): update API reference for new methods
test(permits): add integration tests for active permits
```

### Code Review

PRs will be reviewed for:
- Code quality and style
- Test coverage
- Documentation
- Breaking changes
- Performance implications

## Getting Help

- **GitHub Issues**: Report bugs or request features
- **Discussions**: Ask questions or share ideas
- **Documentation**: Check docs/ directory

## License

See LICENSE file for details.
