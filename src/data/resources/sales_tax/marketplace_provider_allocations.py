from typing import List
from src.data.responses.sales_tax import MarketplaceProviderAllocationData
import httpx
from src.data.exceptions import HttpError, InvalidRequest


class MarketplaceProviderAllocations:
    DATASET_ID = "hezn-fbgw"

    def __init__(self, socrata_client):
        self.client = socrata_client
        self._params = {}
        self.authority_name = []

    def for_authority(self, name: str):
        """Filter by authority name (case-sensitive, e.g., may be both 'Houston' and "HOUSTON")."""
        self.authority_name.append(name)
        self.authority_name.append(name.upper())
        return self

    def for_type(self, authority_type: str):
        """Filter by authority type: CITY, COUNTY, etc."""
        self._params["authority_type"] = authority_type
        return self

    def for_year(self, year: int):
        """Filter by allocation year."""
        self._params["allocation_year"] = year
        return self

    def sort_by(self, field: str, desc: bool = False):
        self._params["$order"] = f"{field} DESC" if desc else field
        return self

    def limit(self, n: int):
        self._params["$limit"] = n
        return self
    
    def reset(self):
        self._params = {}
        self.authority_name = []
        return self

    def get(self) -> List["MarketplaceProviderAllocationData"]:
        records = []
        try:
            if self.authority_name:
                for name in self.authority_name:
                    self._params["authority_name"] = name
                    cur_records = self.client.get(self.DATASET_ID, self._params)
                    records.extend([MarketplaceProviderAllocationData.from_dict(r) for r in cur_records])
            else:
                records = self.client.get(self.DATASET_ID, self._params)
                records = [MarketplaceProviderAllocationData.from_dict(r) for r in records]
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest("No records returned from Marketplace Provider Allocations dataset")
        return records
        