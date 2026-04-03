from typing import List

import httpx

from src.compytroller.exceptions import HttpError, InvalidRequest
from src.compytroller.responses.sales_tax import ActivePermitData
from src.compytroller.fields import ActivePermitField


class ActivePermits:
    """
    Query active sales tax permits from the Texas Comptroller.

    This class provides access to the Active Sales Tax Permits dataset via the Socrata API,
    containing information about businesses with active sales tax permits in Texas. The data
    includes taxpayer details, outlet locations, permit issue dates, and NAICS codes.

    Attributes:
        DATASET_ID: Socrata dataset identifier (jrea-zgmq) for active permits.

    Example:
        >>> resource = ActivePermits(client)
        >>> results = resource.for_city("Austin").with_naics("722511").limit(10).get()
        >>> for permit in results:
        ...     print(permit.taxpayer_number, permit.outlet_city)
    """
    DATASET_ID = "jrea-zgmq"

    def __init__(self, socrata_client):
        """
        Initialize the ActivePermits resource.

        Args:
            socrata_client: An instance of SocrataClient for API requests.
        """
        self.client = socrata_client
        self._params = {}
        self._where_clauses = []

    def for_taxpayer(self, number):
        """
        Filter permits by taxpayer number.

        Args:
            number: The taxpayer number to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["taxpayer_number"] = str(number)
        return self

    def for_city(self, city: str):
        """
        Filter permits by outlet city name.

        Args:
            city: The city name to filter by (case-insensitive).

        Returns:
            Self for method chaining.
        """
        self._params["outlet_city"] = city.upper()
        return self

    def in_county(self, county_code: str):
        """
        Filter permits by county code.

        County codes are 3-digit numeric codes identifying Texas counties.

        Args:
            county_code: The county code to filter by. Available at:
                https://comptroller.texas.gov/taxes/resources/county-codes.php

        Returns:
            Self for method chaining.
        """
        self._params["outlet_county_code"] = county_code
        return self

    def with_naics(self, code):
        """
        Filter permits by NAICS industry code.

        Args:
            code: The NAICS code to filter by (e.g., "722511" for full-service restaurants).

        Returns:
            Self for method chaining.
        """
        self._params["outlet_naics_code"] = str(code)
        return self

    def issued_after(self, date: str):
        """
        Filter permits issued after a specific date.

        Args:
            date: The cutoff date in ISO format (YYYY-MM-DD).

        Returns:
            Self for method chaining.
        """
        self._where_clauses.append(f"outlet_permit_issue_date > '{date}'")
        return self

    def first_sale_after(self, date: str):
        """
        Filter permits where first sale occurred after a specific date.

        Args:
            date: The cutoff date in ISO format (YYYY-MM-DD).

        Returns:
            Self for method chaining.
        """
        self._where_clauses.append(f"outlet_first_sales_date > '{date}'")
        return self

    def between_issue_dates(self, start: str, end: str):
        """
        Filter permits issued within a date range.

        Args:
            start: The start date in ISO format (YYYY-MM-DD).
            end: The end date in ISO format (YYYY-MM-DD).

        Returns:
            Self for method chaining.
        """
        self._where_clauses.append(
            f"outlet_permit_issue_date BETWEEN '{start}' AND '{end}'"
        )
        return self

    def sort_by(self, field: str | ActivePermitField, desc: bool = False):
        """
        Sort results by a specific field.

        Args:
            field: The field name to sort by.
            desc: If True, sort in descending order. Defaults to False (ascending).

        Returns:
            Self for method chaining.
        """
        self._params["$order"] = f"{field} DESC" if desc else field
        return self

    def limit(self, n: int):
        """
        Limit the number of results returned.

        Args:
            n: Maximum number of results to return.

        Returns:
            Self for method chaining.
        """
        self._params["$limit"] = n
        return self

    def reset(self):
        """
        Reset all filters and parameters to their default state.

        Returns:
            Self for method chaining.
        """
        self._params = {}
        self._where_clauses = []
        return self

    def get(self) -> List[ActivePermitData]:
        """
        Execute the query and return matching active permit records.

        Returns:
            List of ActivePermitData objects matching the query filters.

        Raises:
            HttpError: If the HTTP request to the Socrata API fails.
            InvalidRequest: If no records match the query parameters.
        """
        if self._where_clauses:
            self._params["$where"] = " AND ".join(self._where_clauses)

        try:
            records = self.client.get(self.DATASET_ID, self._params)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest(f"No records returned from {self.__class__.__name__}")

        return [ActivePermitData.from_dict(r) for r in records]