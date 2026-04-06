from datetime import date
from io import StringIO
from typing import List, Optional, Union

import httpx
import pandas as pd

from compytroller.exceptions import HttpError, InvalidRequest
from compytroller.responses.sales_tax import MarketplaceProviderData
from compytroller.utils import parse_date


class MarketplaceProvider:
    """
    Query marketplace providers registered with the Texas Comptroller.

    This class downloads and parses marketplace provider data from a CSV file published by
    the Texas Comptroller. Marketplace providers are platforms (like Amazon or eBay) that
    facilitate retail sales and are responsible for collecting sales tax. The data includes
    provider names, begin dates, and end dates for their registration periods.

    Attributes:
        CSV_URL: URL for the marketplace providers CSV file.

    Example:
        >>> resource = MarketplaceProvider()
        >>> results = resource.after_date("2023-01-01").get()
        >>> for provider in results:
        ...     print(provider.provider_name, provider.begin_date, provider.end_date)
    """
    CSV_URL = "https://assets.comptroller.texas.gov/open-data-files/marketplace-providers.csv"

    def __init__(self):
        """Initialize the MarketplaceProvider resource with an HTTP client."""
        self.client = httpx.Client(follow_redirects=True)
        self.instructions = {}

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

    def before_date(self, cutoff_date: Union[str, date]) -> List[MarketplaceProviderData]:
        """
        Filter providers whose registration ended before a specific date.

        Only returns providers with an end_date that is strictly before the cutoff date.

        Args:
            cutoff_date: The cutoff date (YYYY-MM-DD string or date object).

        Returns:
            Self for method chaining.
        """
        self.instructions["before_date"] = self._coerce_cutoff(cutoff_date)
        return self

    def after_date(self, cutoff_date: Union[str, date]) -> List[MarketplaceProviderData]:
        """
        Filter providers whose registration began after a specific date.

        Only returns providers with a begin_date that is strictly after the cutoff date.

        Args:
            cutoff_date: The cutoff date (YYYY-MM-DD string or date object).

        Returns:
            Self for method chaining.
        """
        self.instructions["after_date"] = self._coerce_cutoff(cutoff_date)
        return self

    def reset(self):
        """
        Reset all filters to their default state.

        Returns:
            Self for method chaining.
        """
        self.instructions = {}
        return self

    def get(self) -> List[MarketplaceProviderData]:
        """
        Download, parse, and return filtered marketplace provider records.

        Downloads the CSV file, parses it into data objects, and applies any date filters
        that were specified via before_date() or after_date() methods.

        Returns:
            List of MarketplaceProviderData objects matching the filters.

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
            raise InvalidRequest("No records returned from Marketplace Providers CSV")
        results = [MarketplaceProviderData.from_dict(row) for _, row in df.iterrows()]
        if "after_date" in self.instructions:
            cutoff = self.instructions["after_date"]
            results = [
                p for p in results
                if p.begin_date is not None and p.begin_date > cutoff
            ]
        if "before_date" in self.instructions:
            cutoff = self.instructions["before_date"]
            results = [
                p for p in results
                if p.end_date is not None and p.end_date < cutoff
            ]
        return results
        
