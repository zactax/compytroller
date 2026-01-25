# Data Sources Reference

Comprehensive reference for all Texas Comptroller data sources available through Compytroller.

## Overview

Compytroller accesses data from three types of sources:

1. **Socrata Open Data API** - Primary source (data.texas.gov)
2. **Web Forms** - Historical allocation data (mycpa.cpa.state.tx.us)
3. **CSV Downloads** - Static exports (assets.comptroller.texas.gov)

## Sales Tax Data Sources

### Active Permits

**Source Type:** Socrata API
**Dataset ID:** `jrea-zgmq`
**URL:** https://data.texas.gov/dataset/Sales-Tax-Active-Permits/jrea-zgmq

**Description:**
Current list of active sales tax permit holders with taxpayer and outlet information.

**Fields:**
- Taxpayer number, name, and address
- Outlet number, name, and address
- Issue date
- Permit status

**Common Use Cases:**
- Verify permit status for a business
- Find all outlets for a taxpayer
- Search permits by location
- Track new permit issuance

**Example:**
```python
permits = (client.sales_tax()
    .active_permits()
    .for_taxpayer("12345678")
    .get())
```

**Update Frequency:** Daily

---

### Sales Tax Rates

**Source Type:** Socrata API
**Dataset ID:** `tmhs-ahbh`
**URL:** https://data.texas.gov/dataset/Sales-and-Use-Tax-Rates/tmhs-ahbh

**Description:**
Current and historical sales tax rates by jurisdiction.

**Fields:**
- County and city names
- State rate (currently 6.25%)
- Local rate
- Combined rate
- Effective date
- Expiration date

**Common Use Cases:**
- Calculate sales tax for a location
- Track rate changes over time
- Compare rates across jurisdictions

**Example:**
```python
rates = (client.sales_tax()
    .rates()
    .for_city("Austin")
    .get())
```

**Update Frequency:** As rates change (varies by jurisdiction)

---

### Allocation History

**Source Type:** Web Scraping
**URL:** https://mycpa.cpa.state.tx.us/allocation/

**Description:**
Monthly historical allocation payments to cities, counties, transit authorities, and special districts.

**Fields:**
- Jurisdiction name
- Period (month/year)
- Current payment amount
- Prior year payment amount
- Collections

**Common Use Cases:**
- Analyze revenue trends
- Compare year-over-year changes
- Calculate total allocations
- Forecast future revenue

**Example:**
```python
history = (client.sales_tax()
    .allocation_history()
    .for_city("Austin")
    .get())
```

**Update Frequency:** Monthly

**Note:** This source uses web scraping and may be slower than API-based sources.

---

### Allocation Payment Details

**Source Type:** Socrata API
**Dataset ID:** `3p4v-vsr3`
**URL:** https://data.texas.gov/dataset/Sales-Tax-Local-Allocation-Payment-Detail/3p4v-vsr3

**Description:**
Detailed breakdown of local sales tax allocation payments.

**Fields:**
- Jurisdiction information
- Payment period
- Payment amounts by category
- Adjustment details

**Common Use Cases:**
- Detailed payment analysis
- Reconciliation
- Audit trail

**Example:**
```python
details = (client.sales_tax()
    .allocation_payment_details()
    .for_city("Dallas")
    .get())
```

**Update Frequency:** Monthly

---

### Single Local Allocations

**Source Type:** Socrata API
**Dataset ID:** `5yx2-afcg`
**URL:** https://data.texas.gov/dataset/Sales-Tax-Single-Local-Allocations/5yx2-afcg

**Description:**
Allocations to single local jurisdictions with year-over-year comparisons.

**Fields:**
- Jurisdiction name and type
- Current year payment
- Prior year payment
- Payment difference
- Percentage change

**Common Use Cases:**
- Year-over-year comparison
- Revenue growth analysis
- Jurisdiction ranking

**Example:**
```python
allocations = (client.sales_tax()
    .single_local_allocations()
    .sort_by("current_year_payment", desc=True)
    .limit(50)
    .get())
```

**Update Frequency:** Quarterly

---

