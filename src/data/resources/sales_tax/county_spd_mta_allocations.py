from typing import List

import httpx

from src.data.exceptions import HttpError, InvalidRequest
from src.data.responses.sales_tax import CountySPDMTAAllocationData


class CountySPDMTAAllocations:
    """
    Query county, special district, and transit authority sales tax allocations.

    This class provides access to the County/SPD/MTA Allocations dataset via the
    Socrata API. It contains allocation data for counties, special purpose districts (SPD),
    and mass transit authorities (MTA) in Texas.

    Attributes:
        DATASET_ID: Socrata dataset identifier (qsh8-tby8) for these allocations.

    Example:
        >>> resource = CountySPDMTAAllocations(client)
        >>> results = resource.for_type("County").with_name("Travis").limit(20).get()
        >>> for record in results:
        ...     print(record.type, record.name, record.allocation_amount)
    """
    DATASET_ID = "qsh8-tby8"

    def __init__(self, socrata_client):
        """
        Initialize the CountySPDMTAAllocations resource.

        Args:
            socrata_client: An instance of SocrataClient for API requests.
        """
        self.client = socrata_client
        self._params = {}

    def for_type(self, type_name: str):
        """
        Filter allocations by jurisdiction type.

        Args:
            type_name: The type to filter by (e.g., "County", "SPD", "MTA").

        Returns:
            Self for method chaining.
        """
        self._params["type"] = type_name.upper()
        return self

    def with_name(self, name: str):
        """
        Filter allocations by jurisdiction name.

        Args:
            name: The name of the county, district, or authority.

        Returns:
            Self for method chaining.
        """
        self._params["name"] = name
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

    def get(self) -> List[CountySPDMTAAllocationData]:
        """
        Execute the query and return allocation records.

        Returns:
            List of CountySPDMTAAllocationData objects matching the query filters.

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
        return [CountySPDMTAAllocationData.from_dict(r) for r in records]
