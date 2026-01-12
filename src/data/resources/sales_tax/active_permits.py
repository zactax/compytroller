import httpx
from typing import List
from src.data.responses.sales_tax import ActivePermitData
from src.data.exceptions import HttpError, InvalidRequest


class ActivePermits:
    DATASET_ID = "jrea-zgmq"

    def __init__(self, socrata_client):
        self.client = socrata_client
        self._params = {}
        self._where_clauses = []

    def for_taxpayer(self, number):
        self._params["taxpayer_number"] = str(number)
        return self

    def in_city(self, city: str):
        self._params["outlet_city"] = city.upper()
        return self

    def in_county(self, county_code: str):
        """
        County codes can be found here:
        https://comptroller.texas.gov/taxes/resources/county-codes.php
        """
        self._params["outlet_county_code"] = county_code
        return self

    def with_naics(self, code):
        self._params["outlet_naics_code"] = str(code)
        return self

    def issued_after(self, date: str):
        self._where_clauses.append(f"outlet_permit_issue_date > '{date}'")
        return self

    def first_sale_after(self, date: str):
        self._where_clauses.append(f"outlet_first_sales_date > '{date}'")
        return self

    def between_issue_dates(self, start: str, end: str):
        self._where_clauses.append(
            f"outlet_permit_issue_date BETWEEN '{start}' AND '{end}'"
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

    def get(self) -> List[ActivePermitData]:
        if self._where_clauses:
            self._params["$where"] = " AND ".join(self._where_clauses)

        try:
            records = self.client.get(self.DATASET_ID, self._params)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest("No records returned from Active Permits dataset")

        return [ActivePermitData.from_dict(r) for r in records]