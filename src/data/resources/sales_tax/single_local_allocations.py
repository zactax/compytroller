from typing import List
from src.data.responses.sales_tax import SingleLocalAllocationData
import httpx
from src.data.exceptions import HttpError, InvalidRequest


class SingleLocalAllocations:
    DATASET_ID = "5yx2-afcg"

    def __init__(self, socrata_client):
        self.client = socrata_client
        self._params = {}
    
    def for_city(self, city: str):
        self._params["tax_authority"] = city
        self._params["authority_type"] = "CITY"
        return self
        
    def for_county(self, county: str):
        self._params["tax_authority"] = county
        self._params["authority_type"] = "COUNTY"
        return self
    
    def for_spd(self, spd_name: str):
        """Filter by special purpose district name."""
        self._params["tax_authority"] = spd_name
        self._params["authority_type"] = "SPD"
        return self
    
    def for_mta(self, mta_name: str):
        """Filter by mass transit authority name."""
        self._params["tax_authority"] = mta_name
        self._params["authority_type"] = "MTA"
        return self
    
    def for_year(self, year: int):
        """Filter by reporting year."""
        self._params["report_year"] = year
        return self
    
    def for_month(self, month: int):
        """Filter by reporting month (1-12)."""
        if month < 1 or month > 12:
            raise InvalidRequest("Month must be between 1 and 12")
        self._params["report_month"] = month
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
    
    def get(self) -> List[SingleLocalAllocationData]:
        try:
            records = self.client.get(self.DATASET_ID, self._params)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest("No records returned from Single Local Allocations dataset")

        print([SingleLocalAllocationData.from_dict(r) for r in records][0])
        return [SingleLocalAllocationData.from_dict(r) for r in records]
    
    def get_all(self) -> List[SingleLocalAllocationData]:
        """Get all records without filtering (use with caution)."""
        try:
            records = self.client.get(self.DATASET_ID)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest("No records returned from Single Local Allocations dataset")

        return [SingleLocalAllocationData.from_dict(r) for r in records]