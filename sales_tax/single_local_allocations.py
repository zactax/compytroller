from typing import List
from compytroller.responses.sales_tax import SingleLocalAllocationData


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

    def get(self):
        records = self.client.get(self.DATASET_ID, self._params)
        return [SingleLocalAllocationData.from_dict(r) for r in records]
