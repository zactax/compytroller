from datetime import datetime
from typing import List

import httpx
from selectolax.parser import HTMLParser

from src.compytroller.exceptions import HttpError, InvalidRequest
from src.compytroller.responses.sales_tax import AllocationHistoryData


class SalesTaxAllocationHistory:
    """
    Query historical sales tax allocation data via web scraping.

    This class scrapes allocation history from the Texas Comptroller's allocation
    portal (mycpa.cpa.state.tx.us). It retrieves monthly allocation amounts for cities,
    counties, transit authorities, special districts, and statewide categories by parsing
    HTML tables from form-based POST requests.

    Attributes:
        BASE_URL: Base URL for the Comptroller's allocation portal.

    Example:
        >>> resource = SalesTaxAllocationHistory()
        >>> results = resource.for_city("Austin").get()
        >>> for record in results:
        ...     print(record.allocation_month, record.net_payment)
    """
    BASE_URL = "https://mycpa.cpa.state.tx.us/allocation/"

    def __init__(self):
        """
        Initialize the SalesTaxAllocationHistory resource with an HTTP client.
        """
        self.client = httpx.Client(follow_redirects=True)
        self.endpoint = None
        self.params = {}

    def for_city(self, name: str):
        """
        Filter allocation history for a specific city.

        Args:
            name: The city name to query.

        Returns:
            Self for method chaining.
        """
        self.endpoint = "CtyCntyAllocResults"
        self.params = {"cityCountyName": name, "cityCountyOption": "City"}
        return self

    def in_county(self, name: str):
        """
        Filter allocation history for a specific county.

        Args:
            name: The county name to query.

        Returns:
            Self for method chaining.
        """
        self.endpoint = "CtyCntyAllocResults"
        self.params = {"cityCountyName": name, "cityCountyOption": "County"}
        return self

    def for_transit_authority(self, name: str):
        """
        Filter allocation history for a mass transit authority.

        Args:
            name: The transit authority name to query (e.g., "DART", "Metro").

        Returns:
            Self for method chaining.
        """
        self.endpoint = "MCCAllocResults"
        self.params = {"mccOption": "MCC", "mccOptions": name}
        return self

    def for_special_district(self, name: str):
        """
        Filter allocation history for a special purpose district.

        Args:
            name: The special district name to query.

        Returns:
            Self for method chaining.
        """
        self.endpoint = "SPDAllocResults"
        self.params = {"spdOption": "SPD", "spdOptions": name}
        return self

    def statewide(self, statewide_type: str):
        """
        Query statewide allocation data by category.

        Args:
            statewide_type: The statewide category to query.

        Returns:
            Self for method chaining.
        """
        self.endpoint = "StateAllocResults"
        self.params = {"stateOptions": statewide_type}
        return self

    def reset(self):
        """
        Reset all filters and parameters to their default state.

        Returns:
            Self for method chaining.
        """
        self._params = {}
        return self

    def get(self) -> List[AllocationHistoryData]:
        """
        Execute the query and return allocation history records.

        Scrapes and parses allocation data from HTML tables returned by the portal.
        Only returns records with allocation dates on or before today.

        Returns:
            List of AllocationHistoryData objects sorted by allocation month (descending).

        Raises:
            HttpError: If the HTTP request fails.
            InvalidRequest: If no filter method was called or no tables found in response.
        """
        if not self.endpoint:
            raise InvalidRequest("Must call for_city / in_county / for_transit_authority / for_special_district first.")

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

                if record and record.allocation_month <= now.date(): # pragma: no cover
                    results.append(record)

        return sorted(results, key=lambda r: r.allocation_month, reverse=True)
