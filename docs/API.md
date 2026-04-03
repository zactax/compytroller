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

#### Constructor

```python
ComptrollerClient(app_token: str, base_url: str = "https://data.texas.gov/resource")
```

Creates a new client instance with the provided Socrata app token.

**Parameters:**
- `app_token` (str): Your Socrata application token from data.texas.gov
- `base_url` (str, optional): Base URL for the Socrata API. Defaults to Texas data portal.

**Returns:**
- `ComptrollerClient`: Configured client instance

**Example:**
```python
from data import ComptrollerClient

client = ComptrollerClient(app_token="your-app-token")
```

#### Factory Method

```python
ComptrollerClient.factory(app_token: str) -> ComptrollerClient
```

Alternative factory method to create a client instance.

**Example:**
```python
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
- `local_allocation_payment_details() -> LocalAllocationPaymentDetail`
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

## Field Enums

Optional enums for `sort_by()` fields and categorical filter values. All enums inherit from `str` and can be used anywhere a raw string is accepted.

```python
from data.fields import ActivePermitField, AuthorityType, RightToTransactCode
```

### Sort Field Enums

| Enum | Resource | Members |
|------|----------|---------|
| `ActivePermitField` | `active_permits()` | `TAXPAYER_NUMBER`, `OUTLET_CITY`, `OUTLET_COUNTY_CODE`, `OUTLET_NAICS_CODE`, etc. |
| `AllocationPaymentDetailField` | `local_allocation_payment_details()` | `AUTHORITY_ID`, `TOTAL_COLLECTIONS`, `NET_PAYMENT`, etc. |
| `ComparisonSummaryField` | `city_county_comparison_summary()` | `CITY`, `COUNTY`, `NET_PAYMENT_THIS_PERIOD`, `YEAR_PERCENT_CHANGE`, etc. |
| `CountySPDMTAAllocationField` | `county_spd_mta_allocations()` | `NAME`, `JURISDICTION_TYPE`, `NET_PAYMENT_THIS_PERIOD`, etc. |
| `DirectPayTaxpayerField` | `direct_pay_taxpayers()` | `ID`, `NAME`, `COUNTY`, `NAICS_CODE`, etc. |
| `MarketplaceProviderAllocationField` | `marketplace_provider_allocations()` | `AUTHORITY_TYPE`, `AUTHORITY_NAME`, `AMOUNT_ALLOCATED`, etc. |
| `PermittedLocationField` | `permitted_locations()` | `OUTLET_CITY`, `OUTLET_COUNTY`, `OUTLET_NAICS_CODE`, etc. |
| `SalesTaxRateField` | `rates()` | `CITY_NAME`, `COUNTY_NAME`, `NEW_RATE`, `EFFECTIVE_DATE`, etc. |
| `SingleLocalAllocationField` | `single_local_allocations()` | `AUTHORITY_NAME`, `CURRENT_NET_PAYMENT`, `PRIOR_NET_PAYMENT`, etc. |
| `FranchiseTaxPermitHolderField` | `active_permit_holders()` | `TAXPAYER_NAME`, `TAXPAYER_CITY`, `NAICS_CODE`, `RIGHT_TO_TRANSACT_BUSINESS_CODE`, etc. |
| `MixedBeverageGrossReceiptsField` | `gross_receipts()` | `LOCATION_NAME`, `LOCATION_CITY`, `TOTAL_RECEIPTS`, `LIQUOR_RECEIPTS`, etc. |

### Categorical Enums

| Enum | Used with | Values |
|------|-----------|--------|
| `AuthorityType` | `county_spd_mta_allocations().for_type()` | `CITY`, `COUNTY`, `SPD`, `MTA`, `TRANSIT` |
| `SalesTaxRateType` | `rates().for_type()` | `CITY_LIST`, `SPD_LIST` |
| `RightToTransactCode` | `active_permit_holders().with_right_to_transact()` | `ACTIVE`, `ELIGIBLE_FOR_TERMINATION`, `FORFEITED`, `INVOLUNTARILY_ENDED`, `NOT_ESTABLISHED` |

**Example:**

```python
from data.fields import ActivePermitField, RightToTransactCode

# Use enum for sort_by
permits = (client.sales_tax()
    .active_permits()
    .sort_by(ActivePermitField.OUTLET_CITY, desc=True)
    .limit(100)
    .get())

