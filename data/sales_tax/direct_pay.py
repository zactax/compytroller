from typing import List
from data.responses.sales_tax import DirectPayTaxpayerData

class DirectPayTaxpayers:
    DATASET_ID = "deed-e7u6"

    def __init__(self, socrata_client):
        self.client = socrata_client
        self._params = {}

    def with_naics(self, code: str):
        self._params["naics_code"] = code
        return self

    def in_county(self, county: str):
        self._params["county"] = county.upper()
        return self

    def in_city(self, city: str):
        self._params["city"] = city.upper()
        return self

    def sort_by(self, field: str, desc: bool = False):
        self._params["$order"] = f"{field} DESC" if desc else field
        return self

    def limit(self, n: int):
        self._params["$limit"] = n
        return self

    def get(self) -> List[DirectPayTaxpayerData]:
        records = self.client.get(self.DATASET_ID, self._params)
        return [DirectPayTaxpayerData.from_dict(r) for r in records]
