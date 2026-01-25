from typing import List

import httpx

from src.data.exceptions import HttpError, InvalidRequest
from src.data.responses.sales_tax import SingleLocalAllocationData


class SingleLocalAllocations:
    """
    Query single local sales tax allocations in Texas.

    This class provides access to the Single Local Allocations dataset via the Socrata API.
    It contains monthly allocation data for single local taxing jurisdictions including cities,
    counties, special purpose districts (SPDs), and mass transit authorities (MTAs).

    Attributes:
        DATASET_ID: Socrata dataset identifier (5yx2-afcg) for single local allocations.

    Example:
        >>> resource = SingleLocalAllocations(client)
        >>> results = resource.for_city("Austin").for_year(2023).for_month(6).get()
        >>> for record in results:
        ...     print(record.tax_authority, record.report_year, record.allocation_amount)
    """
    DATASET_ID = "5yx2-afcg"

    def __init__(self, socrata_client):
        """
        Initialize the SingleLocalAllocations resource.

        Args:
            socrata_client: An instance of SocrataClient for API requests.
        """
        self.client = socrata_client
        self._params = {}

    def for_city(self, city: str):
        """
        Filter allocations for a specific city.

        Args:
            city: The city name to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["tax_authority"] = city
        self._params["authority_type"] = "CITY"
        return self

    def in_county(self, county: str):
        """
        Filter allocations for a specific county.

        Args:
            county: The county name to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["tax_authority"] = county
        self._params["authority_type"] = "COUNTY"
        return self

    def for_spd(self, spd_name: str):
        """
        Filter allocations for a special purpose district.

        Args:
            spd_name: The SPD name to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["tax_authority"] = spd_name
        self._params["authority_type"] = "SPD"
        return self

    def for_mta(self, mta_name: str):
        """
        Filter allocations for a mass transit authority.

        Args:
            mta_name: The MTA name to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["tax_authority"] = mta_name
        self._params["authority_type"] = "MTA"
        return self

    def for_year(self, year: int):
        """
        Filter allocations by reporting year.

        Args:
            year: The report year to filter by (e.g., 2023).

        Returns:
            Self for method chaining.
        """
        self._params["report_year"] = year
        return self

    def for_month(self, month: int):
        """
        Filter allocations by reporting month.

        Args:
            month: The report month to filter by (1-12).

        Returns:
            Self for method chaining.

        Raises:
            InvalidRequest: If month is not between 1 and 12.
        """
        if month < 1 or month > 12:
            raise InvalidRequest("Month must be between 1 and 12")
        self._params["report_month"] = month
        return self

    def sort_by(self, field: str, desc: bool = False):
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
        return self

    def get(self) -> List[SingleLocalAllocationData]:
        """
        Execute the query and return single local allocation records.

        Returns:
            List of SingleLocalAllocationData objects matching the query filters.

        Raises:
            HttpError: If the HTTP request to the Socrata API fails.
            InvalidRequest: If no records match the query parameters.
        """
        try:
            records = self.client.get(self.DATASET_ID, self._params)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest(f"No records returned from {self.__class__.__name__}")

        return [SingleLocalAllocationData.from_dict(r) for r in records]
    
    def get_all(self) -> List[SingleLocalAllocationData]:
        """
        Retrieve all single local allocation records without filtering.

        Warning: This method retrieves the entire dataset which may be very large.
        Use with caution and consider applying filters for better performance.

        Returns:
            List of all SingleLocalAllocationData objects in the dataset.

        Raises:
            HttpError: If the HTTP request to the Socrata API fails.
            InvalidRequest: If the dataset is empty or unavailable.
        """
        try:
            records = self.client.get(self.DATASET_ID)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest(f"No records returned from {self.__class__.__name__}")

        return [SingleLocalAllocationData.from_dict(r) for r in records]