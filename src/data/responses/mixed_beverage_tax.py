from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import date
from src.data.utils import parse_date, parse_float, parse_int

@dataclass
class MixedBeverageGrossReceiptsData:
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
    jurisdiction_name: str
    jurisdiction_type: str
    summary_type: str
    allocation_month: date
    net_payment: Optional[float]
