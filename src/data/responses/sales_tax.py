from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, List, Optional

import pandas as pd

from src.data.utils import parse_date, parse_float, parse_int

@dataclass
class ComparisonSummaryData:
    """Sales tax comparison summary data for a jurisdiction.

    Represents year-over-year and period-over-period sales tax payment comparisons
    for Texas counties and cities. This data allows for analyzing payment trends
    and growth patterns across reporting periods.

    Attributes:
        county: County name where the tax was collected.
        city: City name where the tax was collected (if applicable).
        current_rate: Current sales tax rate for the jurisdiction as a decimal.
        net_payment_this_period: Net tax payment amount for the current reporting period.
        comparable_payment_prior_year: Tax payment amount from the same period in the prior year.
        period_percent_change: Percentage change in payment compared to the prior year period.
        payments_to_date: Cumulative payments for the fiscal year to date.
        previous_payments_to_date: Cumulative payments from the previous fiscal year to date.
        year_percent_change: Percentage change in year-to-date payments compared to prior year.
        report_month: Month of the reporting period (1-12).
        report_year: Year of the reporting period.
        report_period_type: Type of reporting period (e.g., "Monthly", "Quarterly").
    """
    county: Optional[str]
    city: Optional[str]
    current_rate: Optional[float]
    net_payment_this_period: Optional[float]
    comparable_payment_prior_year: Optional[float]
    period_percent_change: Optional[float]
    payments_to_date: Optional[float]
    previous_payments_to_date: Optional[float]
    year_percent_change: Optional[float]
    report_month: Optional[int]
    report_year: Optional[int]
    report_period_type: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create instance from a dictionary.

        Parses a dictionary (typically from JSON API response) and constructs
        a ComparisonSummaryData instance with properly typed fields. Numeric
        strings are converted to float or int as appropriate.

        Args:
            data: Dictionary containing the raw data from the API response.

        Returns:
            A new ComparisonSummaryData instance with parsed and typed data.
        """
        return cls(
            county = data.get("county"),
            city = data.get("city"),
            current_rate = data.get("current_rate"),
            net_payment_this_period = parse_float(data.get("net_payment_this_period")),
            comparable_payment_prior_year = parse_float(data.get("comparable_payment_prior_year")),
            period_percent_change = parse_float(data.get("period_percent_change")),
            payments_to_date = parse_float(data.get("payments_to_date")),
            previous_payments_to_date = parse_float(data.get("previous_payments_to_date")),
            year_percent_change = parse_float(data.get("year_percent_change")),
            report_month = parse_int(data.get("report_month")),
            report_year = parse_int(data.get("report_year")),
            report_period_type = data.get("report_period_type")
        )
        
@dataclass
class CountySPDMTAAllocationData:
    """County, special purpose district, or mass transit authority allocation data.

    Represents sales tax allocation data for counties, special purpose districts (SPD),
    and mass transit authorities (MTA) in Texas. This includes current payments,
    historical comparisons, and year-to-date totals.

    Attributes:
        name: Name of the jurisdiction (county, district, or authority).
        jurisdiction_type: Type of jurisdiction (e.g., "County", "SPD", "MTA").
        current_rate: Current sales tax rate for the jurisdiction as a decimal.
        net_payment_this_period: Net tax payment allocated for the current reporting period.
        percent_change_prior_year: Percentage change compared to the same period last year.
        report_year: Year of the reporting period.
        report_month: Month of the reporting period (1-12).
        report_period_type: Type of reporting period (e.g., "Monthly", "Quarterly").
        comparable_payment_prior_year: Payment amount from the same period in the prior year.
        payments_to_date: Cumulative payments allocated for the fiscal year to date.
        previous_payments_to_date: Cumulative payments from the previous fiscal year to date.
        percent_change_to_date: Percentage change in year-to-date payments compared to prior year.
    """
    name: Optional[str]
    jurisdiction_type: Optional[str]
    current_rate: Optional[float]
    net_payment_this_period: Optional[float]
    percent_change_prior_year: Optional[float]
    report_year: Optional[int]
    report_month: Optional[int]
    report_period_type: Optional[str]
    comparable_payment_prior_year: Optional[float]
    payments_to_date: Optional[float]
    previous_payments_to_date: Optional[float]
    percent_change_to_date: Optional[float]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create instance from a dictionary.

        Parses a dictionary (typically from JSON API response) and constructs
        a CountySPDMTAAllocationData instance with properly typed fields. Note that
        the 'type' field in the input data is mapped to 'jurisdiction_type'.

        Args:
            data: Dictionary containing the raw data from the API response.

        Returns:
            A new CountySPDMTAAllocationData instance with parsed and typed data.
        """
        return cls(
            name=data.get("name"),
            jurisdiction_type=data.get("type"),
            current_rate=data.get("current_rate"),
            net_payment_this_period=parse_float(data.get("net_payment_this_period")),
            percent_change_prior_year = parse_float(data.get("percent_change_prior_year")),
            report_year=parse_int(data.get("report_year")),
            report_month=parse_int(data.get("report_month")),
            report_period_type = data.get("report_period_type"),
            comparable_payment_prior_year=parse_float(data.get("comparable_payment_prior_year")),
            payments_to_date=parse_float(data.get("payments_to_date")),
            previous_payments_to_date=parse_float(data.get("previous_payments_to_date")),
            percent_change_to_date=parse_float(data.get("percent_change_to_date")),
        )

