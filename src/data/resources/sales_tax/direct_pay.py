from typing import List

import httpx

from src.data.exceptions import HttpError, InvalidRequest
from src.data.responses.sales_tax import DirectPayTaxpayerData

class DirectPayTaxpayers:
    """
    Query sales tax direct pay taxpayers in Texas.

    This class provides access to the Direct Pay Taxpayers dataset via the Socrata API.
    Direct pay taxpayers are authorized to purchase goods and services tax-free and remit
    sales tax directly to the Comptroller, typically large businesses or government entities.

    Attributes:
        DATASET_ID: Socrata dataset identifier (deed-e7u6) for direct pay taxpayers.

    Example:
        >>> resource = DirectPayTaxpayers(client)
        >>> results = resource.for_city("Austin").with_naics("541").limit(25).get()
        >>> for taxpayer in results:
        ...     print(taxpayer.taxpayer_name, taxpayer.city, taxpayer.naics_code)
    """
    DATASET_ID = "deed-e7u6"

    def __init__(self, socrata_client):
        """
        Initialize the DirectPayTaxpayers resource.

        Args:
            socrata_client: An instance of SocrataClient for API requests.
        """
        self.client = socrata_client
        self._params = {}

    def with_naics(self, code: str):
        """
        Filter direct pay taxpayers by NAICS industry code.

        Args:
            code: The NAICS code to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["naics_code"] = code
        return self

    def in_county(self, county: str):
        """
        Filter direct pay taxpayers by county name.

        Args:
            county: The county name to filter by (case-insensitive).

        Returns:
            Self for method chaining.
        """
        self._params["county"] = county.upper()
        return self

    def for_city(self, city: str):
        """
        Filter direct pay taxpayers by city name.

        Args:
            city: The city name to filter by (case-insensitive).

        Returns:
            Self for method chaining.
        """
        self._params["city"] = city.upper()
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

    def get(self) -> List["DirectPayTaxpayerData"]:
        """
        Execute the query and return direct pay taxpayer records.

        Returns:
            List of DirectPayTaxpayerData objects matching the query filters.

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

        return [DirectPayTaxpayerData.from_dict(r) for r in records]
