from dataclasses import dataclass
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class ComparisonSummaryData:
    jurisdiction: Optional[str]          # city / county / name
    jurisdiction_type: Optional[str]     # only for qsh8-tby8
    county: Optional[str]                # only for 53pa-m7sm
    report_year: Optional[int]
    report_month: Optional[int]
    net_payment_this_period: Optional[float]
    comparable_payment_prior_year: Optional[float]
    payments_to_date: Optional[float]
    previous_payments_to_date: Optional[float]
    percent_change: Optional[float]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        def parse_float(val):
            try:
                return float(val)
            except Exception:
                return None

        def parse_int(val):
            try:
                return int(val)
            except Exception:
                return None

        # figure out the jurisdiction field
        jurisdiction = (
            data.get("city") or
            data.get("name") or
            None
        )
        county = data.get("county")
        jtype = data.get("type")

        # percent change could be period, year, or ytd depending on dataset
        pct = (
            data.get("period_percent_change")
            or data.get("year_percent_change")
            or data.get("ytd_percent_change")
            or data.get("percent_change_prior_year")
            or data.get("percent_change_to_date")
        )

        return cls(
            jurisdiction=jurisdiction,
            jurisdiction_type=jtype,
            county=county,
            report_year=parse_int(data.get("report_year")),
            report_month=parse_int(data.get("report_month")),
            net_payment_this_period=parse_float(data.get("net_payment_this_period")),
            comparable_payment_prior_year=parse_float(data.get("comparable_payment_prior_year")),
            payments_to_date=parse_float(data.get("payments_to_date")),
            previous_payments_to_date=parse_float(data.get("previous_payments_to_date")),
            percent_change=parse_float(pct),
        )

@dataclass
class SingleLocalAllocationData:
    authority_type: str
    tax_authority: str
    report_year: Optional[int]
    report_month: Optional[int]
    current_net_payment: Optional[float]
    prior_year_net_payment: Optional[float]
    yoy_percent_change: Optional[float]
    payment_ytd: Optional[float]
    prior_year_payment_ytd: Optional[float]
    ytd_percent_change: Optional[float]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        def f(x):
            try:
                return float(x)
            except Exception:
                return None
        def i(x):
            try:
                return int(x)
            except Exception:
                return None

        return cls(
            authority_type=data.get("authority_type"),
            tax_authority=data.get("tax_authority"),
            report_year=i(data.get("report_year")),
            report_month=i(data.get("report_month")),
            current_net_payment=f(data.get("current_net_payment")),
            prior_year_net_payment=f(data.get("prior_year_net_payment")),
            yoy_percent_change=f(data.get("yoy_percent_change")),
            payment_ytd=f(data.get("payment_ytd")),
            prior_year_payment_ytd=f(data.get("prior_year_payment_ytd")),
            ytd_percent_change=f(data.get("ytd_percent_change")),
        )
    
@dataclass
class SingleLocalTaxRateData:
    taxpayer_number: str
    name: str
    begin_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
     
@dataclass
class LocalAllocationPaymentDetailsData:
    authority_id: str
    authority_name: str
    allocation_month: Optional[datetime] = None
    allocation_date: Optional[datetime] = None
    total_collections: Optional[float] = None
    prior_collections: Optional[float] = None
    current_collections: Optional[float] = None
    future_collections: Optional[float] = None
    audit_collections: Optional[float] = None
    unidentified_collections: Optional[float] = None
    single_local_tax_collections: Optional[float] = None
    service_fee: Optional[float] = None
    current_retainage: Optional[float] = None
    prior_retainage: Optional[float] = None
    net_payment: Optional[float] = None

