from typing import List
from compytroller.responses.sales_tax import PermittedLocationData

class PermittedLocations:
    DATASET_ID = "3kx8-uryv"

    def __init__(self, socrata_client):
        self.client = socrata_client
        self._params = {}

    def in_city(self, city: str):
        self._params["loc_city"] = city.upper()
        return self

    def in_county(self, county: str):
        self._params["loc_county"] = county.upper()
        return self

    def with_naics_code(self, code: str):
        self._params["naics"] = str(code)
        return self

    def with_tp_number(self, tp_number: str):
        self._params["tp_number"] = tp_number
        return self

    def with_city_taid(self, taid: str):
        self._params["city_taid"] = taid
        return self

    def with_county_taid(self, taid: str):
        self._params["county_taid"] = taid
        return self

    def with_mta_taid(self, taid: str, slot: int = 1):
        """slot = 1 or 2"""
        self._params[f"mass_transit_auth{slot}_taid"] = taid
        return self

    def with_spd_taid(self, taid: str, slot: int = 1):
        """slot = 1–4"""
        self._params[f"special_purp_dist{slot}_taid"] = taid
        return self

    def sort_by(self, field: str, desc: bool = False):
        self._params["$order"] = f"{field} DESC" if desc else field
        return self

    def limit(self, n: int):
        self._params["$limit"] = n
        return self

    def get(self) -> List[PermittedLocationData]:
        records = self.client.get(self.DATASET_ID, self._params)
        return [PermittedLocationData.from_dict(r) for r in records]