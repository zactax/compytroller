"""Field enums for mixed beverage tax datasets.

Provides ``str``-based enums for Socrata column names exposed by the
mixed beverage tax resources.
"""

from ._base import FieldEnum


class MixedBeverageGrossReceiptsField(FieldEnum):
    """Sortable fields for the Mixed Beverage Gross Receipts dataset."""

    TAXPAYER_NAME = "taxpayer_name"
    TAXPAYER_ADDRESS = "taxpayer_address"
    TAXPAYER_CITY = "taxpayer_city"
    TAXPAYER_STATE = "taxpayer_state"
    TAXPAYER_ZIP = "taxpayer_zip"
    TAXPAYER_COUNTY = "taxpayer_county"
    LOCATION_NUMBER = "location_number"
    LOCATION_NAME = "location_name"
    LOCATION_ADDRESS = "location_address"
    LOCATION_CITY = "location_city"
    LOCATION_STATE = "location_state"
    LOCATION_ZIP = "location_zip"
    LOCATION_COUNTY = "location_county"
    INSIDE_OUTSIDE_CITY_LIMITS = "inside_outside_city_limits_code_y_n"
    RESPONSIBILITY_BEGIN_DATE = "responsibility_begin_date_yyyymmdd"
    RESPONSIBILITY_END_DATE = "responsibility_end_date_yyyymmdd"
    OBLIGATION_END_DATE = "obligation_end_date_yyyymmdd"
    BEER_RECEIPTS = "beer_receipts"
    WINE_RECEIPTS = "wine_receipts"
    LIQUOR_RECEIPTS = "liquor_receipts"
    COVER_CHARGE_RECEIPTS = "cover_charge_receipts"
    TOTAL_RECEIPTS = "total_receipts"
    TABC_PERMIT_NUMBER = "tabc_permit_number"