### Marketplace Provider Allocations

**Source Type:** Socrata API
**Dataset ID:** `hezn-fbgw`
**URL:** https://data.texas.gov/dataset/Sales-Tax-Marketplace-Provider-Allocations/hezn-fbgw

**Description:**
Sales tax allocations collected by marketplace providers (e.g., Amazon, eBay).

**Fields:**
- Provider name
- Jurisdiction
- Allocation period
- Payment amounts

**Common Use Cases:**
- Track marketplace sales impact
- Analyze e-commerce tax revenue
- Compare marketplace vs traditional retail

**Example:**
```python
allocations = (client.sales_tax()
    .marketplace_provider_allocations()
    .for_provider("Amazon")
    .get())
```

**Update Frequency:** Monthly

---

### Marketplace Providers

**Source Type:** CSV Download
**URL:** https://assets.comptroller.texas.gov/open-data-files/marketplace-providers.csv

**Description:**
Registry of marketplace providers registered to collect and remit Texas sales tax.

**Fields:**
- Provider name
- Registration date
- Effective date
- Status

**Common Use Cases:**
- Verify provider registration
- List all registered providers
- Track new registrations

**Example:**
```python
providers = client.sales_tax().marketplace_provider().get()
```

**Update Frequency:** Weekly

**Note:** This source downloads the entire CSV file (no filtering at source).

---

### Permitted Locations

**Source Type:** Socrata API
**Dataset ID:** `3kx8-uryv`
**URL:** https://data.texas.gov/dataset/Sales-Tax-Permitted-Locations/3kx8-uryv

**Description:**
Comprehensive location details for sales tax permitted outlets (31+ fields).

**Fields:**
- Complete taxpayer and outlet information
- Geographic coordinates
- Jurisdiction codes (city, county, special districts)
- Tax rate information
- Permit dates and status

**Common Use Cases:**
- Geographic analysis
- Multi-outlet taxpayer tracking
- Jurisdiction mapping
- Location-based reporting

**Example:**
```python
locations = (client.sales_tax()
    .permitted_locations()
    .in_zip("78701")
    .get())
```

**Update Frequency:** Daily

---

### Direct Pay Taxpayers

**Source Type:** Socrata API
**Dataset ID:** `deed-e7u6`
**URL:** https://data.texas.gov/dataset/Sales-Tax-Direct-Pay-Taxpayers/deed-e7u6

**Description:**
List of taxpayers authorized for direct payment of sales tax.

**Fields:**
- Taxpayer number
- Taxpayer name
- Effective date
- Status

**Common Use Cases:**
- Verify direct pay authorization
- Identify qualified taxpayers
- Track authorization changes

**Example:**
```python
direct_pay = (client.sales_tax()
    .direct_pay_taxpayers()
    .for_taxpayer("12345678")
    .get())
```

**Update Frequency:** Monthly

---

### Quarterly Sales History

**Source Type:** Web Scraping
**URL:** https://mycpa.cpa.state.tx.us/allocation/

**Description:**
Quarterly taxable sales by jurisdiction and industry classification (NAICS).

**Fields:**
- Jurisdiction name and type
- Industry classification
- Quarter/year
- Taxable sales amount
- Number of outlets

**Common Use Cases:**
- Economic analysis by industry
- Seasonal trend analysis
- Industry concentration studies
- MSA-level analysis

**Example:**
```python
sales = (client.sales_tax()
    .quarterly_sales_history()
    .for_city("Austin")
    .for_industry("Retail Trade")
    .get())
```

**Update Frequency:** Quarterly

**Note:** This source uses web scraping and may be slower than API-based sources.

---

### Single Local Tax Rates

**Source Type:** Internal
**Dataset ID:** N/A

**Description:**
Tax rates for single local jurisdictions with validity periods.

**Fields:**
- Jurisdiction name
- Tax rate
- Effective date
- Expiration date

**Common Use Cases:**
- Rate lookup by date
- Historical rate tracking
- Rate change analysis

**Example:**
```python
rates = (client.sales_tax()
    .single_local_tax_rates()
    .limit(100)
    .get())
```

