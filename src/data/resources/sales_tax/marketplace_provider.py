import httpx
import pandas as pd
from io import StringIO
from typing import List, Optional, Union
from datetime import date

from src.data.responses.sales_tax import MarketplaceProviderData
from src.data.exceptions import HttpError, InvalidRequest
from src.data.utils import parse_date


class MarketplaceProvider:
    CSV_URL = "https://assets.comptroller.texas.gov/open-data-files/marketplace-providers.csv"

    def __init__(self):
        self.client = httpx.Client(follow_redirects=True)
        self.instructions = {}

    @staticmethod
    def _coerce_cutoff(cutoff: Union[str, date]) -> date:
        if isinstance(cutoff, date):
            return cutoff
        parsed = parse_date(cutoff)
        if parsed is None:
            raise InvalidRequest(f"Invalid cutoff_date: {cutoff!r}. Expected YYYY-MM-DD.")
        return parsed

    def before_date(self, cutoff_date: Union[str, date]) -> List[MarketplaceProviderData]:
        """
        Providers whose end_date exists AND is strictly before cutoff_date.
        """
        self.instructions["before_date"] = self._coerce_cutoff(cutoff_date)
        return self

    def after_date(self, cutoff_date: Union[str, date]) -> List[MarketplaceProviderData]:
        """
        Providers whose begin_date exists AND is strictly after cutoff_date.
        """
        self.instructions["after_date"] = self._coerce_cutoff(cutoff_date)
        return self
    
    def reset(self):
        self.instructions = {}
        return self
        
    def get(self) -> List[MarketplaceProviderData]:
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
        
