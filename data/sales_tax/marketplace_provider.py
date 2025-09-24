import httpx
import pandas as pd
from io import StringIO
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from data.responses.sales_tax import MarketplaceProviderData


class MarketplaceProvider:
    CSV_URL = "https://assets.comptroller.texas.gov/open-data-files/marketplace-providers.csv"

    def __init__(self):
        self.client = httpx.Client(follow_redirects=True)

    def get(self) -> List[MarketplaceProviderData]:
        resp = self.client.get(self.CSV_URL)
        resp.raise_for_status()

        # Use StringIO to wrap CSV text for pandas
        df = pd.read_csv(StringIO(resp.text))

        records: List[MarketplaceProviderData] = []
        for _, row in df.iterrows():
            records.append(
                MarketplaceProviderData(
                    taxpayer_number=str(row["Taxpayer Number"]),
                    name=row["Taxpayer Name"].strip(),
                    begin_date=self._parse_date(row["Begin Date"]),
                    end_date=self._parse_date(row.get("End Date", "")),
                )
            )
        return records

    @staticmethod
    def _parse_date(value: str) -> Optional[datetime.date]:
        if not value or pd.isna(value):
            return None
        return datetime.strptime(value, "%Y-%m-%d").date()
