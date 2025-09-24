from dataclasses import dataclass
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class MixedBeverageGrossReceiptsData:
    permit_number: str
    tp_name : str
    tp_address: str
    tp_city: Optional[str]
    tp_state: Optional[str]
    tp_zip: Optional[str]
    location_name: Optional[str]
    location_address: Optional[str]
    location_city: Optional[str]
    location_state: Optional[str]
    location_zip: Optional[str]
    inside_outside_city_limits: Optional[str]
    responsibility_begin_date: Optional[date]
    responsibility_end_date: Optional[date]
    obligation_start_date: Optional[date]
    obligation_end_date: Optional[date]
    
    beer_receipts: Optional[float]
    wine_receipts: Optional[float]
    liquor_receipts: Optional[float]
    cover_charge_receipts: Optional[float]
    total_receipts: Optional[float]
    num_outlets: Optional[int]     # if included
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        def f(x):
            try: return float(x)
            except: return None
        def i(x):
            try: return int(x)
            except: return None
        def d(x):
            if not x:
                return None
            for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%f"):
                try:
                    return datetime.strptime(x, fmt).date()
                except (ValueError, TypeError):
                    continue
            return None


        return cls(
            permit_number=data.get("permit_number"),
            tp_name=data.get("taxpayer_name"),
            tp_address=data.get("taxpayer_address"),
            tp_city=data.get("taxpayer_city"),
            tp_state=data.get("taxpayer_state"),
            tp_zip=data.get("taxpayer_zip"),
            location_name=data.get("location_name"),
            location_address=data.get("location_address"),
            location_city=data.get("location_city"),
            location_state=data.get("location_state"),
            location_zip=data.get("location_zip"),
            inside_outside_city_limits=data.get("inside_outside_city_limits_code_y_n"),
            responsibility_begin_date=d(data.get("responsibility_begin_date_yyyymmdd")),
            responsibility_end_date=d(data.get("responsibility_end_date_yyyymmdd")),
            obligation_start_date=d(data.get("obligation_start_date_yyyymmdd")),
            obligation_end_date=d(data.get("obligation_end_date_yyyymmdd")),
            beer_receipts=f(data.get("beer_receipts")),
            wine_receipts=f(data.get("wine_receipts")),
            liquor_receipts=f(data.get("liquor_receipts")),
            cover_charge_receipts=f(data.get("cover_charge_receipts")),
            total_receipts=f(data.get("total_receipts")),
            num_outlets=i(data.get("num_outlets")) if "num_outlets" in data else None,
        )

@dataclass
class MixedBeverageHistoryData:
    jurisdiction_name: str        # e.g. "Austin"
    jurisdiction_type: str        # "City" / "County"
    summary_type: str             # "Total Taxes", "Gross Receipts", etc.
    allocation_month: date        # normalized to first of the month
    net_payment: Optional[float]  