# Use enum for categorical filter
holders = (client.franchise_tax()
    .active_permit_holders()
    .with_right_to_transact(RightToTransactCode.ACTIVE)
    .limit(50)
    .get())
```

## Sales Tax Data Sources

### ActivePermits

Query active sales tax permits.

**Socrata Dataset ID:** `jrea-zgmq`

#### Filter Methods

```python
for_taxpayer(number: str) -> Self
```
Filter by taxpayer number.

```python
for_city(city: str) -> Self
```
Filter by outlet city name.

```python
in_county(county_code: str) -> Self
```
Filter by county code.

```python
with_naics(code: str) -> Self
```
Filter by NAICS industry code.

```python
issued_after(date: str) -> Self
```
Filter permits issued after a specific date (format: YYYY-MM-DD).

```python
first_sale_after(date: str) -> Self
```
Filter permits where first sale occurred after a specific date.

```python
between_issue_dates(start: str, end: str) -> Self
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
    .for_city("Austin")
    .with_naics("722511")
    .limit(10)
    .get())
```

### SalesTaxRates

Query sales tax rate changes.

**Socrata Dataset ID:** `tmhs-ahbh`

#### Filter Methods

```python
for_city(city: str) -> Self
```
Filter by city name.

```python
in_county(county: str) -> Self
```
Filter by county name.

```python
for_type(jurisdiction_type: str) -> Self
```
Filter by jurisdiction type (e.g., "SPD List", "City List").

```python
for_year(year: int) -> Self
```
Filter by report year.

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
get() -> List[SalesTaxRateData]
```
Execute query and return results.

### PermittedLocations

Query permitted location details.

**Socrata Dataset ID:** `3kx8-uryv`

#### Filter Methods

```python
with_tp_number(tp_number: str) -> Self
```
Filter by taxpayer number.

```python
for_city(city: str) -> Self
```
Filter by city name.

```python
with_naics(code: str) -> Self
```
Filter by NAICS industry code.

```python
with_city_taid(taid: str) -> Self
```
Filter by city taxing authority ID.

```python
with_county_taid(taid: str) -> Self
```
Filter by county taxing authority ID.

```python
with_mta_taid(taid: str, slot: int = 1) -> Self
```
Filter by mass transit authority TAID. Slot must be 1 or 2.

```python
with_spd_taid(taid: str, slot: int = 1) -> Self
```
Filter by special purpose district TAID. Slot must be 1, 2, 3, or 4.

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
get() -> List[PermittedLocationData]
```
Execute query and return results.

### DirectPayTaxpayers

Query direct pay taxpayer list.

**Socrata Dataset ID:** `deed-e7u6`

#### Filter Methods

```python
with_naics(code: str) -> Self
```
Filter by NAICS industry code.

```python
in_county(county: str) -> Self
```
Filter by county name.

```python
for_city(city: str) -> Self
```
Filter by city name.

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
get() -> List[DirectPayTaxpayerData]
```
Execute query and return results.

### SalesTaxAllocationHistory

Query historical sales tax allocation data (web scraping).

#### Filter Methods

```python
for_city(name: str) -> Self
```
Set city name for allocation history query.

```python
in_county(name: str) -> Self
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

```python
statewide(statewide_type: str) -> Self
```
Query statewide allocation data by category.

```python
reset() -> Self
```
Clear all filters.

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
summary_report(summary_type: str = "In-State") -> Self
```
Configure for statewide summary report.

```python
report_by_ccma(ccm_option: str, jurisdiction_name: str) -> Self
```
Configure for city, county, or MSA-specific report.
- `ccm_option`: "City", "County", or "MSA"
- `jurisdiction_name`: Name of the city, county, or MSA

```python
with_summary_type(summary_type: str) -> Self
```
Set the summary type for summary reports (e.g., "In-State", "Out-of-State").

```python
with_industry(label: str) -> Self
```
Filter by industry sector (e.g., "Retail Trade", "All Industries").

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[QuarterlySalesHistoryData]
```
Execute query and return results.

**Example:**
```python
quarterly = (client.sales_tax()
    .quarterly_sales_history()
    .report_by_ccma("City", "Austin")
    .with_industry("Retail Trade")
    .get())
