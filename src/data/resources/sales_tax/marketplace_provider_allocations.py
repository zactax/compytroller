from typing import List

import httpx

from src.data.exceptions import HttpError, InvalidRequest
from src.data.responses.sales_tax import MarketplaceProviderAllocationData
from src.data.fields import AuthorityType, MarketplaceProviderAllocationField


class MarketplaceProviderAllocations:
    """
    Query sales tax allocations from marketplace providers.

    This class provides access to the Marketplace Provider Allocations dataset via the
    Socrata API. It contains allocation data showing how marketplace sales tax revenue
    is distributed to local taxing authorities (cities, counties, etc.) in Texas.

    Attributes:
        DATASET_ID: Socrata dataset identifier (hezn-fbgw) for marketplace allocations.

    Example:
        >>> resource = MarketplaceProviderAllocations(client)
        >>> results = resource.for_authority("Austin").for_type("CITY").for_year(2023).get()
        >>> for record in results:
        ...     print(record.authority_name, record.allocation_amount, record.allocation_year)
    """
    DATASET_ID = "hezn-fbgw"

    def __init__(self, socrata_client):
        """
        Initialize the MarketplaceProviderAllocations resource.

        Args:
            socrata_client: An instance of SocrataClient for API requests.
        """
        self.client = socrata_client
        self._params = {}
        self.authority_name = []

    def for_authority(self, name: str):
        """
        Filter allocations by authority name.

        Note: Authority names in the dataset may be stored in different cases.
        This method searches for both the original case and uppercase versions.

        Args:
            name: The authority name to filter by (e.g., "Austin" or "AUSTIN").

        Returns:
            Self for method chaining.
        """
        self.authority_name.append(name)
        self.authority_name.append(name.upper())
        return self

    def for_type(self, authority_type: str | AuthorityType):
        """
        Filter allocations by authority type.

        Args:
            authority_type: The type to filter by (e.g., "CITY", "COUNTY", "SPD", "TRANSIT").

        Returns:
            Self for method chaining.
        """
        self._params["authority_type"] = authority_type
        return self

    def for_year(self, year: int):
        """
        Filter allocations by year.

        Args:
            year: The allocation year to filter by (e.g., 2023).

        Returns:
            Self for method chaining.
        """
        self._params["allocation_year"] = year
        return self

    def sort_by(self, field: str | MarketplaceProviderAllocationField, desc: bool = False):
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
        self.authority_name = []
        return self

    def get(self) -> List["MarketplaceProviderAllocationData"]:
        """
        Execute the query and return marketplace provider allocation records.

        If filtering by authority name, this method queries both the original case
        and uppercase versions to ensure complete results.

        Returns:
            List of MarketplaceProviderAllocationData objects matching the query filters.

        Raises:
            HttpError: If the HTTP request to the Socrata API fails.
            InvalidRequest: If no records match the query parameters.
        """
        # Step 1: Execute HTTP request and handle HTTP errors
        raw_records = []
        try:
            if self.authority_name:
                for name in self.authority_name:
                    self._params["authority_name"] = name
                    cur_records = self.client.get(self.DATASET_ID, self._params)
                    raw_records.extend(cur_records)
            else:
                raw_records = self.client.get(self.DATASET_ID, self._params)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        # Step 2: Validate we got data
        if not raw_records:
            raise InvalidRequest(f"No records returned from {self.__class__.__name__}")

        # Step 3: Transform to data objects (outside try/except)
        return [MarketplaceProviderAllocationData.from_dict(r) for r in raw_records]
        