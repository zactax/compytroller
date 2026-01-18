# API Reference

Complete API documentation for Compytroller.

## Table of Contents

- [Client](#client)
- [Resources](#resources)
- [Sales Tax Data Sources](#sales-tax-data-sources)
- [Franchise Tax Data Sources](#franchise-tax-data-sources)
- [Mixed Beverage Tax Data Sources](#mixed-beverage-tax-data-sources)
- [Response Models](#response-models)
- [Exceptions](#exceptions)
- [Utilities](#utilities)

## Client

### ComptrollerClient

Main entry point for accessing Texas Comptroller data.

#### Factory Method

```python
ComptrollerClient.factory(app_token: str) -> ComptrollerClient
```

Creates a new client instance with the provided Socrata app token.

**Parameters:**
- `app_token` (str): Your Socrata application token from data.texas.gov

**Returns:**
- `ComptrollerClient`: Configured client instance

**Example:**
```python
from data import ComptrollerClient

client = ComptrollerClient.factory("your-app-token")
```

#### Methods

##### sales_tax()

```python
sales_tax() -> SalesTaxResource
```

Returns a resource factory for sales tax data sources.

**Returns:**
- `SalesTaxResource`: Sales tax resource factory

##### franchise_tax()

```python
franchise_tax() -> FranchiseResource
```

Returns a resource factory for franchise tax data sources.

**Returns:**
- `FranchiseResource`: Franchise tax resource factory

##### mixed_beverage_tax()

```python
mixed_beverage_tax() -> MixedBeverageResource
```

Returns a resource factory for mixed beverage tax data sources.

**Returns:**
- `MixedBeverageResource`: Mixed beverage tax resource factory

##### get()

```python
get(dataset_id: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]
```

Direct access to Socrata API for custom queries.

**Parameters:**
- `dataset_id` (str): Socrata dataset identifier
- `params` (dict, optional): Query parameters

**Returns:**
- `List[Dict]`: Raw JSON response data

## Resources

### SalesTaxResource

Factory for sales tax data sources.

#### Methods

- `active_permits() -> ActivePermits`
- `rates() -> SalesTaxRates`
- `allocation_history() -> SalesTaxAllocationHistory`
- `allocation_payment_details() -> LocalAllocationPaymentDetail`
- `single_local_allocations() -> SingleLocalAllocations`
- `marketplace_provider_allocations() -> MarketplaceProviderAllocations`
- `marketplace_provider() -> MarketplaceProvider`
- `permitted_locations() -> PermittedLocations`
- `direct_pay_taxpayers() -> DirectPayTaxpayers`
- `quarterly_sales_history() -> QuarterlySalesHistory`
- `single_local_tax_rates() -> SingleLocalTaxRates`
- `city_county_comparison_summary() -> CityCountyComparisonSummary`
- `county_spd_mta_allocations() -> CountySPDMTAAllocations`

### FranchiseResource

Factory for franchise tax data sources.

#### Methods

- `active_permit_holders() -> ActiveFranchiseTaxPermitHolders`

### MixedBeverageResource

Factory for mixed beverage tax data sources.

#### Methods

- `gross_receipts() -> MixedBeverageGrossReceipts`
- `history() -> MixedBeverageHistory`

## Sales Tax Data Sources

### ActivePermits

Query active sales tax permits.

**Socrata Dataset ID:** `jrea-zgmq`

#### Filter Methods

```python
for_taxpayer(taxpayer_number: str) -> Self
```
Filter by taxpayer number.

```python
for_outlet(outlet_number: str) -> Self
```
Filter by outlet number.

```python
in_city(city_name: str) -> Self
```
Filter by outlet city name.

```python
in_county(county_code: str) -> Self
```
Filter by county code.

```python
issued_after(date: str) -> Self
```
Filter permits issued after a specific date (format: YYYY-MM-DD).

```python
between_dates(start_date: str, end_date: str) -> Self
```
Filter permits issued between two dates.

```python
sort_by(field: str, desc: bool = False) -> Self
```
Sort results by field name.

```python
limit(n: int) -> Self
```
Limit number of results.

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[ActivePermitData]
```
Execute query and return results.

**Example:**
```python
permits = (client.sales_tax()
    .active_permits()
    .for_taxpayer("12345678")
    .in_city("Austin")
    .limit(10)
    .get())
```

### SalesTaxRates

Query sales tax rate changes.

**Socrata Dataset ID:** `tmhs-ahbh`

#### Filter Methods

```python
in_city(city: str) -> Self
```
Filter by city name.

```python
in_county(county: str) -> Self
```
Filter by county name.

```python
limit(n: int) -> Self
```
Limit number of results.

```python
sort_by(field: str, desc: bool = False) -> Self
```
Sort results by field name.

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[SalesTaxRateData]
```
Execute query and return results.

### PermittedLocations

Query permitted location details.

**Socrata Dataset ID:** `3kx8-uryv`

#### Filter Methods

```python
for_taxpayer(taxpayer_number: str) -> Self
```
Filter by taxpayer number.

```python
in_city(city: str) -> Self
```
Filter by city name.

```python
in_county(county: str) -> Self
```
Filter by county name.

```python
in_zip(zip_code: str) -> Self
```
Filter by ZIP code.

```python
limit(n: int) -> Self
```
Limit number of results.

```python
sort_by(field: str, desc: bool = False) -> Self
```
Sort results by field name.

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[PermittedLocationData]
```
Execute query and return results.

### DirectPayTaxpayers

Query direct pay taxpayer list.

**Socrata Dataset ID:** `deed-e7u6`

#### Filter Methods

```python
for_taxpayer(taxpayer_number: str) -> Self
```
Filter by taxpayer number.

```python
limit(n: int) -> Self
```
Limit number of results.

```python
sort_by(field: str, desc: bool = False) -> Self
```
Sort results by field name.

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[DirectPayTaxpayerData]
```
Execute query and return results.

### SalesTaxAllocationHistory

Query historical sales tax allocation data (web scraping).

#### Filter Methods

```python
for_city(city_name: str) -> Self
```
Set city name for allocation history query.

```python
for_county(county_name: str) -> Self
```
Set county name for allocation history query.

```python
for_transit_authority(name: str) -> Self
```
Set transit authority name.

```python
for_special_district(name: str) -> Self
```
Set special district name.

#### Execution

```python
get() -> List[AllocationHistoryData]
```
Execute query and return results.

**Example:**
```python
history = (client.sales_tax()
    .allocation_history()
    .for_city("Austin")
    .get())
```

### QuarterlySalesHistory

Query quarterly sales history data by jurisdiction and industry (web scraping).

#### Filter Methods

```python
for_city(city_name: str) -> Self
```
Filter by city name.

```python
for_county(county_name: str) -> Self
```
Filter by county name.

```python
for_industry(industry_name: str) -> Self
```
Filter by industry name.

```python
for_msa(msa_name: str) -> Self
```
Filter by Metropolitan Statistical Area name.

#### Execution

```python
get() -> List[QuarterlySalesHistoryData]
```
Execute query and return results.

### MarketplaceProvider

Query marketplace provider registry (CSV download).

**Data Source:** CSV file from assets.comptroller.texas.gov

#### Execution

```python
get() -> List[MarketplaceProviderData]
```
Download and parse marketplace provider CSV.

**Note:** This data source does not support filters. It returns the complete provider list.

### SingleLocalAllocations

Query single local jurisdiction allocations.

**Socrata Dataset ID:** `5yx2-afcg`

#### Filter Methods

```python
for_taxpayer(taxpayer_number: str) -> Self
```
Filter by taxpayer number.

```python
limit(n: int) -> Self
```
Limit number of results.

```python
sort_by(field: str, desc: bool = False) -> Self
```
Sort results by field name.

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[SingleLocalAllocationData]
```
Execute query and return results.

### MarketplaceProviderAllocations

Query marketplace provider allocations.

**Socrata Dataset ID:** `hezn-fbgw`

#### Filter Methods

```python
for_provider(provider_name: str) -> Self
```
Filter by provider name.

```python
limit(n: int) -> Self
```
Limit number of results.

```python
sort_by(field: str, desc: bool = False) -> Self
```
Sort results by field name.

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[MarketplaceProviderAllocationData]
```
Execute query and return results.

### LocalAllocationPaymentDetail

Query detailed payment breakdown data.

**Socrata Dataset ID:** `qwe5-t7ba`

#### Filter Methods

```python
in_city(city: str) -> Self
```
Filter by city name.

```python
in_county(county: str) -> Self
```
Filter by county name.

```python
limit(n: int) -> Self
```
Limit number of results.

```python
sort_by(field: str, desc: bool = False) -> Self
```
Sort results by field name.

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[LocalAllocationPaymentDetailsData]
```
Execute query and return results.

### CityCountyComparisonSummary

Query city/county payment comparison data.

**Socrata Dataset ID:** `7p3s-vkws`

#### Filter Methods

```python
in_city(city: str) -> Self
```
Filter by city name.

```python
in_county(county: str) -> Self
```
Filter by county name.

```python
limit(n: int) -> Self
```
Limit number of results.

```python
sort_by(field: str, desc: bool = False) -> Self
```
Sort results by field name.

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[ComparisonSummaryData]
```
Execute query and return results.

### CountySPDMTAAllocations

Query county/special district/MTA allocation data.

**Socrata Dataset ID:** `5cyp-j5c2`

#### Filter Methods

```python
in_county(county: str) -> Self
```
Filter by county name.

```python
limit(n: int) -> Self
```
Limit number of results.

```python
sort_by(field: str, desc: bool = False) -> Self
```
Sort results by field name.

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[CountySPDMTAAllocationData]
```
Execute query and return results.

### SingleLocalTaxRates

Query single local tax rate data.

**Note:** Internal data source, does not use Socrata API.

#### Filter Methods

```python
limit(n: int) -> Self
```
Limit number of results.

```python
sort_by(field: str, desc: bool = False) -> Self
```
Sort results by field name.

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[SingleLocalTaxRateData]
```
Execute query and return results.

## Franchise Tax Data Sources

### ActiveFranchiseTaxPermitHolders

Query active franchise tax permit holders.

**Socrata Dataset ID:** `9cir-efmm`

#### Filter Methods

```python
for_taxpayer(taxpayer_number: str) -> Self
```
Filter by taxpayer number.

```python
limit(n: int) -> Self
```
Limit number of results.

```python
sort_by(field: str, desc: bool = False) -> Self
```
Sort results by field name.

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[FranchiseTaxPermitHolderData]
```
Execute query and return results.

**Example:**
```python
holders = (client.franchise_tax()
    .active_permit_holders()
    .for_taxpayer("12345678")
    .get())
```

## Mixed Beverage Tax Data Sources

### MixedBeverageGrossReceipts

Query mixed beverage gross receipts by beverage type.

**Socrata Dataset ID:** `naix-2893`

#### Filter Methods

```python
for_taxpayer(taxpayer_number: str) -> Self
```
Filter by taxpayer number.

```python
for_year(year: int) -> Self
```
Filter by year.

```python
limit(n: int) -> Self
```
Limit number of results.

```python
sort_by(field: str, desc: bool = False) -> Self
```
Sort results by field name.

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[MixedBeverageGrossReceiptsData]
```
Execute query and return results.

**Example:**
```python
receipts = (client.mixed_beverage_tax()
    .gross_receipts()
    .for_year(2024)
    .limit(100)
    .get())
```

### MixedBeverageHistory

Query historical mixed beverage allocation data (web scraping).

#### Filter Methods

```python
for_city(city_name: str) -> Self
```
Set city name for allocation history query.

```python
for_county(county_name: str) -> Self
```
Set county name for allocation history query.

```python
for_special_district(name: str) -> Self
```
Set special district name.

#### Execution

```python
get() -> List[MixedBeverageHistoryData]
```
Execute query and return results.

## Response Models

All response models are Python dataclasses with type hints.

### Sales Tax Models

#### ActivePermitData

Fields:
- `taxpayer_number: str`
- `taxpayer_name: str`
- `taxpayer_address: Optional[str]`
- `taxpayer_city: Optional[str]`
- `taxpayer_state: Optional[str]`
- `taxpayer_zip: Optional[str]`
- `taxpayer_county: Optional[str]`
- `outlet_number: str`
- `outlet_name: str`
- `outlet_address: Optional[str]`
- `outlet_city: Optional[str]`
- `outlet_state: Optional[str]`
- `outlet_zip: Optional[str]`
- `outlet_county: Optional[str]`
- `issue_date: Optional[date]`
- `permit_status: Optional[str]`

#### SalesTaxRateData

Fields:
- `county: Optional[str]`
- `city: Optional[str]`
- `local_rate: Optional[float]`
- `state_rate: Optional[float]`
- `combined_rate: Optional[float]`
- `effective_date: Optional[date]`
- `expiration_date: Optional[date]`

#### PermittedLocationData

Comprehensive location data (31 fields including jurisdiction codes, tax rates, addresses).

#### DirectPayTaxpayerData

Fields:
- `taxpayer_number: str`
- `taxpayer_name: str`
- `effective_date: Optional[date]`

#### SingleLocalAllocationData

Fields for year-over-year payment comparisons.

#### LocalAllocationPaymentDetailsData

Detailed payment breakdown fields.

#### MarketplaceProviderAllocationData

Marketplace provider allocation fields.

#### MarketplaceProviderData

Provider registration information.

#### AllocationHistoryData

Fields:
- `jurisdiction: str`
- `period: str`
- `current_payment: Optional[float]`
- `prior_payment: Optional[float]`
- `collections: Optional[float]`

#### ComparisonSummaryData

City/county payment comparison fields.

#### CountySPDMTAAllocationData

Multi-jurisdiction allocation fields.

#### QuarterlySalesHistoryData

Quarterly sales by industry/jurisdiction fields.

#### SingleLocalTaxRateData

Tax rate validity period fields.

### Franchise Tax Models

#### FranchiseTaxPermitHolderData

Fields (19 total) including:
- `taxpayer_number: str`
- `taxpayer_name: str`
- `taxpayer_address: Optional[str]`
- `taxpayer_city: Optional[str]`
- `taxpayer_state: Optional[str]`
- `taxpayer_zip: Optional[str]`
- `entity_type: Optional[str]`
- `state_of_formation: Optional[str]`
- `exemption_type: Optional[str]`
- And more...

### Mixed Beverage Tax Models

#### MixedBeverageGrossReceiptsData

Fields for gross receipts by beverage type.

#### MixedBeverageHistoryData

Fields:
- `jurisdiction: str`
- `period: str`
- `current_payment: Optional[float]`
- `prior_payment: Optional[float]`
- `collections: Optional[float]`

### Factory Methods

All response models include:

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> Self
```

Creates an instance from a dictionary (typically from JSON response).

Some models also include:

```python
@classmethod
def from_row(cls, cells: List) -> Self
```

Creates an instance from an HTML table row (for web-scraped data).

## Exceptions

### TexasComptrollerError

Base exception class for all Compytroller errors.

```python
class TexasComptrollerError(Exception):
    pass
```

### HttpError

Raised when HTTP requests fail.

```python
class HttpError(TexasComptrollerError):
    def __init__(self, message: str, status_code: Optional[int] = None, url: Optional[str] = None)
```

**Attributes:**
- `status_code: Optional[int]` - HTTP status code
- `url: Optional[str]` - Request URL that failed

**Factory Method:**
```python
@classmethod
def from_httpx_exception(cls, exc: httpx.HTTPError) -> HttpError
```

### InvalidRequest

Raised when request validation fails.

```python
class InvalidRequest(TexasComptrollerError):
    pass
```

**Example:**
```python
from data.exceptions import HttpError, InvalidRequest

try:
    results = client.sales_tax().rates().get()
except HttpError as e:
    print(f"HTTP Error {e.status_code} at {e.url}: {e}")
except InvalidRequest as e:
    print(f"Invalid request: {e}")
```

## Utilities

### Date Parsing

```python
parse_date(x: str) -> Optional[date]
```

Parses date strings in various formats.

**Supported Formats:**
- `YYYY-MM-DD`
- `YYYY-MM-DDTHH:MM:SS.fff`

**Parameters:**
- `x` (str): Date string to parse

**Returns:**
- `date`: Parsed date object, or `None` if parsing fails

### Float Parsing

```python
parse_float(val: Any) -> Optional[float]
```

Safely parses float values from various input types.

**Handles:**
- String numbers with commas
- Numeric types
- NaN and Infinity values
- Empty/null values

**Parameters:**
- `val` (Any): Value to parse

**Returns:**
- `float`: Parsed float, or `None` if parsing fails or value is NaN/Inf

### Integer Parsing

```python
parse_int(x: str) -> Optional[int]
```

Safely parses integer values from strings.

**Handles:**
- Strings with commas
- Float-formatted strings
- NaN and Infinity values
- Empty/null values

**Parameters:**
- `x` (str): String to parse

**Returns:**
- `int`: Parsed integer, or `None` if parsing fails

## SocrataClient (Advanced)

Low-level HTTP client for Socrata Open Data API.

### Constructor

```python
SocrataClient(app_token: str)
```

**Parameters:**
- `app_token` (str): Socrata application token

### Methods

```python
get(dataset_id: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]
```

Execute a GET request against a Socrata dataset.

**Parameters:**
- `dataset_id` (str): Socrata dataset identifier (e.g., "jrea-zgmq")
- `params` (dict, optional): Query parameters

**Returns:**
- `List[Dict]`: Parsed JSON response

**Raises:**
- `HttpError`: On HTTP failures

**Example:**
```python
from data.socrata import SocrataClient

client = SocrataClient("your-app-token")
data = client.get("jrea-zgmq", {"$limit": 10})
```