```

### MarketplaceProvider

Query marketplace provider registry (CSV download).

**Data Source:** CSV file from assets.comptroller.texas.gov

#### Filter Methods

```python
after_date(cutoff_date: Union[str, date]) -> Self
```
Filter providers whose registration began after a specific date.

```python
before_date(cutoff_date: Union[str, date]) -> Self
```
Filter providers whose registration ended before a specific date.

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[MarketplaceProviderData]
```
Download and parse marketplace provider CSV with optional date filters.

**Example:**
```python
providers = (client.sales_tax()
    .marketplace_provider()
    .after_date("2023-01-01")
    .get())
```

### SingleLocalAllocations

Query single local jurisdiction allocations.

**Socrata Dataset ID:** `5yx2-afcg`

#### Filter Methods

```python
for_city(city: str) -> Self
```
Filter allocations for a specific city.

```python
in_county(county: str) -> Self
```
Filter allocations for a specific county.

```python
for_spd(spd_name: str) -> Self
```
Filter allocations for a special purpose district.

```python
for_mta(mta_name: str) -> Self
```
Filter allocations for a mass transit authority.

```python
for_year(year: int) -> Self
```
Filter by reporting year.

```python
for_month(month: int) -> Self
```
Filter by reporting month (1-12).

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
get() -> List[SingleLocalAllocationData]
```
Execute query and return results.

```python
get_all() -> List[SingleLocalAllocationData]
```
Retrieve all records without filtering (use with caution).

### MarketplaceProviderAllocations

Query marketplace provider allocations.

**Socrata Dataset ID:** `hezn-fbgw`

#### Filter Methods

```python
for_authority(name: str) -> Self
```
Filter by authority name (searches both original and uppercase).

```python
for_type(authority_type: str) -> Self
```
Filter by authority type (e.g., "CITY", "COUNTY", "SPD", "TRANSIT").

```python
for_year(year: int) -> Self
```
Filter by allocation year.

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
get() -> List[MarketplaceProviderAllocationData]
```
Execute query and return results.

### LocalAllocationPaymentDetail

Query detailed payment breakdown data.

**Socrata Dataset ID:** `3p4v-vsr3`

#### Filter Methods

```python
for_city(city: str) -> Self
```
Filter by city name.

```python
with_authority_id(authority_id: str) -> Self
```
Filter by authority ID.

```python
for_month(month: str) -> Self
```
Filter by allocation month (floating timestamp format).

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
get() -> List[LocalAllocationPaymentDetailsData]
```
Execute query and return results.

### CityCountyComparisonSummary

Query city/county payment comparison data.

**Socrata Dataset ID:** `53pa-m7sm`

#### Filter Methods

```python
for_city(name: str) -> Self
```
Filter by city name.

```python
in_county(name: str) -> Self
```
Filter by county name.

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
get() -> List[ComparisonSummaryData]
```
Execute query and return results.

### CountySPDMTAAllocations

Query county/special district/MTA allocation data.

**Socrata Dataset ID:** `qsh8-tby8`

#### Filter Methods

```python
for_type(type_name: str) -> Self
```
Filter by jurisdiction type (e.g., "County", "SPD", "MTA").

```python
with_name(name: str) -> Self
```
Filter by jurisdiction name.

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
get() -> List[CountySPDMTAAllocationData]
```
Execute query and return results.

**Example:**
```python
allocations = (client.sales_tax()
    .county_spd_mta_allocations()
    .for_type("County")
    .with_name("Travis")
    .limit(20)
    .get())
```

### SingleLocalTaxRates

Query single local tax rate data (CSV download).

**Data Source:** CSV file from assets.comptroller.texas.gov

#### Execution Methods

```python
get_all() -> List[SingleLocalTaxRateData]
```
Download and parse all single local tax rate records.

```python
get_after_date(cutoff_date: Union[str, date]) -> List[SingleLocalTaxRateData]
```
Get taxpayers whose registration began after a specific date.

```python
get_before_date(cutoff_date: Union[str, date]) -> List[SingleLocalTaxRateData]
```
Get taxpayers whose registration ended before a specific date.

**Example:**
```python
rates = (client.sales_tax()
    .single_local_tax_rates()
    .get_after_date("2023-01-01"))
