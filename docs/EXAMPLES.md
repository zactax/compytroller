# Usage Examples

Common usage patterns and examples for Compytroller.

## Table of Contents

- [Getting Started](#getting-started)
- [Sales Tax Examples](#sales-tax-examples)
- [Franchise Tax Examples](#franchise-tax-examples)
- [Mixed Beverage Tax Examples](#mixed-beverage-tax-examples)
- [Advanced Queries](#advanced-queries)
- [Error Handling](#error-handling)
- [Data Processing](#data-processing)

## Getting Started

### Initialize the Client

```python
from data import ComptrollerClient

# Get your app token from https://data.texas.gov/profile/app_tokens
client = ComptrollerClient.factory(app_token="your-app-token-here")
```

### Basic Query

```python
# Get all sales tax rates (limited to 100 results)
rates = client.sales_tax().rates().limit(100).get()

for rate in rates:
    print(f"{rate.city}: {rate.combined_rate}%")
```

## Sales Tax Examples

### Active Permits

#### Find All Permits for a Taxpayer

```python
permits = (client.sales_tax()
    .active_permits()
    .for_taxpayer("12345678")
    .get())

for permit in permits:
    print(f"Outlet: {permit.outlet_name}")
    print(f"Address: {permit.outlet_address}, {permit.outlet_city}")
    print(f"First Sale Date: {permit.outlet_first_sales_date}")
    print("---")
```

#### Find Permits in a Specific City

```python
austin_permits = (client.sales_tax()
    .active_permits()
    .for_city("Austin")
    .limit(50)
    .get())
```

#### Find Recent Permits

```python
from datetime import datetime, timedelta

# Permits issued in the last 30 days
thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

recent_permits = (client.sales_tax()
    .active_permits()
    .issued_after(thirty_days_ago)
    .sort_by("issue_date", desc=True)
    .get())
```

#### Complex Multi-Filter Query

```python
permits = (client.sales_tax()
    .active_permits()
    .for_city("Houston")
    .in_county("201")  # Harris County
    .issued_after("2024-01-01")
    .sort_by("outlet_city", desc=False)
    .limit(100)
    .get())
```

### Sales Tax Rates

#### Get Rates for a City

```python
rates = (client.sales_tax()
    .rates()
    .for_city("Dallas")
    .get())

for rate in rates:
    print(f"Effective: {rate.effective_date}")
    print(f"Old Rate: {rate.old_rate}%")
    print(f"New Rate: {rate.new_rate}%")
```

#### Compare Rates Across Counties

```python
counties = ["Travis", "Harris", "Dallas", "Bexar"]

for county in counties:
    rates = (client.sales_tax()
        .rates()
        .in_county(county)
        .limit(1)
        .get())

    if rates:
        print(f"{county} County: {rates[0].new_rate}%")
```

### Allocation History

#### Get City Allocation History

```python
history = (client.sales_tax()
    .allocation_history()
    .for_city("Austin")
    .get())

for record in history:
    print(f"{record.allocation_month}: ${record.net_payment:,.2f}")
```

#### Get County Allocation History

```python
history = (client.sales_tax()
    .allocation_history()
    .in_county("Travis")
    .get())

total_collections = sum(h.net_payment or 0 for h in history)
print(f"Total collections: ${total_collections:,.2f}")
```

### Permitted Locations

#### Find All Locations for a Taxpayer

```python
locations = (client.sales_tax()
    .permitted_locations()
    .with_tp_number("12345678")
    .get())

for loc in locations:
    print(f"Location: {loc.outlet_name}")
    print(f"City: {loc.outlet_city}, ZIP: {loc.outlet_zip}")
    print(f"County: {loc.outlet_county}")
```

### Direct Pay Taxpayers

```python
direct_pay = (client.sales_tax()
    .direct_pay_taxpayers()
    .limit(100)
    .get())

for taxpayer in direct_pay:
    print(f"{taxpayer.name} (#{taxpayer.tp_id})")
    print(f"Effective: {taxpayer.responsibility_begin_date}")
```

### Quarterly Sales History

#### Get Sales by City and Industry

```python
sales = (client.sales_tax()
    .report_by_ccma("City", "Austin")
    .with_industry("Retail Trade")
    .get())

for record in sales:
    print(f"Quarter: {record.quarter, record.year}")
    print(f"Sales: ${record.taxable_sales:,.2f}")
```

#### Get MSA Sales Data

```python
sales = (client.sales_tax()
    .quarterly_sales_history()
    .report_by_ccma("MSA","Austin-Round Rock MSA")
    .get())
```

### Marketplace Providers

#### Get All Marketplace Providers

```python
providers = client.sales_tax().marketplace_provider().get()

print(f"Total providers: {len(providers)}")

for provider in providers[:10]:
    print(f"{provider.name}")
    print(f"  Begin Date: {provider.begin_date}")
```

#### Get Marketplace Provider Allocations

```python
allocations = (client.sales_tax()
    .marketplace_provider_allocations()
    .for_authority("Austin")
    .limit(100)
    .get())
```

### Single Local Allocations

```python
allocations = (client.sales_tax()
    .single_local_allocations()
    .sort_by("current_year_payment", desc=True)
    .limit(50)
    .get())

for alloc in allocations:
    print(f"Jurisdiction: {alloc.tax_authority}")
    print(f"Current: ${alloc.current_net_payment:,.2f}")
    print(f"Prior: ${alloc.prior_year_net_payment:,.2f}")
```

### City/County Comparison Summary

```python
comparison = (client.sales_tax()
    .city_county_comparison_summary()
    .for_city("Austin")
    .get())

for comp in comparison:
    print(f"Period: {comp.report_month, comp.report_year}")
    print(f"Payment: ${comp.net_payment_this_period:,.2f}")
    print(f"Period % Change: ${comp.period_percent_change:,.2f}")
```

### County/SPD/MTA Allocations

```python
allocations = (client.sales_tax()
    .county_spd_mta_allocations()
    .for_type("County")
    .with_name("Travis")
    .get())
```

## Franchise Tax Examples

### Active Permit Holders

#### Find a Specific Company

```python
holders = (client.franchise_tax()
    .active_permit_holders()
    .for_taxpayer("12345678")
    .get())

for holder in holders:
    print(f"Name: {holder.taxpayer_name}")
    print(f"Address: {holder.taxpayer_address}")
    print(f"City: {holder.taxpayer_city}, {holder.taxpayer_state}")
```

#### Get Recent Permit Holders

```python
holders = (client.franchise_tax()
    .active_permit_holders()
    .sort_by("responsibility_beginning_date", desc=True)
    .limit(100)
    .get())

for holder in holders[:10]:
    print(f"{holder.taxpayer_name} - Registered: {holder.responsibility_beginning_date}")
```

## Mixed Beverage Tax Examples

### Gross Receipts

#### Get Receipts for a Specific Year

```python
receipts = (client.mixed_beverage_tax()
    .gross_receipts()
    .for_year(2024)
    .limit(100)
    .get())

for receipt in receipts:
    print(f"Taxpayer: {receipt.taxpayer_name}")
    print(f"Total Receipts: ${receipt.total_receipts:,.2f}")
    print(f"Beer: ${receipt.beer_receipts:,.2f}")
    print(f"Liquor: ${receipt.liquor_receipts:,.2f}")
    print(f"Wine: ${receipt.wine_receipts:,.2f}")
```

#### Get Receipts for a Specific Taxpayer

```python
receipts = (client.mixed_beverage_tax()
    .gross_receipts()
    .for_taxpayer("12345678")
    .get())
```

### Allocation History

#### Get City Allocation History

```python
history = (client.mixed_beverage_tax()
    .history()
    .for_city("Austin")
    .get())

for record in history:
    print(f"{record.period}: ${record.current_payment:,.2f}")
```

#### Get County Allocation History

```python
history = (client.mixed_beverage_tax()
    .history()
    .in_county("Travis")
    .get())
```

## Using Field Enums

Field enums provide IDE autocompletion for `sort_by()` fields and categorical filter values. They're optional — raw strings still work.

### Sorting with Field Enums

```python
from data.fields import ActivePermitField, SalesTaxRateField

# Instead of sort_by("outlet_city")
permits = (client.sales_tax()
    .active_permits()
    .sort_by(ActivePermitField.OUTLET_CITY, desc=True)
    .limit(100)
    .get())

# Instead of sort_by("new_rate")
rates = (client.sales_tax()
    .rates()
    .for_city("Austin")
    .sort_by(SalesTaxRateField.NEW_RATE, desc=True)
    .get())
```

### Categorical Filter Enums

```python
from data.fields import AuthorityType, RightToTransactCode, SalesTaxRateType

# Instead of for_type("COUNTY")
allocations = (client.sales_tax()
    .county_spd_mta_allocations()
    .for_type(AuthorityType.COUNTY)
    .with_name("Travis")
    .get())

# Instead of for_type("SPD List")
spd_rates = (client.sales_tax()
    .rates()
    .for_type(SalesTaxRateType.SPD_LIST)
    .get())

# Instead of with_right_to_transact("A")
active_holders = (client.franchise_tax()
    .active_permit_holders()
    .with_right_to_transact(RightToTransactCode.ACTIVE)
    .limit(50)
    .get())
```

## Advanced Queries

### Resetting Filters

```python
query = client.sales_tax().active_permits()

# First query
austin_permits = query.for_city("Austin").limit(10).get()

# Reset and run different query
query.reset()
houston_permits = query.for_city("Houston").limit(10).get()
```

### Sorting Results

```python
# Sort ascending (default)
permits = (client.sales_tax()
    .active_permits()
    .sort_by("outlet_city")
    .limit(100)
    .get())

# Sort descending
permits = (client.sales_tax()
    .active_permits()
    .sort_by("outlet_permit_issue_date", desc=True)
    .limit(100)
    .get())
```

## Error Handling

### Handling HTTP Errors

```python
from data.exceptions import HttpError, InvalidRequest

try:
    rates = client.sales_tax().rates().for_city("Austin").get()
except HttpError as e:
    print(f"HTTP Error occurred:")
    print(f"  Status Code: {e.status_code}")
    print(f"  URL: {e.url}")
    print(f"  Message: {e}")
except InvalidRequest as e:
    print(f"Invalid request: {e}")
```

### Checking for Empty Results

```python
permits = (client.sales_tax()
    .active_permits()
    .for_taxpayer("00000000")
    .get())

if not permits:
    print("No permits found for this taxpayer")
else:
    print(f"Found {len(permits)} permit(s)")
```

### Retry Logic

```python
import time
from data.exceptions import HttpError

def query_with_retry(query_func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return query_func()
        except HttpError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

# Usage
results = query_with_retry(
    lambda: client.sales_tax().rates().for_city("Austin").get()
)
```

## Data Processing

### Converting to Pandas DataFrame

```python
import pandas as pd

permits = (client.sales_tax()
    .active_permits()
    .for_city("Austin")
    .limit(100)
    .get())

# Convert to DataFrame
df = pd.DataFrame([vars(permit) for permit in permits])

# Basic analysis
print(df.describe())
print(df['outlet_city'].value_counts())
```

### Aggregating Results

```python
from collections import defaultdict

permits = (client.sales_tax()
    .active_permits()
    .in_county("227")  # Travis County
    .limit(1000)
    .get())

# Count permits by city
by_city = defaultdict(int)
for permit in permits:
    by_city[permit.outlet_city] += 1

# Sort and display
for city, count in sorted(by_city.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"{city}: {count} permits")
```

### Filtering Results in Memory

```python
permits = (client.sales_tax()
    .active_permits()
    .for_city("Dallas")
    .limit(500)
    .get())

# Filter to only active permits
active = [p for p in permits if p.permit_status == "Active"]

# Filter by address pattern
downtown = [p for p in permits if "Main St" in (p.outlet_address or "")]
```

### Exporting to CSV

```python
import csv

permits = (client.sales_tax()
    .active_permits()
    .for_city("Houston")
    .limit(100)
    .get())

with open('houston_permits.csv', 'w', newline='') as f:
    if permits:
        writer = csv.DictWriter(f, fieldnames=vars(permits[0]).keys())
        writer.writeheader()
        for permit in permits:
            writer.writerow(vars(permit))
```

### Calculating Totals

```python
history = (client.sales_tax()
    .allocation_history()
    .for_city("Austin")
    .get())

# Calculate total allocations
total_payments = sum(h.net_payment or 0 for h in history)

print(f"Total Allocations: ${total_payments:,.2f}")
```

### Combining Multiple Queries

```python
# Get both permits and locations for a taxpayer
taxpayer_number = "12345678"

permits = (client.sales_tax()
    .active_permits()
    .for_taxpayer(taxpayer_number)
    .get())

locations = (client.sales_tax()
    .permitted_locations()
    .for_taxpayer(taxpayer_number)
    .get())

franchise = (client.franchise_tax()
    .active_permit_holders()
    .for_taxpayer(taxpayer_number)
    .get())

print(f"Taxpayer {taxpayer_number}:")
print(f"  Sales Tax Permits: {len(permits)}")
print(f"  Permitted Locations: {len(locations)}")
print(f"  Franchise Tax Status: {'Active' if franchise else 'None'}")
```

### Date Range Queries

```python
from datetime import datetime, timedelta

# Last 90 days
end_date = datetime.now()
start_date = end_date - timedelta(days=90)

permits = (client.sales_tax()
    .active_permits()
    .between_dates(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
    .get())

print(f"Permits issued in last 90 days: {len(permits)}")
```

## Performance Tips

### Limit Results for Exploration

```python
# Use limit() when exploring data
sample = client.sales_tax().rates().limit(10).get()
```

### Use Specific Filters

```python
# More efficient - uses API filtering
permits = (client.sales_tax()
    .active_permits()
    .for_city("Austin")
    .get())

# Less efficient - fetches all, filters in memory
all_permits = client.sales_tax().active_permits().get()
austin = [p for p in all_permits if p.outlet_city == "Austin"]
```

### Cache Results

```python
# Cache expensive queries
_cache = {}

def get_city_rates(city):
    if city not in _cache:
        _cache[city] = (client.sales_tax()
            .rates()
            .for_city(city)
            .get())
    return _cache[city]
```
