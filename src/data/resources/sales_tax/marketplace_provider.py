import httpx
import pandas as pd
from io import StringIO
from typing import List
from data.responses.sales_tax import MarketplaceProviderData
from data.exceptions import HttpError, InvalidRequest


class MarketplaceProvider:
    CSV_URL = "https://assets.comptroller.texas.gov/open-data-files/marketplace-providers.csv"

    def __init__(self):
        self.client = httpx.Client(follow_redirects=True)

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

        return [MarketplaceProviderData.from_dict(row) for _, row in df.iterrows()]