@dataclass
class SingleLocalAllocationData:
    """Single local sales tax allocation data for a tax authority.

    Represents allocation data for jurisdictions that levy a single local sales tax.
    This includes monthly payment information and year-over-year comparisons for
    cities and other local tax authorities.

    Attributes:
        authority_type: Type of tax authority (e.g., "City", "County").
        tax_authority: Name of the tax authority collecting the tax.
        report_year: Year of the reporting period.
        report_month: Month of the reporting period (1-12).
        current_net_payment: Net payment allocated for the current reporting period.
        prior_year_net_payment: Net payment from the same period in the prior year.
        yoy_percent_change: Year-over-year percentage change in net payment.
        payment_ytd: Cumulative payments allocated for the fiscal year to date.
        prior_year_payment_ytd: Cumulative payments from the previous fiscal year to date.
        ytd_percent_change: Percentage change in year-to-date payments compared to prior year.
    """
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
        """Create instance from a dictionary.

        Parses a dictionary (typically from JSON API response) and constructs
        a SingleLocalAllocationData instance with properly typed fields.

        Args:
            data: Dictionary containing the raw data from the API response.

        Returns:
            A new SingleLocalAllocationData instance with parsed and typed data.
        """
        return cls(
            authority_type=data.get("authority_type"),
            tax_authority=data.get("tax_authority"),
            report_year=parse_int(data.get("report_year")),
            report_month=parse_int(data.get("report_month")),
            current_net_payment=parse_float(data.get("current_net_payment")),
            prior_year_net_payment=parse_float(data.get("prior_year_net_payment")),
            yoy_percent_change=parse_float(data.get("yoy_percent_change")),
            payment_ytd=parse_float(data.get("payment_ytd")),
            prior_year_payment_ytd=parse_float(data.get("prior_year_payment_ytd")),
            ytd_percent_change=parse_float(data.get("ytd_percent_change")),
        )

@dataclass
class SingleLocalTaxRateData:
    """Single local sales tax rate data for a taxpayer.

    Represents taxpayer information for entities authorized to collect single local
    sales tax. This includes the taxpayer's identification details and the period
    during which they are/were authorized to collect the tax.

    Attributes:
        taxpayer_number: Unique identification number assigned to the taxpayer.
        name: Legal name of the taxpayer or business entity.
        begin_date: Date when the taxpayer became authorized to collect single local sales tax.
        end_date: Date when the taxpayer's authorization ended (None if still active).
    """
    taxpayer_number: str
    name: str
    begin_date: Optional[date]
    end_date: Optional[date]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SingleLocalTaxRateData":
        """Create instance from a dictionary.

        Parses a dictionary (typically from JSON API response) and constructs
        a SingleLocalTaxRateData instance with properly typed fields. Date strings
        in "YYYY-MM-DD" format are parsed into date objects.

        Args:
            data: Dictionary containing the raw data from the API response.

        Returns:
            A new SingleLocalTaxRateData instance with parsed and typed data.
        """
        def parse_date(val: str) -> Optional[date]:
            if not val or pd.isna(val):
                return None
            try:
                return datetime.strptime(val, "%Y-%m-%d").date()
            except Exception:
                return None

        return cls(
            taxpayer_number=data.get("taxpayer_number"),
            name=data.get("name"),
            begin_date=parse_date(data.get("begin_date")),
            end_date=parse_date(data.get("end_date")),
        )

