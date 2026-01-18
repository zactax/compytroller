from typing import List

import httpx

from src.data.exceptions import HttpError, InvalidRequest
from src.data.responses.sales_tax import LocalAllocationPaymentDetailsData


class LocalAllocationPaymentDetail:
    """Query detailed local sales tax allocation payment records.

    This class provides access to the Local Allocation Payment Detail dataset via the
    Socrata API. It contains detailed payment breakdowns for local taxing authorities
    including cities, showing allocation amounts by month and payment type.

    Attributes:
        DATASET_ID: Socrata dataset identifier (3p4v-vsr3) for payment details.

    Example:
        >>> resource = LocalAllocationPaymentDetail(client)
        >>> results = resource.for_city("Austin").for_month("2024-01-01T00:00:00").limit(50).get()
        >>> for record in results:
        ...     print(record.authority_name, record.allocation_month, record.net_payment)
    """
    DATASET_ID = "3p4v-vsr3"

    def __init__(self, socrata_client):
        """Initialize the LocalAllocationPaymentDetail resource.

        Args:
            socrata_client: An instance of SocrataClient for API requests.
        """
        self.client = socrata_client
        self._params = {}

    def for_city(self, city: str):
        """Filter payment details by city name.

        Args:
            city: The city name to filter by (case-insensitive).

        Returns:
            Self for method chaining.
        """
        self._params["authority_name"] = f"'{city.upper()}'"
        return self

    def with_authority_id(self, authority_id: str):
        """Filter payment details by authority ID.

        Args:
            authority_id: The authority identifier to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["authority_id"] = f"'{authority_id}'"
        return self

    def for_month(self, month: str):
        """Filter payment details by allocation month.

        Args:
            month: The allocation month as a floating timestamp (e.g., "2024-01-01T00:00:00").

        Returns:
            Self for method chaining.
        """
        self._params["allocation_month"] = f"'{month}'"
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

    def get(self) -> List[LocalAllocationPaymentDetailsData]:
        """Execute the query and return payment detail records.

        Returns:
            List of LocalAllocationPaymentDetailsData objects matching the query filters.

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

        return [LocalAllocationPaymentDetailsData.from_dict(r) for r in records]
