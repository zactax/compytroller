# Compytroller

A Python library for accessing Texas Comptroller of Public Accounts tax and financial data.

## Overview

Compytroller provides a clean, type-safe interface to Texas Comptroller data from multiple sources:
- Socrata Open Data API (data.texas.gov)
- Texas Comptroller web forms
- CSV data exports

The library supports:
- Sales tax data (rates, permits, allocations, quarterly sales)
- Franchise tax data (permit holders)
- Mixed beverage tax data (receipts, allocations)

## Installation

### From PyPI (Recommended)

```bash
pip install compytroller
```

### From Source

```bash
git clone https://github.com/TeamZac/compytroller-project.git
cd compytroller-project
pip install -e .
```

### Development Installation

To install with development dependencies:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from data import ComptrollerClient

# Initialize the client with your Socrata app token
client = ComptrollerClient(app_token="your-app-token-here")

# Get sales tax rates for a specific city
rates = (client.sales_tax()
    .rates()
    .in_city("Austin")
    .get())

# Get active permits for a taxpayer
permits = (client.sales_tax()
    .active_permits()
    .for_taxpayer("12345678")
    .get())

# Get franchise tax permit holders
franchise = (client.franchise_tax()
    .active_permit_holders()
    .for_taxpayer("12345678")
    .get())

# Get mixed beverage gross receipts
receipts = (client.mixed_beverage_tax()
    .gross_receipts()
    .for_year(2024)
    .get())
```

## Features

### Fluent Query Builder API
All data sources support method chaining for intuitive query construction:

```python
results = (client.sales_tax()
    .active_permits()
    .in_city("Houston")
    .in_county("Harris")
    .issued_after("2024-01-01")
    .sort_by("outlet_city", desc=True)
    .limit(100)
    .get())
```

### Type-Safe Responses
All responses are returned as Python dataclasses with full type hints:

```python
from data.responses.sales_tax import ActivePermitData

permits: list[ActivePermitData] = client.sales_tax().active_permits().get()
for permit in permits:
    print(f"{permit.taxpayer_name} - {permit.outlet_city}")
```

### Multiple Data Sources
- **Socrata API**: Primary source for most datasets
- **Web Scraping**: Historical allocation data via state forms
- **CSV Downloads**: Marketplace provider lists

### Comprehensive Error Handling
Custom exceptions for clear error messages:

```python
from data.exceptions import HttpError, InvalidRequest

try:
    results = client.sales_tax().rates().get()
except HttpError as e:
    print(f"HTTP Error {e.status_code}: {e.url}")
except InvalidRequest as e:
    print(f"Invalid request: {e}")
```

## Available Data Sources

### Sales Tax
- `active_permits()` - Active sales tax permits
- `rates()` - Sales tax rate changes
- `allocation_history()` - Historical allocation data
- `allocation_payment_details()` - Detailed payment breakdowns
- `single_local_allocations()` - Single local jurisdiction allocations
- `marketplace_provider_allocations()` - Marketplace provider allocations
- `marketplace_provider()` - Marketplace provider registry
- `permitted_locations()` - Permitted location details
- `direct_pay_taxpayers()` - Direct pay taxpayer list
- `quarterly_sales_history()` - Quarterly sales by jurisdiction/industry
- `single_local_tax_rates()` - Single local tax rates
- `city_county_comparison_summary()` - City/county payment comparisons
- `county_spd_mta_allocations()` - County/SPD/MTA allocations

### Franchise Tax
- `active_permit_holders()` - Active franchise tax permit holders

### Mixed Beverage Tax
- `gross_receipts()` - Gross receipts by beverage type
- `history()` - Historical allocation data

## Documentation

- [API Reference](docs/API.md) - Complete API documentation
- [Usage Examples](docs/EXAMPLES.md) - Common usage patterns
- [Data Sources](docs/DATA_SOURCES.md) - Detailed data source reference
- [Development Guide](docs/DEVELOPMENT.md) - Contributing and development setup

## Authentication

Most data sources require a Socrata app token. Get yours at:
https://data.texas.gov/profile/app_tokens

## Requirements

- Python 3.8+
- httpx
- pandas
- selectolax

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for development setup and guidelines.

## Support

For issues and feature requests, please use the GitHub issue tracker.
