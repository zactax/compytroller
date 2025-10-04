import httpx
from typing import List
from data.responses.sales_tax import LocalAllocationPaymentDetailsData
from data.exceptions import HttpError, InvalidRequest


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
        try:
            records = self.client.get(self.DATASET_ID, self._params)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest("No records returned from Local Allocation Payment Detail dataset")

        return [LocalAllocationPaymentDetailsData.from_dict(r) for r in records]
