from typing import List

import httpx

from src.compytroller.exceptions import HttpError, InvalidRequest
from src.compytroller.responses.sales_tax import SalesTaxRateData
from src.compytroller.fields import SalesTaxRateField, SalesTaxRateType


class SalesTaxRates:
    """
    Query sales tax rates for Texas jurisdictions.

    This class provides access to the Sales Tax Rates dataset via the Socrata API.
    It contains current and historical sales tax rates for cities, counties, special
    purpose districts (SPDs), and other taxing jurisdictions in Texas.

    Attributes:
        DATASET_ID: Socrata dataset identifier (tmhs-ahbh) for sales tax rates.

    Example:
        >>> resource = SalesTaxRates(client)
        >>> results = resource.for_city("Austin").for_year(2023).get()
        >>> for rate in results:
        ...     print(rate.city_name, rate.report_year, rate.combined_rate)
    """
    DATASET_ID = "tmhs-ahbh"

    def __init__(self, socrata_client):
        """
        Initialize the SalesTaxRates resource.

        Args:
            socrata_client: An instance of SocrataClient for API requests.
        """
        self.client = socrata_client
        self._params = {}

    def for_city(self, city: str):
        """
        Filter sales tax rates by city name.

        Args:
            city: The city name to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["city_name"] = city
        return self

    def in_county(self, county: str):
        """
        Filter sales tax rates by county name.

        Args:
            county: The county name to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["county_name"] = county
        return self

    def for_type(self, jurisdiction_type: str | SalesTaxRateType):
        """
        Filter sales tax rates by jurisdiction type.

        Args:
            jurisdiction_type: The type to filter by (e.g., "SPD List", "City List").

        Returns:
            Self for method chaining.
        """
        self._params["type"] = jurisdiction_type
        return self

    def for_year(self, year: int):
        """
        Filter sales tax rates by report year.

        Args:
            year: The report year to filter by (e.g., 2023).

        Returns:
            Self for method chaining.
        """
        self._params["report_year"] = year
        return self

    def sort_by(self, field: str | SalesTaxRateField, desc: bool = False):
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

    def get(self) -> List["SalesTaxRateData"]:
        """
        Execute the query and return sales tax rate records.

        Returns:
            List of SalesTaxRateData objects matching the query filters.

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

        return [SalesTaxRateData.from_dict(r) for r in records]