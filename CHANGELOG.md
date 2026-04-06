# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-04-05

### Changed
- **BREAKING:** Renamed package from `data` to `compytroller` — all imports change from `from data import ...` to `from compytroller import ...`
- Fixed packaging bug where `src.` prefix in internal imports made the published wheel non-functional
- Minimum Python version bumped from 3.8 to 3.10

### Added
- Type-safe field enums for all dataset resources (`ActivePermitField`, `SalesTaxRateField`, `FranchiseTaxPermitHolderField`, `MixedBeverageGrossReceiptsField`, etc.)
- Categorical enums for filter values (`AuthorityType`, `RightToTransactCode`, `SalesTaxRateType`)
- Union type hints (`str | FieldEnum`) on `sort_by()` and categorical filter methods for IDE discoverability
- CONTRIBUTING.md with import path conventions
- Field enums documentation in README, API reference, and examples

### Fixed
- Fixed 17 incorrect method names in `example_usage.ipynb`
- Fixed circular import caused by mixed `data.` vs `src.data.` import paths

## [0.1.0] - 2026-04-03

Initial public release.

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
- Type-safe field enums for all dataset resources (`ActivePermitField`, `SalesTaxRateField`, `FranchiseTaxPermitHolderField`, `MixedBeverageGrossReceiptsField`, etc.)
- Categorical enums for filter values (`AuthorityType`, `RightToTransactCode`, `SalesTaxRateType`)
- Union type hints (`str | FieldEnum`) on `sort_by()` and categorical filter methods for IDE discoverability
- Custom exception hierarchy (HttpError, InvalidRequest)
- Multiple data source support (Socrata API, web scraping, CSV downloads)
- Comprehensive documentation
- Full test coverage (99%)
- CONTRIBUTING.md with import path conventions

---

## Release Notes

### Version 0.1.0

This is the first public release of Compytroller, a comprehensive Python library for accessing Texas Comptroller of Public Accounts data. The library provides:

**Key Features:**
- **16 sales tax data resources** covering rates, permits, allocations, and historical data
- **Franchise and mixed beverage tax support** with dedicated resource classes
- **Fluent API** with method chaining for intuitive query construction
- **Type-safe responses** using Python dataclasses with full type hints
- **Type-safe field enums** for IDE discoverability on `sort_by()` and categorical filters
- **Multiple data sources** including Socrata API, web scraping, and CSV downloads
- **Comprehensive error handling** with custom exception types
- **99% test coverage** ensuring reliability and stability

**Python Support:**
- Python 3.10+
- Type hints throughout the codebase
- Fully tested on Python 3.10-3.12

**Dependencies:**
- httpx (HTTP client)
- pandas (data processing)
- selectolax (HTML parsing)

For detailed API documentation, see the [API reference](docs/API.md).

[0.2.0]: https://github.com/TeamZac/compytroller-project/releases/tag/v0.2.0
[0.1.0]: https://github.com/TeamZac/compytroller-project/releases/tag/v0.1.0
