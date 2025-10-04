from data.responses.sales_tax import SingleLocalTaxRateData
import httpx
import pandas as pd
from io import StringIO
from datetime import datetime
from data.exceptions import HttpError, InvalidRequest


class SingleLocalTaxRates:
    CSV_URL = "https://assets.comptroller.texas.gov/open-data-files/single-local-tax-rate.csv"

    def __init__(self):
        self.client = httpx.Client(follow_redirects=True)

    def get(self) -> list[SingleLocalTaxRateData]:
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
    def _parse_date(value: str): ## pragma: no cover
        if not value or pd.isna(value):
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except Exception:
            return None