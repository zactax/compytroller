from numpy import record
from src.data.responses.sales_tax import QuarterlySalesHistoryData
import httpx
from selectolax.parser import HTMLParser
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from src.data.exceptions import HttpError, InvalidRequest

class QuarterlySalesHistory:
    BASE_URL = "https://mycpa.cpa.state.tx.us/allocation/"
    SELECTOR_MAP = {
        "All Industries": "200",
        "Agriculture/Forestry/Fishing/Hunting": "11",
        "Utilities": "22",
        "Management of Companies/Enterprises": "55",
        "Nonclassifiable": "99",
        "Construction": "23",
        "Admin/Support/Waste Mgmt/Remediation Services": "56",
        "Manufacturing": "31-33",
        "Other": "100",
        "Transportation/Warehousing": "48-49",
        "Other Services (except Public Administration)": "81",
        "Public Administration": "92",
        "Arts/Entertainment/Recreation": "71",
        "Retail Trade": "44-45",
        "Educational Services": "61",
        "Accommodation/Food Services": "72",
        "Information": "51",
        "Health Care/Social Assistance": "62",
        "Finance/Insurance": "52",
        "Wholesale Trade": "42",
        "Real Estate/Rental/Leasing": "53",
        "Mining/Quarrying/Oil and Gas Extraction": "21",
        "Professional/Scientific/Technical Services": "54",
    }
    MSA_OPTIONS_MAP = {
        "Abilene MSA": "1",
        "Amarillo MSA": "2",
        "Austin-Round Rock MSA": "3",
        "Beaumont-Port Arthur MSA": "4",
        "Brownsville-Harlingen MSA": "5",
        "College Station-Bryan MSA": "6",
        "Corpus Christi MSA": "7",
        "Dallas-Plano-Irving MD": "8",
        "El Paso MSA": "9",
        "Fort Worth-Arlington MD": "10",
        "Houston-Sugar Land-Baytown MSA": "11",
        "Killeen-Temple-Fort Hood MSA": "12",
        "Laredo MSA": "13",
        "Longview MSA": "14",
        "Lubbock MSA": "15",
        "McAllen-Edinburg-Mission MSA": "16",
        "Midland MSA": "17",
        "Odessa MSA": "18",
        "San Angelo MSA": "19",
        "San Antonio MSA": "20",
        "Sherman-Denison MSA": "21",
        "Texarkana MSA": "22",
        "Tyler MSA": "23",
        "Victoria MSA": "24",
        "Waco MSA": "25",
        "Wichita Falls MSA": "26",
    }

    def __init__(self):
        self.client = httpx.Client(follow_redirects=True)
        self.payload: Dict[str, Any] = {}
        self.summary = True
        self.label = None
        self.endpoint: Optional[str] = None

    def summary_report(self, summary_type: str = "In-State"):
        self.endpoint = "QtrSalesSummaryResults"
        self.payload.clear()
        self.summary = True
        self.payload["summaryType"] = summary_type
        return self

    def report_by_ccma(self, ccm_option: str, jurisdiction_name: str):
        self.endpoint = "QtrSalesReportByResults"
        self.payload.clear()
        self.summary = False
        self.payload["ccmOption"] = ccm_option
        if ccm_option not in ["City", "County", "MSA"]:
            raise InvalidRequest(f"Invalid ccm_option: {ccm_option}. Must be 'City', 'County', or 'MSA'.")
        if ccm_option == "County":
            self.payload["countyName"] = jurisdiction_name
        elif ccm_option == "MSA":
            self.payload["msaOptions"] = self.MSA_OPTIONS_MAP.get(jurisdiction_name, jurisdiction_name)
        else:
            self.payload["cityName"] = jurisdiction_name
        return self

    def with_summary_type(self, summary_type: str):
        if not self.summary:
            raise InvalidRequest("Can only set summary type for summary reports.")
        self.payload["summaryType"] = summary_type
        return self

    def with_industry(self, label: str):
        self.label = label
        key = "selectorOptionsSummary" if self.summary else "selectorOptionsReportBy"
        self.payload[key] = self.SELECTOR_MAP.get(label, label)
        return self
    
    def reset(self):
        self.payload = {}        
        self.summary = True
        self.label = None
        self.endpoint = None
        return self

    def get(self) -> List["QuarterlySalesHistoryData"]:
        if not self.endpoint:
            raise InvalidRequest("No report type selected. Call summary_report() or report_by_ccma().")

        self.payload["submitButtonValue"] = "Get report"

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
        records: List[QuarterlySalesHistoryData] = []

        for tab in parser.css("div.tab-pane"):
            year = tab.attributes.get("id", "0")

            for row in tab.css("table.resultsTable tbody tr"):
                cols = [c.text(strip=True) for c in row.css("td")]
                if not cols or len(cols) < 4:
                    continue

                record_dict = {
                    "jurisdiction_name": (
                        self.payload.get("cityName")
                        or self.payload.get("countyName")
                        or self.payload.get("msaOptions")
                        or "Texas"
                    ),
                    "jurisdiction_type": self.payload.get("ccmOption", "State"),
                    "industry_label": self.label,
                    "summary_type": self.payload.get("summaryType") if self.summary else None,
                    "report_kind": "Summary" if self.summary else "CCMA",
                    "year": year,
                    "quarter": cols[0],
                    "gross_sales": cols[1],
                    "taxable_sales": cols[2],
                    "num_outlets": cols[3],
                }

                record = QuarterlySalesHistoryData.from_dict(record_dict)
                if record.quarter > 0:
                    records.append(record)

        if not records:
            raise InvalidRequest("No results parsed from response.")

        return records