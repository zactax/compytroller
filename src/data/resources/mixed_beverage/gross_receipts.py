from datetime import date, datetime
from io import StringIO
from typing import List, Optional, Union

import httpx
import pandas as pd

from src.data.exceptions import HttpError, InvalidRequest
from src.data.responses.mixed_beverage_tax import MixedBeverageGrossReceiptsData
from src.data.utils import parse_date
from src.data.fields import MixedBeverageGrossReceiptsField

class MixedBeverageGrossReceipts:
    """
    Query mixed beverage gross receipts data in Texas.

    This class provides access to the Mixed Beverage Gross Receipts dataset via the
    Socrata API. It contains revenue data from businesses with mixed beverage permits
    (typically bars, restaurants, and clubs), including taxpayer information, location
    details, TABC permit numbers, and gross receipt amounts.

    Attributes:
        DATASET_ID: Socrata dataset identifier (naix-2893) for mixed beverage gross receipts.

    Example:
        >>> resource = MixedBeverageGrossReceipts(client)
        >>> results = resource.location_for_city("Austin").limit(100).get()
        >>> for record in results:
        ...     print(record.location_name, record.location_city, record.gross_receipts)
    """
    DATASET_ID = "naix-2893"

    def __init__(self, socrata_client):
        """
        Initialize the MixedBeverageGrossReceipts resource.

        Args:
            socrata_client: An instance of SocrataClient for API requests.
        """
        self.client = socrata_client
        self._params = {}
        self._where_clauses = []

    def for_taxpayer(self, number):
        """
        Filter gross receipts by taxpayer number.

        Args:
            number: The taxpayer number to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["taxpayer_number"] = str(number)
        return self

    def taxpayer_for_city(self, city: str):
        """
        Filter gross receipts by taxpayer's city.

        Args:
            city: The taxpayer's city name to filter by (case-insensitive).

        Returns:
            Self for method chaining.
        """
        self._params["taxpayer_city"] = city.upper()
        return self

    def for_location(self, name):
        """
        Filter gross receipts by location name.

        Args:
            name: The location name to filter by (case-insensitive).

        Returns:
            Self for method chaining.
        """
        self._params["location_name"] = str(name).upper()
        return self

    def location_for_city(self, city: str):
        """
        Filter gross receipts by location city.

        Args:
            city: The location city name to filter by (case-insensitive).

        Returns:
            Self for method chaining.
        """
        self._params["location_city"] = city.upper()
        return self

    def location_inside_city_limits(self, inside: bool = True):
        """
        Filter gross receipts by whether location is inside city limits.

        Args:
            inside: If True, filter for locations inside city limits. If False,
                filter for locations outside city limits. Defaults to True.

        Returns:
            Self for method chaining.
        """
        self._params["inside_outside_city_limits_code_y_n"] = "Y" if inside else "N"
        return self

    def with_location_number(self, location_number):
        """
        Filter gross receipts by location number.

        Args:
            location_number: The location number to filter by.

        Returns:
            Self for method chaining.
        """
        self._params["location_number"] = str(location_number)
        return self

    def with_tabc_permit(self, tabc_permit: str):
        """
        Filter gross receipts by TABC permit number.

        Args:
            tabc_permit: The Texas Alcoholic Beverage Commission permit number.

        Returns:
            Self for method chaining.
        """
        self._params["tabc_permit_number"] = tabc_permit
        return self

    def responsibility_start_after(self, date: str):
        """
        Filter gross receipts where responsibility began after a specific date.

        Args:
            date: The cutoff date in ISO format (YYYY-MM-DD).

        Returns:
            Self for method chaining.
        """
        self._where_clauses.append(f"responsibility_begin_date_yyyymmdd > '{date}'")
        return self

    def responsibility_start_before(self, date: str):
        """
        Filter gross receipts where responsibility began before a specific date.

        Args:
            date: The cutoff date in ISO format (YYYY-MM-DD).

        Returns:
            Self for method chaining.
        """
        self._where_clauses.append(f"responsibility_begin_date_yyyymmdd < '{date}'")
        return self

    def responsibility_between_dates(self, start: str, end: str):
        """
        Filter gross receipts where responsibility began within a date range.

        Args:
            start: The start date in ISO format (YYYY-MM-DD).
            end: The end date in ISO format (YYYY-MM-DD).

        Returns:
            Self for method chaining.
        """
        self._where_clauses.append(
            f"responsibility_begin_date_yyyymmdd BETWEEN '{start}' AND '{end}'"
        )
        return self

    def sort_by(self, field: str | MixedBeverageGrossReceiptsField, desc: bool = False):
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

    def get(self) -> List[MixedBeverageGrossReceiptsData]:
        """
        Execute the query and return mixed beverage gross receipts records.

        Returns:
            List of MixedBeverageGrossReceiptsData objects matching the query filters.

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

        return [MixedBeverageGrossReceiptsData.from_dict(r) for r in records]