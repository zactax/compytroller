from datetime import date, datetime
from io import StringIO
from typing import List, Optional, Union

import httpx
import pandas as pd

from compytroller.exceptions import HttpError, InvalidRequest
from compytroller.responses.sales_tax import SingleLocalTaxRateData
from compytroller.utils import parse_date

class SingleLocalTaxRates:
    """
    Query single local tax rate taxpayers via CSV download.

    This class downloads and parses single local tax rate data from a CSV file published by
    the Texas Comptroller. Single local tax rate taxpayers remit sales tax at a single rate
    rather than the standard combination of state, city, county, and special district rates.
    The data includes taxpayer numbers, names, begin dates, and end dates.

    Attributes:
        CSV_URL: URL for the single local tax rate CSV file.

    Example:
        >>> resource = SingleLocalTaxRates()
        >>> results = resource.get_after_date("2023-01-01")
        >>> for taxpayer in results:
        ...     print(taxpayer.taxpayer_number, taxpayer.name, taxpayer.begin_date)
    """
    CSV_URL = "https://assets.comptroller.texas.gov/open-data-files/single-local-tax-rate.csv"

    def __init__(self):
        """
        Initialize the SingleLocalTaxRates resource with an HTTP client.
        """
        self.client = httpx.Client(follow_redirects=True)

    def get_all(self) -> list[SingleLocalTaxRateData]:
        """
        Download and parse all single local tax rate records.

        Returns:
            List of all SingleLocalTaxRateData objects from the CSV file.

        Raises:
            HttpError: If the HTTP request to download the CSV fails.
            InvalidRequest: If the CSV is empty or cannot be parsed.
        """
        try:
            resp = self.client.get(self.CSV_URL)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        df = pd.read_csv(StringIO(resp.text))
        if df.empty:
            raise InvalidRequest("No records returned from Single Local Tax Rates CSV")

        records = []
        for _, row in df.iterrows():
            record_dict = {
                "taxpayer_number": str(row["Taxpayer Number"]),
                "name": row["Taxpayer Name"].strip(),
                "begin_date": row["Begin Date"],
                "end_date": row.get("End Date", ""),
            }
            records.append(SingleLocalTaxRateData.from_dict(record_dict))

        return records
    
    @staticmethod
    def _coerce_cutoff(cutoff: Union[str, date]) -> date:
        """
        Convert string or date to date object.

        Args:
            cutoff: Date string (YYYY-MM-DD) or date object.

        Returns:
            Date object.

        Raises:
            InvalidRequest: If the date string is invalid.
        """
        if isinstance(cutoff, date): # pragma: no cover
            return cutoff
        parsed = parse_date(cutoff)
        if parsed is None: # pragma: no cover
            raise InvalidRequest(f"Invalid cutoff_date: {cutoff!r}. Expected YYYY-MM-DD.")
        return parsed

    def get_before_date(self, cutoff_date: Union[str, date]) -> List[SingleLocalTaxRateData]:
        """
        Filter taxpayers whose registration ended before a specific date.

        Only returns taxpayers with an end_date that is strictly before the cutoff date.

        Args:
            cutoff_date: The cutoff date (YYYY-MM-DD string or date object).

        Returns:
            List of SingleLocalTaxRateData objects with end dates before the cutoff.

        Raises:
            HttpError: If the HTTP request to download the CSV fails.
            InvalidRequest: If the date is invalid or CSV cannot be parsed.
        """
        cutoff = self._coerce_cutoff(cutoff_date)
        all_providers = self.get_all()
        return [
            p for p in all_providers
            if p.end_date is not None and p.end_date < cutoff
        ]

    def get_after_date(self, cutoff_date: Union[str, date]) -> List[SingleLocalTaxRateData]:
        """
        Filter taxpayers whose registration began after a specific date.

        Only returns taxpayers with a begin_date that is strictly after the cutoff date.

        Args:
            cutoff_date: The cutoff date (YYYY-MM-DD string or date object).

        Returns:
            List of SingleLocalTaxRateData objects with begin dates after the cutoff.

        Raises:
            HttpError: If the HTTP request to download the CSV fails.
            InvalidRequest: If the date is invalid or CSV cannot be parsed.
        """
        cutoff = self._coerce_cutoff(cutoff_date)
        all_providers = self.get_all()
        return [
            p for p in all_providers
            if p.begin_date is not None and p.begin_date > cutoff
        ]