@dataclass
class MarketplaceProviderAllocationData:
    authority_type: str
    authority_id: str
    authority_name: str
    allocation_year: Optional[int]
    allocation_month: Optional[int]
    amount_allocated: Optional[float]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        def f(x):
            try: return float(x)
            except: return None
        def i(x):
            try: return int(x)
            except: return None

        return cls(
            authority_type=data.get("authority_type"),
            authority_id=data.get("authority_id"),
            authority_name=data.get("authority_name"),
            allocation_year=i(data.get("allocation_year")),
            allocation_month=i(data.get("allocation_month")),
            amount_allocated=f(data.get("amount_allocated")),
        )
        
@dataclass
class MarketplaceProviderData:
    taxpayer_number: str
    name: str
    begin_date: Optional[datetime.date]
    end_date: Optional[datetime.date]

@dataclass
class PermittedLocationData:
    tp_number: str
    tp_name: str
    tp_address: str
    tp_city: str
    tp_state: str
    tp_zip: str
    tp_county: str
    org_type: Optional[str]
    loc_number: str
    loc_name: str
    loc_city: str
    loc_state: str
    loc_zip: str
    loc_county: str
    naics: Optional[str]
    juris_city: Optional[str]
    city_taid: Optional[str]
    mass_transit_auth1_taid: Optional[str]
    mass_transit_auth2_taid: Optional[str]
    county_taid: Optional[str]
    special_purp_dist1_taid: Optional[str]
    special_purp_dist2_taid: Optional[str]
    special_purp_dist3_taid: Optional[str]
    special_purp_dist4_taid: Optional[str]
    unique_taid: Optional[str]
    first_sale_date: Optional[str]
    out_of_business_date: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            tp_number=data.get("tp_number"),
            tp_name=data.get("tp_name"),
            tp_address=data.get("tp_address"),
            tp_city=data.get("tp_city"),
            tp_state=data.get("tp_state"),
            tp_zip=data.get("tp_zip"),
            tp_county=data.get("tp_county"),
            org_type=data.get("org_type"),
            loc_number=data.get("loc_number"),
            loc_name=data.get("loc_name"),
            loc_city=data.get("loc_city"),
            loc_state=data.get("loc_state"),
            loc_zip=data.get("loc_zip"),
            loc_county=data.get("loc_county"),
            naics=data.get("naics"),
            juris_city=data.get("juris_city"),
            city_taid=data.get("city_taid"),
            mass_transit_auth1_taid=data.get("mass_transit_auth1_taid"),
            mass_transit_auth2_taid=data.get("mass_transit_auth2_taid"),
            county_taid=data.get("county_taid"),
            special_purp_dist1_taid=data.get("special_purp_dist1_taid"),
            special_purp_dist2_taid=data.get("special_purp_dist2_taid"),
            special_purp_dist3_taid=data.get("special_purp_dist3_taid"),
            special_purp_dist4_taid=data.get("special_purp_dist4_taid"),
            unique_taid=data.get("unique_taid"),
            first_sale_date=data.get("first_sale_date"),
            out_of_business_date=data.get("out_of_business_date"),
        )

@dataclass
class ActivePermitData:
    taxpayer_number: str
    taxpayer_name: str
    taxpayer_address: str
    taxpayer_city: str
    taxpayer_state: str
    taxpayer_zip_code: str
    taxpayer_county_code: str
    taxpayer_organization_type: Optional[str]
    outlet_number: str
    outlet_name: str
    outlet_address: str
    outlet_city: str
    outlet_state: str
    outlet_zip_code: str
    outlet_county_code: str
    outlet_naics_code: Optional[str]
    outlet_inside_outside_city_limits_indicator: Optional[str]
    outlet_permit_issue_date: Optional[str]
    outlet_first_sales_date: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            taxpayer_number=data.get("taxpayer_number"),
            taxpayer_name=data.get("taxpayer_name"),
            taxpayer_address=data.get("taxpayer_address"),
            taxpayer_city=data.get("taxpayer_city"),
            taxpayer_state=data.get("taxpayer_state"),
            taxpayer_zip_code=data.get("taxpayer_zip_code"),
            taxpayer_county_code=data.get("taxpayer_county_code"),
            taxpayer_organization_type=data.get("taxpayer_organization_type"),
            outlet_number=data.get("outlet_number"),
            outlet_name=data.get("outlet_name"),
            outlet_address=data.get("outlet_address"),
            outlet_city=data.get("outlet_city"),
            outlet_state=data.get("outlet_state"),
            outlet_zip_code=data.get("outlet_zip_code"),
            outlet_county_code=data.get("outlet_county_code"),
            outlet_naics_code=data.get("outlet_naics_code"),
            outlet_inside_outside_city_limits_indicator=data.get("outlet_inside_outside_city_limits_indicator"),
            outlet_permit_issue_date=data.get("outlet_permit_issue_date"),
            outlet_first_sales_date=data.get("outlet_first_sales_date"),
        )
        