@dataclass
class LocalAllocationPaymentDetailsData:
    """Detailed breakdown of local sales tax allocation payments.

    Represents a comprehensive breakdown of sales tax collections and payments
    allocated to a local tax authority. This includes various collection categories,
    fees, retainages, and the final net payment amount.

    Attributes:
        authority_id: Unique identifier for the tax authority.
        authority_name: Name of the tax authority receiving the allocation.
        allocation_month: The month for which collections are being allocated (first day of month).
        allocation_date: The actual date when the allocation was made.
        total_collections: Total amount of sales tax collected for this authority.
        prior_collections: Collections from prior reporting periods included in this allocation.
        current_collections: Collections from the current reporting period.
        future_collections: Prepayments or collections for future periods.
        audit_collections: Collections resulting from tax audits.
        unidentified_collections: Collections that could not be attributed to a specific period.
        single_local_tax_collections: Collections specific to single local sales tax.
        service_fee: Administrative fee charged by the state for collection services.
        current_retainage: Amount retained from current period collections (typically for audit reserves).
        prior_retainage: Previously retained amounts now being released or adjusted.
        net_payment: Final payment amount allocated to the authority after all adjustments.
    """
    authority_id: str
    authority_name: str
    allocation_month: Optional[date] = None
    allocation_date: Optional[date] = None
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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create instance from a dictionary.

        Parses a dictionary (typically from JSON API response) and constructs
        a LocalAllocationPaymentDetailsData instance with properly typed fields.
        Note that collection field names in the API use abbreviated forms (e.g., "total_coll")
        which are mapped to more descriptive attribute names.

        Args:
            data: Dictionary containing the raw data from the API response.

        Returns:
            A new LocalAllocationPaymentDetailsData instance with parsed and typed data.
        """
        return cls(
            authority_id=data.get("authority_id"),
            authority_name=data.get("authority_name"),
            allocation_month=parse_date(data.get("allocation_month")),
            allocation_date=parse_date(data.get("allocation_date")),
            total_collections=parse_float(data.get("total_coll")),
            prior_collections=parse_float(data.get("prior_coll")),
            current_collections=parse_float(data.get("current_coll")),
            future_collections=parse_float(data.get("future_coll")),
            audit_collections=parse_float(data.get("audit_coll")),
            unidentified_collections=parse_float(data.get("unidentified_coll")),
            single_local_tax_collections=parse_float(data.get("single_local_tax_coll")),
            service_fee=parse_float(data.get("service_fee")),
            current_retainage=parse_float(data.get("current_retainage")),
            prior_retainage=parse_float(data.get("prior_retainage")),
            net_payment=parse_float(data.get("net_payment")),
        )

@dataclass
class MarketplaceProviderAllocationData:
    """Sales tax allocation data for marketplace providers.

    Represents sales tax allocations to local authorities from marketplace providers
    (e.g., online platforms that facilitate sales). These allocations are tracked
    separately due to the unique collection mechanism for marketplace sales.

    Attributes:
        authority_type: Type of tax authority receiving the allocation (e.g., "City", "County").
        authority_id: Unique identifier for the tax authority.
        authority_name: Name of the tax authority receiving the allocation.
        allocation_year: Year when the allocation was made.
        allocation_month: Month when the allocation was made (1-12).
        amount_allocated: Total amount allocated to the authority from marketplace provider collections.
    """
    authority_type: str
    authority_id: str
    authority_name: str
    allocation_year: Optional[int]
    allocation_month: Optional[int]
    amount_allocated: Optional[float]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create instance from a dictionary.

        Parses a dictionary (typically from JSON API response) and constructs
        a MarketplaceProviderAllocationData instance with properly typed fields.
        String fields are explicitly converted to ensure consistent typing.

        Args:
            data: Dictionary containing the raw data from the API response.

        Returns:
            A new MarketplaceProviderAllocationData instance with parsed and typed data.
        """
        return cls(
            authority_type=str(data.get("authority_type", "")),
            authority_id=str(data.get("authority_id", "")),
            authority_name=str(data.get("authority_name", "")),
            allocation_year=parse_int(data.get("allocation_year")),
            allocation_month=parse_int(data.get("allocation_month")),
            amount_allocated=parse_float(data.get("amount_allocated")),
        )

