from typing import List
from src.data.responses.sales_tax import SalesTaxRateData
import httpx
from src.data.exceptions import HttpError, InvalidRequest


class SalesTaxRates:
    DATASET_ID = "tmhs-ahbh"

    def __init__(self, socrata_client):
        self.client = socrata_client
        self._params = {}

    def for_city(self, city: str):
        self._params["city_name"] = city
        return self

    def for_county(self, county: str):
        self._params["county_name"] = county
        return self

    def for_type(self, jurisdiction_type: str):
        """
        SPD List, City List
        """
        self._params["type"] = jurisdiction_type
        return self

    def for_year(self, year: int):
        self._params["report_year"] = year
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

    def get(self) -> List["SalesTaxRateData"]:
        try:
            records = self.client.get(self.DATASET_ID, self._params)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest("No records returned from Sales Tax Rates dataset")

        return [SalesTaxRateData.from_dict(r) for r in records]