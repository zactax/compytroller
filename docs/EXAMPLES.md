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
    print(f"Status: {permit.permit_status}")
    print("---")
```

#### Find Permits in a Specific City

```python
austin_permits = (client.sales_tax()
    .active_permits()
    .in_city("Austin")
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
    .in_city("Houston")
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
    .in_city("Dallas")
    .get())

for rate in rates:
    print(f"Effective: {rate.effective_date}")
    print(f"State: {rate.state_rate}%")
    print(f"Local: {rate.local_rate}%")
    print(f"Combined: {rate.combined_rate}%")
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
        print(f"{county} County: {rates[0].combined_rate}%")
```

### Allocation History

#### Get City Allocation History

```python
history = (client.sales_tax()
    .allocation_history()
    .for_city("Austin")
    .get())

for record in history:
    print(f"{record.period}: ${record.current_payment:,.2f}")
    if record.prior_payment:
        change = ((record.current_payment - record.prior_payment) / record.prior_payment) * 100
        print(f"  Change: {change:+.2f}%")
```

#### Get County Allocation History

```python
history = (client.sales_tax()
    .allocation_history()
    .for_county("Travis")
    .get())

total_collections = sum(h.collections or 0 for h in history)
print(f"Total collections: ${total_collections:,.2f}")
```

### Permitted Locations

#### Find All Locations for a Taxpayer

```python
locations = (client.sales_tax()
    .permitted_locations()
    .for_taxpayer("12345678")
    .get())

for loc in locations:
    print(f"Location: {loc.outlet_name}")
    print(f"City: {loc.outlet_city}, ZIP: {loc.outlet_zip}")
    print(f"County: {loc.outlet_county}")
```

#### Find Locations by ZIP Code

```python
locations = (client.sales_tax()
    .permitted_locations()
    .in_zip("78701")
    .limit(25)
    .get())
```

### Direct Pay Taxpayers

```python
direct_pay = (client.sales_tax()
    .direct_pay_taxpayers()
    .limit(100)
    .get())

for taxpayer in direct_pay:
    print(f"{taxpayer.taxpayer_name} (#{taxpayer.taxpayer_number})")
    print(f"Effective: {taxpayer.effective_date}")
```

### Quarterly Sales History

#### Get Sales by City and Industry

```python
sales = (client.sales_tax()
    .quarterly_sales_history()
    .for_city("Austin")
    .for_industry("Retail Trade")
    .get())

for record in sales:
    print(f"Quarter: {record.period}")
    print(f"Sales: ${record.taxable_sales:,.2f}")
```

#### Get MSA Sales Data

```python
sales = (client.sales_tax()
    .quarterly_sales_history()
    .for_msa("Austin-Round Rock")
    .get())
```

### Marketplace Providers

#### Get All Marketplace Providers

```python
providers = client.sales_tax().marketplace_provider().get()

print(f"Total providers: {len(providers)}")

for provider in providers[:10]:
    print(f"{provider.provider_name}")
    print(f"  Registered: {provider.registration_date}")
