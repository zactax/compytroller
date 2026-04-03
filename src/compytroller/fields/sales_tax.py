"""Field enums for sales tax datasets.

Provides ``str``-based enums for every Socrata column name exposed by the
sales tax resources. Pass enum members anywhere a raw field-name string is
accepted (e.g. ``sort_by``). Because these enums inherit from ``str``, plain
strings continue to work as before.

Categorical enums (``AuthorityType``, ``SalesTaxRateType``) represent known
valid values for ``for_type()`` filter methods on the corresponding resources.
"""

from ._base import FieldEnum


# ---------------------------------------------------------------------------
# Field enums (one per Socrata-backed resource)
# ---------------------------------------------------------------------------


class ActivePermitField(FieldEnum):
    """Sortable fields for the Active Permits dataset (jrea-zgmq)."""

    TAXPAYER_NUMBER = "taxpayer_number"
    TAXPAYER_NAME = "taxpayer_name"
    TAXPAYER_ADDRESS = "taxpayer_address"
    TAXPAYER_CITY = "taxpayer_city"
    TAXPAYER_STATE = "taxpayer_state"
    TAXPAYER_ZIP_CODE = "taxpayer_zip_code"
    TAXPAYER_COUNTY_CODE = "taxpayer_county_code"
    TAXPAYER_ORGANIZATION_TYPE = "taxpayer_organization_type"
    OUTLET_NUMBER = "outlet_number"
    OUTLET_NAME = "outlet_name"
    OUTLET_ADDRESS = "outlet_address"
    OUTLET_CITY = "outlet_city"
    OUTLET_STATE = "outlet_state"
    OUTLET_ZIP_CODE = "outlet_zip_code"
    OUTLET_COUNTY_CODE = "outlet_county_code"
    OUTLET_NAICS_CODE = "outlet_naics_code"
    OUTLET_INSIDE_OUTSIDE_CITY_LIMITS_INDICATOR = (
        "outlet_inside_outside_city_limits_indicator"
    )
    OUTLET_PERMIT_ISSUE_DATE = "outlet_permit_issue_date"
    OUTLET_FIRST_SALES_DATE = "outlet_first_sales_date"


class PermittedLocationField(FieldEnum):
    """Sortable fields for the Permitted Locations dataset."""

    TP_NUMBER = "tp_number"
    TP_NAME = "tp_name"
    TP_ADDRESS = "tp_address"
    TP_CITY = "tp_city"
    TP_STATE = "tp_state"
    TP_ZIP = "tp_zip"
    TP_COUNTY = "tp_county"
    ORG_TYPE = "org_type"
    LOC_NUMBER = "loc_number"
    LOC_NAME = "loc_name"
    LOC_CITY = "loc_city"
    LOC_STATE = "loc_state"
    LOC_ZIP = "loc_zip"
    LOC_COUNTY = "loc_county"
    NAICS = "naics"
    JURIS_CITY = "juris_city"
    CITY_TAID = "city_taid"
    MASS_TRANSIT_AUTH1_TAID = "mass_transit_auth1_taid"
    MASS_TRANSIT_AUTH2_TAID = "mass_transit_auth2_taid"
    COUNTY_TAID = "county_taid"
    SPECIAL_PURP_DIST1_TAID = "special_purp_dist1_taid"
    SPECIAL_PURP_DIST2_TAID = "special_purp_dist2_taid"
    SPECIAL_PURP_DIST3_TAID = "special_purp_dist3_taid"
    SPECIAL_PURP_DIST4_TAID = "special_purp_dist4_taid"
    UNIQUE_TAID = "unique_taid"
    FIRST_SALE_DATE = "first_sale_date"
    OUT_OF_BUSINESS_DATE = "out_of_business_date"


class SalesTaxRateField(FieldEnum):
    """Sortable fields for the Sales Tax Rates dataset (tmhs-ahbh)."""

    TYPE = "type"
    CITY_NAME = "city_name"
    COUNTY_NAME = "county_name"
    OLD_RATE = "old_rate"
    NEW_RATE = "new_rate"
    EFFECTIVE_DATE = "effective_date"
    REPORT_MONTH = "report_month"
    REPORT_YEAR = "report_year"
    REPORT_PERIOD_TYPE = "report_period_type"


class ComparisonSummaryField(FieldEnum):
    """Sortable fields for the City/County Comparison Summary dataset."""

    COUNTY = "county"
    CITY = "city"
    CURRENT_RATE = "current_rate"
    NET_PAYMENT_THIS_PERIOD = "net_payment_this_period"
    COMPARABLE_PAYMENT_PRIOR_YEAR = "comparable_payment_prior_year"
    PERIOD_PERCENT_CHANGE = "period_percent_change"
    PAYMENTS_TO_DATE = "payments_to_date"
    PREVIOUS_PAYMENTS_TO_DATE = "previous_payments_to_date"
    YEAR_PERCENT_CHANGE = "year_percent_change"
    REPORT_MONTH = "report_month"
    REPORT_YEAR = "report_year"
    REPORT_PERIOD_TYPE = "report_period_type"


