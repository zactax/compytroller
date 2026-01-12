import httpx
from typing import List
from src.data.responses.sales_tax import ComparisonSummaryData
from src.data.exceptions import HttpError, InvalidRequest


class CityCountyComparisonSummary:
    DATASET_ID = "53pa-m7sm"
    
    def __init__(self, socrata_client):
        self.client = socrata_client
        self._params = {}

    def for_city(self, name: str):
        self._params["city"] = name
        return self

    def for_county(self, name: str):
        self._params["county"] = name
        return self

    def sort_by(self, field: str, desc: bool = False):
        self._params["$order"] = f"{field} DESC" if desc else field
        return self

    def limit(self, n: int):
        self._params["$limit"] = n
        return self
    
    def reset(self):
        self._params = {}
        return self

    def get(self) -> List[ComparisonSummaryData]:
        try:
            records = self.client.get(self.DATASET_ID, params=self._params)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest("No records returned from Comparison Summary dataset")

        return [ComparisonSummaryData.from_dict(r) for r in records]