```

#### Get Marketplace Provider Allocations

```python
allocations = (client.sales_tax()
    .marketplace_provider_allocations()
    .for_provider("Amazon")
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
    print(f"Jurisdiction: {alloc.jurisdiction_name}")
    print(f"Current: ${alloc.current_year_payment:,.2f}")
    print(f"Prior: ${alloc.prior_year_payment:,.2f}")
```

### City/County Comparison Summary

```python
comparison = (client.sales_tax()
    .city_county_comparison_summary()
    .in_city("Austin")
    .get())

for comp in comparison:
    print(f"Period: {comp.period}")
    print(f"City payment: ${comp.city_payment:,.2f}")
    print(f"County payment: ${comp.county_payment:,.2f}")
```

### County/SPD/MTA Allocations

```python
allocations = (client.sales_tax()
    .county_spd_mta_allocations()
    .in_county("Travis")
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
    print(f"Entity Type: {holder.entity_type}")
    print(f"State of Formation: {holder.state_of_formation}")
    print(f"Address: {holder.taxpayer_address}")
    print(f"City: {holder.taxpayer_city}, {holder.taxpayer_state}")

    if holder.exemption_type:
        print(f"Exemption: {holder.exemption_type}")
```

#### Get Recent Permit Holders

```python
holders = (client.franchise_tax()
    .active_permit_holders()
    .sort_by("registration_date", desc=True)
    .limit(100)
    .get())

for holder in holders[:10]:
    print(f"{holder.taxpayer_name} - Registered: {holder.registration_date}")
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
    .for_county("Travis")
    .get())
```

## Advanced Queries

### Chaining Multiple Filters

```python
# Complex query combining multiple filters
results = (client.sales_tax()
    .active_permits()
    .in_city("San Antonio")
    .in_county("015")  # Bexar County
    .issued_after("2023-01-01")
    .between_dates("2023-01-01", "2024-12-31")
    .sort_by("issue_date", desc=True)
    .limit(50)
    .get())
```

### Resetting Filters

```python
query = client.sales_tax().active_permits()

# First query
austin_permits = query.in_city("Austin").limit(10).get()

# Reset and run different query
query.reset()
houston_permits = query.in_city("Houston").limit(10).get()
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
    .sort_by("issue_date", desc=True)
    .limit(100)
    .get())
```

### Direct Socrata API Access

```python
# For custom queries not covered by the high-level API
dataset_id = "jrea-zgmq"  # Active permits dataset
params = {
    "$where": "outlet_city='Austin'",
    "$limit": 50,
    "$order": "issue_date DESC"
}

raw_data = client.get(dataset_id, params)
```

## Error Handling

### Handling HTTP Errors

```python
from data.exceptions import HttpError, InvalidRequest

try:
    rates = client.sales_tax().rates().in_city("Austin").get()
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
    lambda: client.sales_tax().rates().in_city("Austin").get()
)
```

## Data Processing

### Converting to Pandas DataFrame

```python
import pandas as pd

permits = (client.sales_tax()
    .active_permits()
    .in_city("Austin")
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
    .in_city("Dallas")
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
    .in_city("Houston")
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
total_current = sum(h.current_payment or 0 for h in history)
total_prior = sum(h.prior_payment or 0 for h in history)
total_collections = sum(h.collections or 0 for h in history)

print(f"Total Current Payments: ${total_current:,.2f}")
print(f"Total Prior Payments: ${total_prior:,.2f}")
print(f"Total Collections: ${total_collections:,.2f}")

# Calculate year-over-year change
if total_prior > 0:
    yoy_change = ((total_current - total_prior) / total_prior) * 100
    print(f"Year-over-Year Change: {yoy_change:+.2f}%")
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

### Pagination Pattern

```python
def get_all_permits(city, batch_size=1000):
    """Fetch all permits for a city in batches"""
    all_permits = []
    offset = 0

    while True:
        batch = (client.sales_tax()
            .active_permits()
            .in_city(city)
            .limit(batch_size)
            .get())

        if not batch:
            break

        all_permits.extend(batch)

        if len(batch) < batch_size:
            # Last batch
            break

        offset += batch_size

    return all_permits

# Usage
all_austin_permits = get_all_permits("Austin")
print(f"Total permits in Austin: {len(all_austin_permits)}")
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
    .in_city("Austin")
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
            .in_city(city)
            .get())
    return _cache[city]
```

### Use Appropriate Data Sources

```python
# For historical allocation data, use allocation_history()
# (web scraping - slower but comprehensive)
history = client.sales_tax().allocation_history().for_city("Austin").get()

# For current data, use API-based sources
# (faster, better for real-time queries)
permits = client.sales_tax().active_permits().in_city("Austin").get()
```