@dataclass
class MarketplaceProviderData:
    """Marketplace provider registration and authorization data.

    Represents a marketplace provider (e.g., online platform) that is registered
    to collect and remit sales tax on behalf of third-party sellers. This includes
    the provider's identification and the period of their authorization.

    Attributes:
        taxpayer_number: Unique identification number assigned to the marketplace provider.
        name: Legal name of the marketplace provider.
        begin_date: Date when the provider became authorized to collect marketplace sales tax.
        end_date: Date when the provider's authorization ended (None if still active).
    """
    taxpayer_number: str
    name: str
    begin_date: Optional[date]
    end_date: Optional[date]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create instance from a dictionary.

        Parses a dictionary (typically from JSON API response) and constructs
        a MarketplaceProviderData instance with properly typed fields. Note that
        this method expects capitalized field names (e.g., "Taxpayer Number") and
        automatically strips whitespace from the name field.

        Args:
            data: Dictionary containing the raw data from the API response.

        Returns:
            A new MarketplaceProviderData instance with parsed and typed data.
        """
        def parse_date(val):
            if not val or pd.isna(val):
                return None
            try:
                return datetime.strptime(str(val), "%Y-%m-%d").date()
            except ValueError:
                return None

        return cls(
            taxpayer_number=str(data.get("Taxpayer Number")),
            name=str(data.get("Taxpayer Name")).strip(),
            begin_date=parse_date(data.get("Begin Date")),
            end_date=parse_date(data.get("End Date")),
        )

@dataclass
class PermittedLocationData:
    """Sales tax permitted location data for taxpayers and their outlets.

    Represents detailed information about a taxpayer and their physical location(s)
    where they are permitted to collect sales tax. This includes taxpayer contact
    information, outlet details, jurisdiction assignments, and business status dates.

    Attributes:
        tp_number: Taxpayer identification number.
        tp_name: Legal name of the taxpayer.
        tp_address: Taxpayer's mailing address.
        tp_city: Taxpayer's city.
        tp_state: Taxpayer's state (typically "TX").
        tp_zip: Taxpayer's ZIP code.
        tp_county: Taxpayer's county.
        org_type: Organization type (e.g., "Corporation", "LLC", "Sole Proprietorship").
        loc_number: Unique location/outlet number.
        loc_name: Name of the outlet/location.
        loc_city: City where the outlet is located.
        loc_state: State where the outlet is located.
        loc_zip: ZIP code of the outlet.
        loc_county: County where the outlet is located.
        naics: North American Industry Classification System code for the business.
        juris_city: Jurisdictional city for tax purposes.
        city_taid: Tax Authority ID for the city.
        mass_transit_auth1_taid: Tax Authority ID for the first mass transit authority (if applicable).
        mass_transit_auth2_taid: Tax Authority ID for the second mass transit authority (if applicable).
        county_taid: Tax Authority ID for the county.
        special_purp_dist1_taid: Tax Authority ID for the first special purpose district (if applicable).
        special_purp_dist2_taid: Tax Authority ID for the second special purpose district (if applicable).
        special_purp_dist3_taid: Tax Authority ID for the third special purpose district (if applicable).
        special_purp_dist4_taid: Tax Authority ID for the fourth special purpose district (if applicable).
        unique_taid: Unique Tax Authority ID combination for this location.
        first_sale_date: Date of first sale at this location.
        out_of_business_date: Date the location went out of business (None if still active).
    """
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
    first_sale_date: Optional[date]
    out_of_business_date: Optional[date]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create instance from a dictionary.

        Parses a dictionary (typically from JSON API response) and constructs
        a PermittedLocationData instance with properly typed fields. Date strings
        in ISO format with microseconds are parsed into date objects.

        Args:
            data: Dictionary containing the raw data from the API response.

        Returns:
            A new PermittedLocationData instance with parsed and typed data.
        """
        def parse_date(val):
            if not val:
                return None
            try:
                return datetime.strptime(val, "%Y-%m-%dT%H:%M:%S.%f").date()
            except ValueError:
                return None

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
            first_sale_date=parse_date(data.get("first_sale_date")),
            out_of_business_date=parse_date(data.get("out_of_business_date")),
        )