**Update Frequency:** As rates change

---

### City/County Comparison Summary

**Source Type:** Socrata API
**Dataset ID:** `53pa-m7sm`
**URL:** https://data.texas.gov/dataset/Sales-Tax-City-County-Comparison-Summary/53pa-m7sm

**Description:**
Comparison of sales tax payments between cities and their counties.

**Fields:**
- City and county names
- Payment period
- City payment amount
- County payment amount
- Comparison metrics

**Common Use Cases:**
- City vs county revenue analysis
- Jurisdiction comparison
- Economic activity distribution

**Example:**
```python
comparison = (client.sales_tax()
    .city_county_comparison_summary()
    .for_city("Austin")
    .get())
```

**Update Frequency:** Quarterly

---

### County/SPD/MTA Allocations

**Source Type:** Socrata API
**Dataset ID:** `qsh8-tby8`
**URL:** https://data.texas.gov/dataset/Sales-Tax-County-SPD-MTA-Allocations/qsh8-tby8

**Description:**
Combined allocations for counties, special purpose districts, and metropolitan transit authorities.

**Fields:**
- County information
- Special district details
- MTA information
- Allocation amounts
- Payment periods

**Common Use Cases:**
- Multi-jurisdiction analysis
- Special district revenue tracking
- Transit authority funding analysis

**Example:**
```python
allocations = (client.sales_tax()
    .county_spd_mta_allocations()
    .in_county("Travis")
    .get())
```

**Update Frequency:** Monthly

---

## Franchise Tax Data Sources

### Active Permit Holders

**Source Type:** Socrata API
**Dataset ID:** `9cir-efmm`
**URL:** https://data.texas.gov/dataset/Franchise-Tax-Active-Permit-Holders/9cir-efmm

**Description:**
Registry of active franchise tax permit holders (corporations and other taxable entities).

**Fields (19 total):**
- Taxpayer number and name
- Entity type
- State of formation
- Address information
- Registration date
- Exemption type (if applicable)
- Status information

**Common Use Cases:**
- Corporate entity verification
- Tax status lookup
- Entity type analysis
- Exemption tracking

**Example:**
```python
holders = (client.franchise_tax()
    .active_permit_holders()
    .for_taxpayer("12345678")
    .get())
```

**Update Frequency:** Daily

**Entity Types Include:**
- Corporations
- Limited Liability Companies (LLC)
- Professional Associations
- Limited Partnerships
- And others

---

## Mixed Beverage Tax Data Sources

### Gross Receipts

**Source Type:** Socrata API
**Dataset ID:** `naix-2893`
**URL:** https://data.texas.gov/dataset/Mixed-Beverage-Gross-Receipts/naix-2893

**Description:**
Gross receipts reported by mixed beverage permit holders, broken down by beverage type.

**Fields:**
- Taxpayer information
- Reporting period
- Total gross receipts
- Beer receipts
- Liquor receipts
- Wine receipts
- Other beverage receipts

**Common Use Cases:**
- Revenue analysis by beverage type
- Permit holder comparison
- Seasonal trend analysis
- Industry benchmarking

**Example:**
```python
receipts = (client.mixed_beverage_tax()
    .gross_receipts()
    .for_year(2024)
    .limit(100)
    .get())
```

**Update Frequency:** Monthly

---

### Allocation History

**Source Type:** Web Scraping
**URL:** https://mycpa.cpa.state.tx.us/allocation/

**Description:**
Monthly historical allocation payments of mixed beverage taxes to cities, counties, and special districts.

**Fields:**
- Jurisdiction name
- Period (month/year)
- Current payment amount
- Prior year payment amount
- Collections

**Common Use Cases:**
- Revenue trend analysis
- Year-over-year comparisons
- Budget forecasting
- Economic impact studies

**Example:**
```python
history = (client.mixed_beverage_tax()
    .history()
    .for_city("Austin")
    .get())
```

**Update Frequency:** Monthly

**Note:** This source uses web scraping and may be slower than API-based sources.

---

## Data Source Comparison

### By Update Frequency

