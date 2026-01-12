from src.data.responses.mixed_beverage_tax import MixedBeverageGrossReceiptsData
import httpx
import pandas as pd
from io import StringIO
from datetime import datetime
from src.data.exceptions import HttpError, InvalidRequest
from src.data.utils import parse_date
from typing import List, Optional, Union
from datetime import date

class MixedBeverageGrossReceipts:
    DATASET_ID = "naix-2893"

    def __init__(self, socrata_client):
        self.client = socrata_client
        self._params = {}
        self._where_clauses = []
        
    def for_taxpayer(self, number):
        self._params["taxpayer_number"] = str(number)
        return self

    def taxpayer_in_city(self, city: str):
        self._params["taxpayer_city"] = city.upper()
        return self
    
    def for_location(self, name):
        self._params["location_name"] = str(name).upper()
        return self
    
    def location_in_city(self, city: str):
        self._params["location_city"] = city.upper()
        return self
    
    def location_inside_city_limits(self, inside: bool = True):
        self._params["inside_outside_city_limits_code_y_n"] = "Y" if inside else "N"
        return self

    def with_location_number(self, location_number):
        self._params["location_number"] = str(location_number)
        return self
    
    def with_tabc_permit(self, tabc_permit: str):
        self._params["tabc_permit_number"] = tabc_permit
        return self

    def responsibility_start_after(self, date: str):
        self._where_clauses.append(f"responsibility_begin_date_yyyymmdd > '{date}'")
        return self
    
    def responsibility_start_before(self, date: str):
        self._where_clauses.append(f"responsibility_begin_date_yyyymmdd < '{date}'")
        return self

    def responsibility_between_dates(self, start: str, end: str):
        self._where_clauses.append(
            f"responsibility_begin_date_yyyymmdd BETWEEN '{start}' AND '{end}'"
        )
        return self

    def sort_by(self, field: str, desc: bool = False):
        self._params["$order"] = f"{field} DESC" if desc else field
        return self

    def limit(self, n: int):
        self._params["$limit"] = n
        return self
    
    def reset(self):
        self._params = {}
        self._where_clauses = []
        return self

    def get(self) -> List[MixedBeverageGrossReceiptsData]:
        if self._where_clauses:
            self._params["$where"] = " AND ".join(self._where_clauses)
        try:
            records = self.client.get(self.DATASET_ID, self._params)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest("No records returned from Mixed Beverage Gross Receipts dataset")

        return [MixedBeverageGrossReceiptsData.from_dict(r) for r in records]