@dataclass
class ActivePermitData:
    """Active sales tax permit data for taxpayers and their outlets.

    Represents current, active sales tax permits held by taxpayers for specific
    outlet locations. This includes comprehensive taxpayer and outlet information,
    business classification, and key dates related to permit issuance and sales activity.

    Attributes:
        taxpayer_number: Unique identification number assigned to the taxpayer.
        taxpayer_name: Legal name of the taxpayer.
        taxpayer_address: Taxpayer's mailing address.
        taxpayer_city: Taxpayer's city.
        taxpayer_state: Taxpayer's state.
        taxpayer_zip_code: Taxpayer's ZIP code.
        taxpayer_county_code: County code where the taxpayer is located.
        taxpayer_organization_type: Type of organization (e.g., "Corporation", "LLC").
        outlet_number: Unique identification number for the outlet/location.
        outlet_name: Name of the outlet/location.
        outlet_address: Physical address of the outlet.
        outlet_city: City where the outlet is located.
        outlet_state: State where the outlet is located.
        outlet_zip_code: ZIP code of the outlet.
        outlet_county_code: County code where the outlet is located.
        outlet_naics_code: North American Industry Classification System code for the outlet.
        outlet_inside_outside_city_limits_indicator: Indicates if outlet is inside ("I") or outside ("O") city limits.
        outlet_permit_issue_date: Date when the sales tax permit was issued (as string).
        outlet_first_sales_date: Date of first sale at this outlet (as string).
    """
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
        """Create instance from a dictionary.

        Parses a dictionary (typically from JSON API response) and constructs
        an ActivePermitData instance with properly typed fields. Date fields are
        kept as strings as they appear in the source data.

        Args:
            data: Dictionary containing the raw data from the API response.

        Returns:
            A new ActivePermitData instance with parsed and typed data.
        """
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
    """Sales tax rate change data for jurisdictions.

    Represents changes to sales tax rates for Texas jurisdictions. This includes
    information about rate changes, the jurisdictions affected, effective dates,
    and reporting periods.

    Attributes:
        type: Type of jurisdiction (e.g., "City", "County", "SPD", "MTA").
        city_name: Name of the city (if applicable).
        county_name: Name of the county (if applicable).
        old_rate: Previous sales tax rate as a decimal.
        new_rate: New sales tax rate as a decimal.
        effective_date: Date when the new rate becomes effective (as string).
        report_month: Month of the reporting period (1-12).
        report_year: Year of the reporting period.
        report_period_type: Type of reporting period (e.g., "Monthly", "Quarterly").
    """
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
        """Create instance from a dictionary.

        Parses a dictionary (typically from JSON API response) and constructs
        a SalesTaxRateData instance with properly typed fields. Rate values are
        parsed as floats representing decimal percentages.

        Args:
            data: Dictionary containing the raw data from the API response.

        Returns:
            A new SalesTaxRateData instance with parsed and typed data.
        """
        return cls(
            type=data.get("type"),
            city_name=data.get("city_name"),
            county_name=data.get("county_name"),
            old_rate=parse_float(data.get("old_rate")),
            new_rate=parse_float(data.get("new_rate")),
            effective_date=data.get("effective_date"),
            report_month=parse_int(data.get("report_month")),
            report_year=parse_int(data.get("report_year")),
            report_period_type=data.get("report_period_type"),
        )