```

## Franchise Tax Data Sources

### ActiveFranchiseTaxPermitHolders

Query active franchise tax permit holders.

**Socrata Dataset ID:** `9cir-efmm`

#### Filter Methods

```python
for_taxpayer(number: str) -> Self
```
Filter by taxpayer number.

```python
for_city(city: str) -> Self
```
Filter by city name.

```python
for_org_type(org_type: str) -> Self
```
Filter by organizational type code (e.g., "CT" for Texas Profit Corporation, "CL" for Texas LLC).

```python
with_right_to_transact(status: str) -> Self
```
Filter by right to transact business status code:
- `A` = Active
- `D` = Active - Eligible for Termination/Withdrawal
- `N` = Forfeited
- `I` = Franchise Tax Involuntarily Ended
- `U` = Franchise Tax Not Established

```python
with_exempt_reason(reason: str) -> Self
```
Filter by exemption reason code (e.g., "00" = Not Exempt, "19" = 501(c)(3) Nonprofit).

```python
responsibility_start_before(date: str) -> Self
```
Filter permit holders whose responsibility began before a specific date.

```python
responsibility_start_after(date: str) -> Self
```
Filter permit holders whose responsibility began after a specific date.

```python
responsibility_start_between(start: str, end: str) -> Self
```
Filter permit holders whose responsibility began within a date range.

```python
exempt_start_before(date: str) -> Self
```
Filter permit holders whose exemption began before a specific date.

```python
exempt_start_after(date: str) -> Self
```
Filter permit holders whose exemption began after a specific date.

```python
exempt_start_between(start: str, end: str) -> Self
```
Filter permit holders whose exemption began within a date range.

```python
for_naics_code(naics_code: str) -> Self
```
Filter by NAICS industry code.

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
get() -> List[FranchiseTaxPermitHolderData]
```
Execute query and return results.

**Example:**
```python
holders = (client.franchise_tax()
    .active_permit_holders()
    .for_city("Austin")
    .for_org_type("CL")
    .with_right_to_transact("A")
    .limit(50)
    .get())
```

## Mixed Beverage Tax Data Sources

### MixedBeverageGrossReceipts

Query mixed beverage gross receipts by beverage type.

**Socrata Dataset ID:** `naix-2893`

#### Filter Methods

```python
for_taxpayer(number: str) -> Self
```
Filter by taxpayer number.

```python
taxpayer_for_city(city: str) -> Self
```
Filter by taxpayer's city.

```python
for_location(name: str) -> Self
```
Filter by location name.

```python
location_for_city(city: str) -> Self
```
Filter by location city.

```python
location_inside_city_limits(inside: bool = True) -> Self
```
Filter by whether location is inside city limits.

```python
with_location_number(location_number: str) -> Self
```
Filter by location number.

```python
with_tabc_permit(tabc_permit: str) -> Self
```
Filter by TABC permit number.

```python
responsibility_start_after(date: str) -> Self
```
Filter where responsibility began after a specific date.

```python
responsibility_start_before(date: str) -> Self
```
Filter where responsibility began before a specific date.

```python
responsibility_between_dates(start: str, end: str) -> Self
```
Filter where responsibility began within a date range.

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
get() -> List[MixedBeverageGrossReceiptsData]
```
Execute query and return results.

**Example:**
```python
receipts = (client.mixed_beverage_tax()
    .gross_receipts()
    .location_for_city("Austin")
    .limit(100)
    .get())
```

### MixedBeverageHistory

Query historical mixed beverage allocation data (web scraping).

#### Filter Methods

```python
for_city(name: str) -> Self
```
Set city name for allocation history query.

```python
in_county(name: str) -> Self
```
Set county name for allocation history query.

```python
for_special_district(name: str) -> Self
```
Set special district name.

```python
with_summary_type(summary_type: str) -> Self
```
Set the summary type (e.g., "Total Taxes", "Gross Receipts", "Sales Tax").

```python
statewide_summary(summary_scope: str, summary_type: str) -> Self
```
Query statewide mixed beverage allocation summary.
- `summary_scope`: "State Revenue", "All Counties", "All Cities", "All SPDs"
- `summary_type`: "Total Taxes", "Gross Receipts", "Sales Tax"

```python
reset() -> Self
```
Clear all filters.

#### Execution

```python
get() -> List[MixedBeverageHistoryData]
```
Execute query and return results.

**Example:**
```python
history = (client.mixed_beverage_tax()
    .history()
    .for_city("Austin")
    .with_summary_type("Total Taxes")
    .get())
```

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
SocrataClient(app_token: str, base_url: str = "https://data.texas.gov/resource")
```

**Parameters:**
- `app_token` (str): Socrata application token
- `base_url` (str): Base URL for the Socrata API

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
