import httpx
from selectolax.parser import HTMLParser
from datetime import datetime
from typing import List
from src.data.responses.sales_tax import AllocationHistoryData
from src.data.exceptions import HttpError, InvalidRequest


class SalesTaxAllocationHistory:
    BASE_URL = "https://mycpa.cpa.state.tx.us/allocation/"

    def __init__(self):
        self.client = httpx.Client(follow_redirects=True)
        self.endpoint = None
        self.params = {}

    def for_city(self, name: str):
        self.endpoint = "CtyCntyAllocResults"
        self.params = {"cityCountyName": name, "cityCountyOption": "City"}
        return self

    def for_county(self, name: str):
        self.endpoint = "CtyCntyAllocResults"
        self.params = {"cityCountyName": name, "cityCountyOption": "County"}
        return self

    def for_transit_authority(self, name: str):
        self.endpoint = "MCCAllocResults"
        self.params = {"mccOption": "MCC", "mccOptions": name}
        return self

    def for_special_district(self, name: str):
        self.endpoint = "SPDAllocResults"
        self.params = {"spdOption": "SPD", "spdOptions": name}
        return self
    
    def statewide(self, statewide_type: str):
        self.endpoint = "StateAllocResults"
        self.params = {"stateOptions": statewide_type}
        return self
    
    def reset(self):
        self._params = {}
        return self

    def get(self) -> List[AllocationHistoryData]:
        if not self.endpoint:
            raise InvalidRequest("Must call for_city / for_county / for_transit_authority / for_special_district first.")

        url = f"{self.BASE_URL}{self.endpoint}"

        try:
            resp = self.client.post(url, data=self.params)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        parser = HTMLParser(resp.text)
        tables = parser.css("table.resultsTable")
        if not tables:
            raise InvalidRequest("No results tables found in response.")

        now = datetime.today()
        results: List[AllocationHistoryData] = []

        for table in tables:
            year_text = table.css_first("thead span").text(strip=True)

            for row in table.css("tbody tr"):
                cols = [c.text(strip=True) for c in row.css("td")]
                if not cols or "TOTAL" in cols[0].upper():
                    continue

                record = AllocationHistoryData.from_row(
                    cols,
                    year_text,
                    authority_id=(
                        self.params.get("cityCountyName")
                        or self.params.get("mccOptions")
                        or self.params.get("spdOptions")
                    ),
                    authority_name=(
                        self.params.get("cityCountyOption")
                        or self.params.get("mccOption")
                        or self.params.get("spdOption")
                    ),
                )

                if record and record.allocation_month <= now.date():
                    results.append(record)

        return sorted(results, key=lambda r: r.allocation_month, reverse=True)
