# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release preparation
- Comprehensive test suite with 99% coverage
- Full API documentation

## [0.1.0] - 2026-01-17

### Added
- ComptrollerClient for accessing Texas Comptroller data
- Sales tax data resources:
  - Active permits
  - Tax rates
  - Allocation history
  - Payment details
  - Single local allocations
  - Marketplace provider data
  - Permitted locations
  - Direct pay taxpayers
  - Quarterly sales history
  - Single local tax rates
  - City/county comparison summaries
  - County/SPD/MTA allocations
- Franchise tax resources:
  - Active permit holders
- Mixed beverage tax resources:
  - Gross receipts
  - Allocation history
- Fluent query builder API with method chaining
- Type-safe response models using dataclasses
- Custom exception hierarchy (HttpError, InvalidRequest)
- Multiple data source support (Socrata API, web scraping, CSV downloads)
- Comprehensive documentation
- Full test coverage (99%)

### Changed
- Standardized method naming across all resources
- Improved error handling with specific exception types
- Enhanced docstrings with Google-style formatting

### Fixed
- Import path consistency
- Error handling in HTTP requests
- Date parsing edge cases

## [0.0.1] - 2024-09-15

### Added
- Initial project structure
- Basic client implementation
- Core resource classes

---

## Release Notes

### Version 0.1.0

This is the first public release of Compytroller, a comprehensive Python library for accessing Texas Comptroller of Public Accounts data. The library provides:

**Key Features:**
- **16 sales tax data resources** covering rates, permits, allocations, and historical data
- **Franchise and mixed beverage tax support** with dedicated resource classes
- **Fluent API** with method chaining for intuitive query construction
- **Type-safe responses** using Python dataclasses with full type hints
- **Multiple data sources** including Socrata API, web scraping, and CSV downloads
- **Comprehensive error handling** with custom exception types
- **99% test coverage** ensuring reliability and stability

**Data Sources Supported:**
- Socrata Open Data API (data.texas.gov)
- Texas Comptroller allocation portal (web scraping)
- CSV data exports

**Python Support:**
- Python 3.8+
- Type hints throughout the codebase
- Fully tested on Python 3.8-3.12

**Dependencies:**
- httpx (HTTP client)
- pandas (data processing)
- selectolax (HTML parsing)

For migration guides and detailed API changes, see the [API documentation](docs/API.md).

[Unreleased]: https://github.com/TeamZac/compytroller-project/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/TeamZac/compytroller-project/releases/tag/v0.1.0
[0.0.1]: https://github.com/TeamZac/compytroller-project/releases/tag/v0.0.1
