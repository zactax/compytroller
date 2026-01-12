from src.data.responses.sales_tax import SingleLocalTaxRateData
import httpx
import pandas as pd
from io import StringIO
from datetime import datetime
from src.data.exceptions import HttpError, InvalidRequest
from src.data.utils import parse_date
from typing import List, Optional, Union
from datetime import date

class SingleLocalTaxRates:
    CSV_URL = "https://assets.comptroller.texas.gov/open-data-files/single-local-tax-rate.csv"

    def __init__(self):
        self.client = httpx.Client(follow_redirects=True)

    def get_all(self) -> list[SingleLocalTaxRateData]:
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
        if isinstance(cutoff, date):
            return cutoff
        parsed = parse_date(cutoff)
        if parsed is None:
            raise InvalidRequest(f"Invalid cutoff_date: {cutoff!r}. Expected YYYY-MM-DD.")
        return parsed

    def get_before_date(self, cutoff_date: Union[str, date]) -> List[SingleLocalTaxRateData]:
        """
        Providers whose end_date exists AND is strictly before cutoff_date.
        """
        cutoff = self._coerce_cutoff(cutoff_date)
        all_providers = self.get_all()
        return [
            p for p in all_providers
            if p.end_date is not None and p.end_date < cutoff
        ]

    def get_after_date(self, cutoff_date: Union[str, date]) -> List[SingleLocalTaxRateData]:
        """
        Providers whose begin_date exists AND is strictly after cutoff_date.
        """
        cutoff = self._coerce_cutoff(cutoff_date)
        all_providers = self.get_all()
        return [
            p for p in all_providers
            if p.begin_date is not None and p.begin_date > cutoff
        ]
