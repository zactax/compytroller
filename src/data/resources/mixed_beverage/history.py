import httpx
from selectolax.parser import HTMLParser
from datetime import datetime
from typing import List
from src.data.responses.mixed_beverage_tax import MixedBeverageHistoryData
from src.data.exceptions import HttpError, InvalidRequest


class MixedBeverageHistory:
    BASE_URL = "https://mycpa.cpa.state.tx.us/allocation/"

    def __init__(self):
        self.client = httpx.Client(follow_redirects=True)
        self.endpoint = None
        self.payload = {"summaryType": "Total Taxes"}

    def for_city(self, name: str):
        self.endpoint = "CtyCntyAllocMixBevResults"
        self.payload = {"ccmOption": "City", "cityName": name, "msaOption": "SPD"}
        return self

    def for_county(self, name: str):
        self.endpoint = "CtyCntyAllocMixBevResults"
        self.payload = {"ccmOption": "County", "countyName": name, "msaOption": "SPD"}
        return self

    def for_special_district(self, name: str):
        self.endpoint = "CtyCntyAllocMixBevResults"
        self.payload = {"ccmOption": "MSA", "msaOption": "SPD", "msaOptions": name}
        return self

    def with_summary_type(self, summary_type: str):
        if self.endpoint is None:
            raise InvalidRequest("Must call for_city, for_county, or for_special_district first.")
        self.payload["summaryType"] = summary_type
        return self
    
    def statewide_summary(self, summary_scope: str, summary_type: str):
        """
        summary_scope: 'State Revenue', 'All Counties', 'All Cities', 'All SPDs'
        summary_type: 'Total Taxes', 'Gross Receipts', 'Sales Tax'
        """
        self.endpoint = "StatewideAllocMixBevResults"
        self.payload = {'stateOption': summary_scope, 'summaryType': summary_type}
        return self
    
    def reset(self):
        self.endpoint = None
        self.payload = {"summaryType": "Total Taxes"}
        return self

    def get(self) -> List[MixedBeverageHistoryData]:
        if not self.endpoint:
            raise InvalidRequest("Must call for_city, for_county, or for_special_district first.")

        self.payload["submitButtonValue"] = "Get report"
        # Debug print to show payload being sent
        try:
            resp = self.client.post(
                f"{self.BASE_URL}{self.endpoint}",
                data=self.payload,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": f"{self.BASE_URL}{self.endpoint}",
                    "User-Agent": "Mozilla/5.0",
                },
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if "Oops! Something went wrong!" in resp.text:
            raise InvalidRequest("Server returned error page. Likely bad params.")

        parser = HTMLParser(resp.text)
        tables = parser.css("table.resultsTable")

        if not tables:
            raise InvalidRequest("No results tables found in response.")

        records: List[MixedBeverageHistoryData] = []
        for table in tables:
            year_text = table.css_first("thead span").text(strip=True)
            year = int(year_text)

            for row in table.css("tbody tr"):
                cols = [c.text(strip=True) for c in row.css("td")]
                if not cols or cols[0].strip() in ("", "\xa0", "TOTAL"):
                    continue

                month_text = cols[0]
                try:
                    allocation_date = datetime.strptime(
                        f"{month_text} {year}", "%B %Y"
                    ).date().replace(day=1)
                except ValueError:
                    continue

                val = None
                if len(cols) > 1 and cols[1].strip() and cols[1] != ".":
                    try:
                        val = float(cols[1].replace(",", ""))
                    except ValueError:
                        pass

                records.append(
                    MixedBeverageHistoryData(
                        jurisdiction_name=self.payload.get("cityName")
                        or self.payload.get("countyName")
                        or self.payload.get("msaOptions", ""),
                        jurisdiction_type=self.payload.get("ccmOption", ""),
                        summary_type=self.payload.get("summaryType", ""),
                        allocation_month=allocation_date,
                        net_payment=val,
                    )
                )
        return records
    
    