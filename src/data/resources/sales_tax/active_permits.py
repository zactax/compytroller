from typing import List
from data.responses.sales_tax import ActivePermitData

class ActivePermits:
    DATASET_ID = "jrea-zgmq"

    def __init__(self, socrata_client):
        self.client = socrata_client
        self._params = {}
        self._where_clauses = []

    def for_taxpayer(self, number: str):
        self._params["taxpayer_number"] = number
        return self

    def in_city(self, city: str):
        self._params["outlet_city"] = city
        return self

    def in_county(self, county_code: str):
        self._params["outlet_county_code"] = county_code
        return self

    def with_naics(self, code: str):
        self._params["outlet_naics_code"] = code
        return self

    def issued_after(self, date: str):
        self._where_clauses.append(f"outlet_permit_issue_date > '{date}'")
        return self

    def first_sale_after(self, date: str):
        self._where_clauses.append(f"outlet_first_sales_date > '{date}'")
        return self

    def between_issue_dates(self, start: str, end: str):
        """
        Filter outlets whose permit issue date is between two dates.
        Dates should be in 'YYYY-MM-DD' format.
        """
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

    def get(self) -> List[ActivePermitData]:
        if self._where_clauses:
            self._params["$where"] = " AND ".join(self._where_clauses)
        records = self.client.get(self.DATASET_ID, self._params)
        return [ActivePermitData.from_dict(r) for r in records]