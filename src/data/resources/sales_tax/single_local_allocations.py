from typing import List
from data.responses.sales_tax import SingleLocalAllocationData
import httpx
from data.exceptions import HttpError, InvalidRequest


class SingleLocalAllocations:
    DATASET_ID = "5yx2-afcg"

    def __init__(self, socrata_client):
        self.client = socrata_client
        self._params = {}

    def for_authority(self, name: str):
        """Filter by tax authority name (case-sensitive, e.g., 'Houston')."""
        self._params["tax_authority"] = name
        return self

    def for_type(self, authority_type: str):
        """Filter by authority type: CITY, COUNTY, etc."""
        self._params["authority_type"] = authority_type.upper()
        return self

    def for_year(self, year: int):
        """Filter by reporting year."""
        self._params["report_year"] = year
        return self

    def sort_by(self, field: str, desc: bool = False):
        self._params["$order"] = f"{field} DESC" if desc else field
        return self

    def limit(self, n: int):
        self._params["$limit"] = n
        return self

    def get(self) -> List[SingleLocalAllocationData]:
        try:
            records = self.client.get(self.DATASET_ID, self._params)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest("No records returned from Single Local Allocations dataset")

        return [SingleLocalAllocationData.from_dict(r) for r in records]