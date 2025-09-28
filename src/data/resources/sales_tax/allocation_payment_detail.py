# compytroller/sales_tax/allocations.py
from typing import List
from data.responses.sales_tax import LocalAllocationPaymentDetailsData


class LocalAllocationPaymentDetail:
    DATASET_ID = "3p4v-vsr3"

    def __init__(self, socrata_client):
        self.client = socrata_client
        self._params = {}

    def where(self, key: str, value):
        """Filter by field = value."""
        self._params[key] = value
        return self

    def sort_by(self, field: str, desc: bool = False):
        """Sort by a field, optionally descending."""
        self._params["$order"] = f"{field} DESC" if desc else field
        return self

    def limit(self, n: int):
        """Limit the number of results."""
        self._params["$limit"] = n
        return self

    def get(self) -> List[LocalAllocationPaymentDetailsData]:
        """Fetch rows and map into DTOs."""
        records = self.client.get(self.DATASET_ID, self._params)
        return [LocalAllocationPaymentDetailsData.from_dict(r) for r in records]