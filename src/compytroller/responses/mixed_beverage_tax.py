from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import date
from src.compytroller.utils import parse_date, parse_float, parse_int

@dataclass
class MixedBeverageGrossReceiptsData:
    """Mixed beverage gross receipts data for taxpayers and their locations.

    Represents detailed gross receipts information for businesses that hold
    Texas Alcoholic Beverage Commission (TABC) permits and are subject to
    mixed beverage tax. This includes taxpayer information, location details,
    and breakdown of receipts by beverage type.

    Attributes:
        tp_name: Legal name of the taxpayer.
        tp_address: Taxpayer's mailing address.
        tp_city: Taxpayer's city.
        tp_state: Taxpayer's state.
        tp_zip: Taxpayer's ZIP code.
        tp_county: Taxpayer's county.
        location_number: Unique number identifying the business location.
        location_name: Name of the business location.
        location_address: Physical address of the business location.
        location_city: City where the business location is situated.
        location_state: State where the business location is situated.
        location_zip: ZIP code of the business location.
        location_county: County where the business location is situated.
        inside_outside_city_limits: Indicator for whether location is inside ("Y") or outside ("N") city limits.
        responsibility_begin_date: Date when mixed beverage tax responsibility began.
        responsibility_end_date: Date when mixed beverage tax responsibility ended (None if still active).
        obligation_end_date: Date when tax obligation ended.
        beer_receipts: Gross receipts from beer sales.
        wine_receipts: Gross receipts from wine sales.
        liquor_receipts: Gross receipts from liquor/spirits sales.
        cover_charge_receipts: Gross receipts from cover charges.
        total_receipts: Total gross receipts from all mixed beverage sales.
        tabc_permit_number: Texas Alcoholic Beverage Commission permit number.
    """
    tp_name: str
    tp_address: str
    tp_city: Optional[str]
    tp_state: Optional[str]
    tp_zip: Optional[str]
    tp_county: Optional[str]
    location_number: Optional[int]
    location_name: Optional[str]
    location_address: Optional[str]
    location_city: Optional[str]
    location_state: Optional[str]
    location_zip: Optional[str]
    location_county: Optional[str]
    inside_outside_city_limits: Optional[str]
    responsibility_begin_date: Optional[date]
    responsibility_end_date: Optional[date]
    obligation_end_date: Optional[date]
    beer_receipts: Optional[float]
    wine_receipts: Optional[float]
    liquor_receipts: Optional[float]
    cover_charge_receipts: Optional[float]
    total_receipts: Optional[float]
    tabc_permit_number: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create instance from a dictionary.

        Parses a dictionary (typically from JSON API response) and constructs
        a MixedBeverageGrossReceiptsData instance with properly typed fields.
        Field names in the source data use verbose naming conventions (e.g.,
        "responsibility_begin_date_yyyymmdd") which are mapped to simpler attribute names.

        Args:
            data: Dictionary containing the raw data from the API response.

        Returns:
            A new MixedBeverageGrossReceiptsData instance with parsed and typed data.
        """
        return cls(
            tp_name=data.get("taxpayer_name"),
            tp_address=data.get("taxpayer_address"),
            tp_city=data.get("taxpayer_city"),
            tp_state=data.get("taxpayer_state"),
            tp_zip=data.get("taxpayer_zip"),
            tp_county=data.get("taxpayer_county"),
            location_number =data.get("location_number"),
            location_name=data.get("location_name"),
            location_address=data.get("location_address"),
            location_city=data.get("location_city"),
            location_state=data.get("location_state"),
            location_zip=data.get("location_zip"),
            location_county = data.get("location_county"),
            inside_outside_city_limits=data.get("inside_outside_city_limits_code_y_n"),
            responsibility_begin_date=parse_date(data.get("responsibility_begin_date_yyyymmdd")),
            responsibility_end_date=parse_date(data.get("responsibility_end_date_yyyymmdd")),
            obligation_end_date=parse_date(data.get("obligation_end_date_yyyymmdd")),
            beer_receipts=parse_float(data.get("beer_receipts")),
            wine_receipts=parse_float(data.get("wine_receipts")),
            liquor_receipts=parse_float(data.get("liquor_receipts")),
            cover_charge_receipts=parse_float(data.get("cover_charge_receipts")),
            total_receipts=parse_float(data.get("total_receipts")),
            tabc_permit_number=data.get("tabc_permit_number")
        )

@dataclass
class MixedBeverageHistoryData:
    """Historical mixed beverage tax allocation data for jurisdictions.

    Represents historical allocation payment data for mixed beverage taxes
    distributed to Texas jurisdictions. This data tracks monthly tax allocations
    derived from mixed beverage gross receipts, providing time-series information
    for revenue analysis.

    Attributes:
        jurisdiction_name: Name of the jurisdiction receiving the allocation.
        jurisdiction_type: Type of jurisdiction (e.g., "City", "County").
        summary_type: Type of summary or aggregation (e.g., "Total", "Detail").
        allocation_month: The month for which the allocation is made.
        net_payment: Net payment amount allocated to the jurisdiction for the period.
    """
    jurisdiction_name: str
    jurisdiction_type: str
    summary_type: str
    allocation_month: date
    net_payment: Optional[float]