class CountySPDMTAAllocationField(FieldEnum):
    """Sortable fields for the County/SPD/MTA Allocations dataset (qsh8-tby8)."""

    NAME = "name"
    TYPE = "type"
    CURRENT_RATE = "current_rate"
    NET_PAYMENT_THIS_PERIOD = "net_payment_this_period"
    PERCENT_CHANGE_PRIOR_YEAR = "percent_change_prior_year"
    REPORT_YEAR = "report_year"
    REPORT_MONTH = "report_month"
    REPORT_PERIOD_TYPE = "report_period_type"
    COMPARABLE_PAYMENT_PRIOR_YEAR = "comparable_payment_prior_year"
    PAYMENTS_TO_DATE = "payments_to_date"
    PREVIOUS_PAYMENTS_TO_DATE = "previous_payments_to_date"
    PERCENT_CHANGE_TO_DATE = "percent_change_to_date"


class SingleLocalAllocationField(FieldEnum):
    """Sortable fields for the Single Local Allocations dataset."""

    AUTHORITY_TYPE = "authority_type"
    TAX_AUTHORITY = "tax_authority"
    REPORT_YEAR = "report_year"
    REPORT_MONTH = "report_month"
    CURRENT_NET_PAYMENT = "current_net_payment"
    PRIOR_YEAR_NET_PAYMENT = "prior_year_net_payment"
    YOY_PERCENT_CHANGE = "yoy_percent_change"
    PAYMENT_YTD = "payment_ytd"
    PRIOR_YEAR_PAYMENT_YTD = "prior_year_payment_ytd"
    YTD_PERCENT_CHANGE = "ytd_percent_change"


class AllocationPaymentDetailField(FieldEnum):
    """Sortable fields for the Local Allocation Payment Detail dataset."""

    AUTHORITY_ID = "authority_id"
    AUTHORITY_NAME = "authority_name"
    ALLOCATION_MONTH = "allocation_month"
    ALLOCATION_DATE = "allocation_date"
    TOTAL_COLLECTIONS = "total_coll"
    PRIOR_COLLECTIONS = "prior_coll"
    CURRENT_COLLECTIONS = "current_coll"
    FUTURE_COLLECTIONS = "future_coll"
    AUDIT_COLLECTIONS = "audit_coll"
    UNIDENTIFIED_COLLECTIONS = "unidentified_coll"
    SINGLE_LOCAL_TAX_COLLECTIONS = "single_local_tax_coll"
    SERVICE_FEE = "service_fee"
    CURRENT_RETAINAGE = "current_retainage"
    PRIOR_RETAINAGE = "prior_retainage"
    NET_PAYMENT = "net_payment"


class MarketplaceProviderAllocationField(FieldEnum):
    """Sortable fields for the Marketplace Provider Allocations dataset (hezn-fbgw)."""

    AUTHORITY_TYPE = "authority_type"
    AUTHORITY_ID = "authority_id"
    AUTHORITY_NAME = "authority_name"
    ALLOCATION_YEAR = "allocation_year"
    ALLOCATION_MONTH = "allocation_month"
    AMOUNT_ALLOCATED = "amount_allocated"


class DirectPayTaxpayerField(FieldEnum):
    """Sortable fields for the Direct Pay Taxpayers dataset."""

    ID = "id"
    NAME = "name"
    ADDRESS = "address"
    CITY = "city"
    STATE = "state"
    ZIP = "zip"
    COUNTY = "county"
    BUSINESS_TYPE = "business_type"
    NAICS_CODE = "naics_code"
    RESPONSIBILITY_BEGIN_DATE = "responsibility_begin_date"


# ---------------------------------------------------------------------------
# Categorical enums
# ---------------------------------------------------------------------------


class AuthorityType(FieldEnum):
    """Known authority/jurisdiction types used by allocation resources.

    Used with ``for_type()`` on :class:`CountySPDMTAAllocations`,
    :class:`SingleLocalAllocations`, and :class:`MarketplaceProviderAllocations`.
    Note that different endpoints may accept different subsets of these values.
    """

    CITY = "CITY"
    COUNTY = "COUNTY"
    SPD = "SPD"
    MTA = "MTA"
    TRANSIT = "TRANSIT"


class SalesTaxRateType(FieldEnum):
    """Known jurisdiction types for the Sales Tax Rates dataset.

    Used with ``for_type()`` on :class:`SalesTaxRates`.
    """

    CITY_LIST = "City List"
    SPD_LIST = "SPD List"
