from typing import List

import httpx

from src.data.exceptions import HttpError, InvalidRequest
from src.data.responses.sales_tax import ComparisonSummaryData


class CityCountyComparisonSummary:
    """Query city and county sales tax comparison summaries.

    This class provides access to the City County Comparison Summary dataset via the
    Socrata API. It contains comparative sales tax statistics for cities and counties
    in Texas, including year-over-year comparisons and percent changes.

    Attributes:
        DATASET_ID: Socrata dataset identifier (53pa-m7sm) for comparison summaries.

    Example:
        >>> resource = CityCountyComparisonSummary(client)
        >>> results = resource.for_city("Dallas").limit(10).get()
        >>> for record in results:
        ...     print(record.city, record.current_year, record.percent_change)
    """
    DATASET_ID = "53pa-m7sm"

    def __init__(self, socrata_client):
        """Initialize the CityCountyComparisonSummary resource.

        Args:
            socrata_client: An instance of SocrataClient for API requests.
        """
        self.client = socrata_client
        self._params = {}

    def for_city(self, name: str):
        """Filter comparison data by city name.

        Args:
            name: The city name to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["city"] = name
        return self

    def in_county(self, name: str):
        """Filter comparison data by county name.

        Args:
            name: The county name to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["county"] = name
        return self

    def sort_by(self, field: str, desc: bool = False):
        """Sort results by a specific field.

        Args:
            field: The field name to sort by.
            desc: If True, sort in descending order. Defaults to False (ascending).

        Returns:
            Self for method chaining.
        """
        self._params["$order"] = f"{field} DESC" if desc else field
        return self

    def limit(self, n: int):
        """Limit the number of results returned.

        Args:
            n: Maximum number of results to return.

        Returns:
            Self for method chaining.
        """
        self._params["$limit"] = n
        return self

    def reset(self):
        """Reset all filters and parameters to their default state.

        Returns:
            Self for method chaining.
        """
        self._params = {}
        return self

    def get(self) -> List[ComparisonSummaryData]:
        """Execute the query and return comparison summary records.

        Returns:
            List of ComparisonSummaryData objects matching the query filters.

        Raises:
            HttpError: If the HTTP request to the Socrata API fails.
            InvalidRequest: If no records match the query parameters.
        """
        # Step 1: Execute HTTP request and handle HTTP errors
        try:
            records = self.client.get(self.DATASET_ID, self._params)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        # Step 2: Validate we got data
        if not records:
            raise InvalidRequest(f"No records returned from {self.__class__.__name__}")

        # Step 3: Transform to data objects (outside try/except)
        return [ComparisonSummaryData.from_dict(r) for r in records]
