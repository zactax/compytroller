import httpx
from typing import List
from src.data.responses.sales_tax import LocalAllocationPaymentDetailsData
from src.data.exceptions import HttpError, InvalidRequest


class LocalAllocationPaymentDetail:
    DATASET_ID = "3p4v-vsr3"

    def __init__(self, socrata_client):
        self.client = socrata_client
        self._params = {}
        
    def for_city(self, city: str):
        """Filter by city."""
        self._params["authority_name"] = f"'{city.upper()}'"
        return self
    
    def with_authority_id(self, authority_id: str):
        """Filter by authority ID."""
        self._params["authority_id"] = f"'{authority_id}'"
        return self
        
    def for_month(self, month: str):
        """Filter by month (floating timestamp)"""
        self._params["allocation_month"] = f"'{month}'"
        return self

    def sort_by(self, field: str, desc: bool = False):
        """Sort by a field, optionally descending."""
        self._params["$order"] = f"{field} DESC" if desc else field
        return self

    def limit(self, n: int):
        """Limit the number of results."""
        self._params["$limit"] = n
        return self
    
    def reset(self):
        self._params = {}
        return self

    def get(self) -> List[LocalAllocationPaymentDetailsData]:
        """Fetch rows and map into DTOs."""
        try:
            records = self.client.get(self.DATASET_ID, self._params)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest("No records returned from Local Allocation Payment Detail dataset")

        return [LocalAllocationPaymentDetailsData.from_dict(r) for r in records]