| Frequency | Data Sources |
|-----------|-------------|
| **Daily** | Active Permits, Permitted Locations, Franchise Permit Holders |
| **Weekly** | Marketplace Providers |
| **Monthly** | Most allocation data, Direct Pay Taxpayers, Gross Receipts |
| **Quarterly** | Single Local Allocations, Quarterly Sales, Comparison Summary |
| **Variable** | Tax Rates (as rates change) |

### By Source Type

| Type | Advantages | Disadvantages | Data Sources |
|------|-----------|---------------|--------------|
| **Socrata API** | Fast, filterable, structured | Requires app token | Most datasets |
| **Web Scraping** | Comprehensive historical data | Slower, less flexible | Allocation histories, quarterly sales |
| **CSV Download** | Simple, complete datasets | No server-side filtering | Marketplace providers |

### By Query Capabilities

| Feature | Socrata API | Web Scraping | CSV Download |
|---------|-------------|--------------|--------------|
| Server-side filtering | ✓ | Limited | ✗ |
| Sorting | ✓ | ✗ | ✗ |
| Pagination | ✓ | ✗ | ✗ |
| Full-text search | ✓ | ✗ | ✗ |
| Date range queries | ✓ | ✗ | ✗ |

## Field Reference

### Common Field Types

- **Taxpayer Number**: 11-digit identifier (string)
- **Dates**: ISO 8601 format (YYYY-MM-DD)
- **Amounts**: Decimal values (float)
- **Codes**: County codes, jurisdiction codes (string)
- **Rates**: Percentage values (float)

### County Codes

Texas uses 3-digit county codes. Examples:
- 227 = Travis County
- 201 = Harris County
- 057 = Dallas County
- 015 = Bexar County

Full list available at: https://www.census.gov/library/reference/code-lists/ansi.html#cousub

### NAICS Codes

Industry classifications follow the North American Industry Classification System.

Common codes:
- 44-45: Retail Trade
- 72: Accommodation and Food Services
- 23: Construction
- 31-33: Manufacturing

Full list: https://www.census.gov/naics/

### Jurisdiction Types

- **City**: Municipal corporation
- **County**: County government
- **SPD**: Special Purpose District
- **MTA**: Metropolitan Transit Authority

## Data Quality Notes

### Known Limitations

1. **Historical Data**: Some datasets only include recent data (last 2-5 years)
2. **Null Values**: Optional fields may contain null/empty values
3. **Name Variations**: Jurisdiction names may vary slightly across datasets
4. **Lag Time**: Some data has a 1-3 month reporting lag
5. **Redactions**: Certain data may be redacted for privacy (e.g., single taxpayers)

### Best Practices

1. **Always handle null values** in optional fields
2. **Use taxpayer numbers** for exact matching (not names)
3. **Check effective dates** when working with rates
4. **Validate jurisdictions** against official lists
5. **Cache results** for frequently accessed data
6. **Implement retry logic** for web-scraped sources
7. **Use date ranges** to limit result sets

### Data Freshness

Check the data source URLs on data.texas.gov for:
- Last update timestamp
- Data refresh schedule
- Known data issues

## Authentication

### Socrata App Token

Required for API-based data sources.

**Get a token:**
1. Visit https://data.texas.gov
2. Sign up for a free account
3. Go to https://data.texas.gov/profile/app_tokens
4. Create an app token

**Rate Limits:**
- With token: 1,000 requests/hour
- Without token: 100 requests/hour

**Usage:**
```python
client = ComptrollerClient.factory(app_token="your-token-here")
```

### No Authentication Required

These sources don't require an app token:
- CSV downloads (Marketplace Providers)
- Web scraping sources (Allocation History, Quarterly Sales)

However, the main client still requires a token for initialization.

## Additional Resources

- **Texas Comptroller Open Data Portal**: https://data.texas.gov
- **Comptroller Allocation Reports**: https://mycpa.cpa.state.tx.us/allocation/
- **API Documentation**: https://dev.socrata.com/
- **Socrata Query Language (SoQL)**: https://dev.socrata.com/docs/queries/
