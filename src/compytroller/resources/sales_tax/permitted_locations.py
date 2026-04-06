from typing import List

import httpx

from compytroller.exceptions import HttpError, InvalidRequest
from compytroller.responses.sales_tax import PermittedLocationData
from compytroller.fields import PermittedLocationField

class PermittedLocations:
    """
    Query sales tax permitted business locations in Texas.

    This class provides access to the Permitted Locations dataset via the Socrata API.
    It contains detailed information about business locations with sales tax permits,
    including taxpayer numbers, NAICS codes, and taxing authority identifiers (TAIDs)
    for cities, counties, transit authorities, and special districts.

    Attributes:
        DATASET_ID: Socrata dataset identifier (3kx8-uryv) for permitted locations.

    Example:
        >>> resource = PermittedLocations(client)
        >>> results = resource.for_city("Austin").with_naics("722").limit(100).get()
        >>> for location in results:
        ...     print(location.tp_number, location.tp_city, location.naics)
    """
    DATASET_ID = "3kx8-uryv"

    def __init__(self, socrata_client):
        """
        Initialize the PermittedLocations resource.

        Args:
            socrata_client: An instance of SocrataClient for API requests.
        """
        self.client = socrata_client
        self._params = {}

    def for_city(self, city: str):
        """
        Filter permitted locations by city name.

        Args:
            city: The city name to filter by (case-insensitive).

        Returns:
            Self for method chaining.
        """
        self._params["tp_city"] = city.upper()
        return self

    def with_naics(self, code: str):
        """
        Filter permitted locations by NAICS industry code.

        Args:
            code: The NAICS code to filter by (e.g., "722" for food services).

        Returns:
            Self for method chaining.
        """
        self._params["naics"] = str(code)
        return self

    def with_tp_number(self, tp_number: str):
        """
        Filter permitted locations by taxpayer number.

        Args:
            tp_number: The taxpayer number to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["tp_number"] = tp_number
        return self

    def with_city_taid(self, taid: str):
        """
        Filter permitted locations by city taxing authority ID.

        Args:
            taid: The city TAID to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["city_taid"] = taid
        return self

    def with_county_taid(self, taid: str):
        """
        Filter permitted locations by county taxing authority ID.

        Args:
            taid: The county TAID to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["county_taid"] = taid
        return self

    def with_mta_taid(self, taid: str, slot: int = 1):
        """
        Filter permitted locations by mass transit authority TAID.

        Locations can have up to 2 MTA TAIDs (slots 1 and 2).

        Args:
            taid: The MTA TAID to filter by.
            slot: The slot number (1 or 2). Defaults to 1.

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If slot is not 1 or 2.
        """
        if slot not in (1, 2): # pragma: no cover
            raise ValueError("slot must be 1 or 2")
        self._params[f"mass_transit_auth{slot}_taid"] = taid
        return self

    def with_spd_taid(self, taid: str, slot: int = 1):
        """
        Filter permitted locations by special purpose district TAID.

        Locations can have up to 4 SPD TAIDs (slots 1-4).

        Args:
            taid: The SPD TAID to filter by.
            slot: The slot number (1, 2, 3, or 4). Defaults to 1.

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If slot is not 1, 2, 3, or 4.
        """
        if slot not in (1, 2, 3, 4): # pragma: no cover
            raise ValueError("slot must be 1, 2, 3, or 4")
        self._params[f"special_purp_dist{slot}_taid"] = taid
        return self

    def sort_by(self, field: str | PermittedLocationField, desc: bool = False):
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

    def get(self) -> List["PermittedLocationData"]:
        """
        Execute the query and return permitted location records.

        Returns:
            List of PermittedLocationData objects matching the query filters.

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

        return [PermittedLocationData.from_dict(r) for r in records]