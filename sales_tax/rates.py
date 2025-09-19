from typing import List
from compytroller.responses.sales_tax import SalesTaxRateData

class SalesTaxRates:
    DATASET_ID = "tmhs-ahbh"

    def __init__(self, socrata_client):
        self.client = socrata_client
        self._params = {}

    def for_city(self, city: str):
        self._params["city_name"] = city
        return self

    def for_county(self, county: str):
        self._params["county_name"] = county
        return self

    def for_type(self, jurisdiction_type: str):
        self._params["type"] = jurisdiction_type
        return self

    def for_year(self, year: int):
        self._params["report_year"] = year
        return self

    def sort_by(self, field: str, desc: bool = False):
        self._params["$order"] = f"{field} DESC" if desc else field
        return self

    def limit(self, n: int):
        self._params["$limit"] = n
        return self

    def get(self) -> List[SalesTaxRateData]:
        records = self.client.get(self.DATASET_ID, self._params)
        return [SalesTaxRateData.from_dict(r) for r in records]