@dataclass
class SalesTaxRateData:
    type: str
    city_name: Optional[str]
    county_name: Optional[str]
    old_rate: Optional[float]
    new_rate: Optional[float]
    effective_date: Optional[str]
    report_month: Optional[int]
    report_year: Optional[int]
    report_period_type: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        def f(x):
            try: return float(x)
            except: return None
        def i(x):
            try: return int(x)
            except: return None

        return cls(
            type=data.get("type"),
            city_name=data.get("city_name"),
            county_name=data.get("county_name"),
            old_rate=f(data.get("old_rate")),
            new_rate=f(data.get("new_rate")),
            effective_date=data.get("effective_date"),
            report_month=i(data.get("report_month")),
            report_year=i(data.get("report_year")),
            report_period_type=data.get("report_period_type"),
        )

@dataclass
class DirectPayTaxpayerData:
    id: str
    name: str
    address: str
    city: str
    state: str
    zip: str
    county: str
    business_type: Optional[str]
    naics_code: Optional[str]
    responsibility_begin_date: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            address=data.get("address"),
            city=data.get("city"),
            state=data.get("state"),
            zip=data.get("zip"),
            county=data.get("county"),
            business_type=data.get("business_type"),
            naics_code=data.get("naics_code"),
            responsibility_begin_date=data.get("responsibility_begin_date"),
        )

@dataclass
class AllocationHistoryData:
    authority_id: str
    authority_name: str
    allocation_month: date   
    allocation_date: date         
    net_payment: Optional[float]
    total_collections: Optional[float]

    @classmethod
    def from_row(
        cls, row: List[str], year_text: str, authority_id: str, authority_name: str
    ):
        """
        Parse a row from AllocHist tables.
        row: [Month, Amount, ...]
        """
        def f(x: str) -> Optional[float]:
            try:
                return float(x.replace(",", ""))
            except Exception:
                return None

        month_text, amount_text = row[0], row[1]

        # Parse month name + year into a date
        try:
            dt = datetime.strptime(f"{month_text} {year_text}", "%B %Y")
        except ValueError:
            try:
                dt = datetime.strptime(f"{month_text} {year_text}", "%b %Y")
            except ValueError:
                return None

        return cls(
            authority_id=authority_id,
            authority_name=authority_name,
            allocation_month=dt.date().replace(day=1),
            allocation_date=dt.date(),
            net_payment=f(amount_text),
            total_collections=None,
        )

@dataclass
class QuarterlySalesHistoryData:
    # Jurisdiction context
    jurisdiction_name: str            # "Texas", "Austin", "Travis", etc.
    jurisdiction_type: str            # "State", "City", "County", "MSA"

    # Report metadata
    industry_label: str               # "All Industries", "Retail Trade", etc.
    summary_type: Optional[str]       # "In-State", "Out-of-State", "Grand Totals" (summary only)
    report_kind: str                  # "Summary" or "CCMA"

    # Time series values
    year: int
    quarter: int
    gross_sales: Optional[float]
    taxable_sales: Optional[float]
    num_outlets: Optional[int]