@dataclass
class DirectPayTaxpayerData:
    """Direct pay taxpayer authorization data.

    Represents taxpayers who are authorized to use the direct pay method for
    sales tax. Direct pay allows qualified taxpayers to issue exemption certificates
    to sellers and remit the tax directly to the state, rather than paying tax
    at the point of purchase.

    Attributes:
        tp_id: Unique taxpayer identification number.
        name: Legal name of the taxpayer.
        address: Taxpayer's mailing address.
        city: Taxpayer's city.
        state: Taxpayer's state.
        zip_code: Taxpayer's ZIP code.
        county: Taxpayer's county.
        business_type: Type of business or organization.
        naics_code: North American Industry Classification System code.
        responsibility_begin_date: Date when direct pay authorization began.
    """
    tp_id: str
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    county: str
    business_type: Optional[str]
    naics_code: Optional[str]
    responsibility_begin_date: Optional[datetime]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create instance from a dictionary.

        Parses a dictionary (typically from JSON API response) and constructs
        a DirectPayTaxpayerData instance with properly typed fields. The ID field
        in the source is mapped to tp_id, and the zip field is mapped to zip_code.

        Args:
            data: Dictionary containing the raw data from the API response.

        Returns:
            A new DirectPayTaxpayerData instance with parsed and typed data.
        """
        def parse_date(value):
            if not value:
                return None
            try:
                return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f").date()
            except ValueError:
                return None

        return cls(
            tp_id=data.get("id"),
            name=data.get("name"),
            address=data.get("address"),
            city=data.get("city"),
            state=data.get("state"),
            zip_code=data.get("zip"),
            county=data.get("county"),
            business_type=data.get("business_type"),
            naics_code=data.get("naics_code"),
            responsibility_begin_date=parse_date(data.get("responsibility_begin_date")),
        )

@dataclass
class AllocationHistoryData:
    """Historical sales tax allocation data for a tax authority.

    Represents historical allocation payment data for a specific tax authority,
    typically scraped from HTML tables or reports. This provides a time series
    of monthly allocations for trend analysis.

    Attributes:
        authority_id: Unique identifier for the tax authority.
        authority_name: Name of the tax authority receiving allocations.
        allocation_month: The month for which the allocation is made (first day of month).
        allocation_date: The date representation of the allocation period.
        net_payment: Net payment amount allocated for the period.
        total_collections: Total collections for the period (often None for historical data).
    """
    authority_id: str
    authority_name: str
    allocation_month: date
    allocation_date: date
    net_payment: Optional[float]
    total_collections: Optional[float]

    @classmethod
    def from_row(cls, row: List[str], year_text: str, authority_id: str, authority_name: str):
        """Create instance from a table row.

        Parses a list representing a row from an HTML table or similar tabular data
        and constructs an AllocationHistoryData instance. This method handles parsing
        month names (both full and abbreviated) and numeric amounts with comma separators.

        Args:
            row: List containing row data where row[0] is the month name and row[1] is the amount.
            year_text: Year as a string (e.g., "2023").
            authority_id: Unique identifier for the tax authority.
            authority_name: Name of the tax authority.

        Returns:
            A new AllocationHistoryData instance with parsed data, or None if parsing fails.
        """
        def f(x: str) -> Optional[float]:
            try:
                return float(x.replace(",", ""))
            except Exception:
                return None

        month_text, amount_text = row[0], row[1]
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
    """Quarterly sales history data for a jurisdiction.

    Represents aggregated sales data reported on a quarterly basis for Texas
    jurisdictions. This includes gross and taxable sales broken down by industry
    or summary type, providing insights into economic activity and tax base.

    Attributes:
        jurisdiction_name: Name of the jurisdiction (defaults to "Texas" for statewide data).
        jurisdiction_type: Type of jurisdiction (e.g., "State", "County", "City").
        industry_label: Industry classification label (e.g., "Retail Trade", "Food Services").
        summary_type: Type of summary aggregation (e.g., "Total", "Industry").
        report_kind: Kind of report (defaults to "Summary").
        year: Year of the quarterly report.
        quarter: Quarter number (1-4).
        gross_sales: Total gross sales for the period.
        taxable_sales: Total taxable sales for the period.
        num_outlets: Number of outlets reporting in the jurisdiction/industry.
    """
    jurisdiction_name: str
    jurisdiction_type: str
    industry_label: Optional[str]
    summary_type: Optional[str]
    report_kind: str
    year: int
    quarter: int
    gross_sales: Optional[float]
    taxable_sales: Optional[float]
    num_outlets: Optional[int]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuarterlySalesHistoryData":
        """Create instance from a dictionary.

        Parses a dictionary (typically from JSON API response) and constructs
        a QuarterlySalesHistoryData instance with properly typed fields. Provides
        sensible defaults for jurisdiction_name, jurisdiction_type, and report_kind
        when not present in the source data.

        Args:
            data: Dictionary containing the raw data from the API response.

        Returns:
            A new QuarterlySalesHistoryData instance with parsed and typed data.
        """
        return cls(
            jurisdiction_name=data.get("jurisdiction_name", "Texas"),
            jurisdiction_type=data.get("jurisdiction_type", "State"),
            industry_label=data.get("industry_label"),
            summary_type=data.get("summary_type"),
            report_kind=data.get("report_kind", "Summary"),
            year=parse_int(data.get("year")) or 0,
            quarter=parse_int(data.get("quarter")) or 0,
            gross_sales=parse_float(data.get("gross_sales")),
            taxable_sales=parse_float(data.get("taxable_sales")),
            num_outlets=parse_int(data.get("num_outlets")),
        )