from typing import List
from data.responses.sales_tax import ComparisonSummaryData

class ComparisonSummary:
    DATASETS = {
        "city_county": {"id": "53pa-m7sm", "key": "city"},   # or county+city
        "cities": {"id": "vfba-b57j", "key": "city"},
        "county_mta_spd": {"id": "qsh8-tby8", "key": "name"},
    }


    def __init__(self, socrata_client, summary_type: str):
        config = self.DATASETS.get(summary_type)
        if not config:
            raise ValueError(f"Unknown comparison summary type: {summary_type}")
        self.client = socrata_client
        self.dataset_id = config["id"]
        self.key_field = config["key"]
        self._params = {}

    def for_city(self, name: str):
        self._params[self.key_field] = name
        return self

    def for_county(self, name: str):
        self._params["county"] = name
        return self

    def for_type(self, type_: str):
        self._params["type"] = type_.upper()  # "COUNTY", "MTA", or "SPD"
        return self

    def where(self, key: str, value):
        self._params[key] = value
        return self

    def sort_by(self, field: str, desc: bool = False):
        self._params["$order"] = f"{field} DESC" if desc else field
        return self

    def limit(self, n: int):
        self._params["$limit"] = n
        return self

    def get(self) -> List[ComparisonSummaryData]:
        records = self.client.get(self.dataset_id, self._params)
        return [ComparisonSummaryData.from_dict(r) for r in records]