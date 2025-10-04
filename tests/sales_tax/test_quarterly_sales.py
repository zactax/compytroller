from data.responses.sales_tax import QuarterlySalesHistoryData
import pytest
import httpx
from data.resources.sales_tax.quarterly_sales_history import QuarterlySalesHistory
from data.exceptions import HttpError, InvalidRequest


HTML_SAMPLE = """
<div class="tab-pane" id="2023">
  <table class="resultsTable">
    <tbody>
      <tr><td>1</td><td>1,000</td><td>500</td><td>10</td></tr>
      <tr><td>2</td><td>2,000</td><td>1,200</td><td>12</td></tr>
      <tr><td>Bad</td><td>NaN</td><td></td><td>Oops</td></tr>
    </tbody>
  </table>
</div>
"""

HTML_MISSING_COLS = """
<div class="tab-pane" id="2023">
  <table class="resultsTable">
    <tbody>
      <tr><td>1</td><td>1000</td></tr> <!-- too few cols -->
    </tbody>
  </table>
</div>
"""

HTML_EMPTY = """
<div class="tab-pane" id="2023">
  <table class="resultsTable"><tbody></tbody></table>
</div>
"""

def test_quarterly_sales_history_summary_parsing(monkeypatch):
    class FakeResp:
        text = HTML_SAMPLE
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, url, data, headers=None): return FakeResp()

    qsh = QuarterlySalesHistory()
    qsh.client = FakeClient()
    results = (
        qsh.summary_report("In-State")
        .with_industry("Retail Trade")
        .get()
    )

    assert len(results) == 2  # only the valid rows
    r1 = results[0]
    assert isinstance(r1, QuarterlySalesHistoryData)
    assert r1.year == 2023
    assert r1.quarter == 1
    assert r1.gross_sales == 1000.0
    assert r1.taxable_sales == 500.0
    assert r1.num_outlets == 10
    assert r1.report_kind == "Summary"
    assert r1.summary_type == "In-State"
    assert r1.industry_label == "Retail Trade"


def test_quarterly_sales_history_ccma_city(monkeypatch):
    class FakeResp:
        text = HTML_SAMPLE
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, url, data, headers=None): return FakeResp()

    qsh = QuarterlySalesHistory()
    qsh.client = FakeClient()
    results = (
        qsh.report_by_ccma("City", "Austin")
        .with_industry("Information")
        .get()
    )

    assert all(r.report_kind == "CCMA" for r in results)
    assert all(r.summary_type is None for r in results)
    assert results[0].jurisdiction_name == "Austin"


def test_quarterly_sales_history_ccma_county(monkeypatch):
    class FakeResp:
        text = HTML_SAMPLE
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, url, data, headers=None): return FakeResp()

    qsh = QuarterlySalesHistory()
    qsh.client = FakeClient()
    results = qsh.report_by_ccma("County", "Travis").get()
    assert results[0].jurisdiction_name == "Travis"


def test_quarterly_sales_history_ccma_msa(monkeypatch):
    class FakeResp:
        text = HTML_SAMPLE
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, url, data, headers=None): return FakeResp()

    qsh = QuarterlySalesHistory()
    qsh.client = FakeClient()
    results = qsh.report_by_ccma("MSA", "Austin-Round Rock MSA").get()
    assert results[0].jurisdiction_type == "MSA"


def test_quarterly_sales_history_with_summary_type_error():
    qsh = QuarterlySalesHistory().report_by_ccma("City", "Austin")
    with pytest.raises(InvalidRequest):
        qsh.with_summary_type("Grand Totals")


def test_quarterly_sales_history_server_error_page(monkeypatch):
    class FakeResp:
        text = "Oops! Something went wrong!"
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, url, data, headers=None): return FakeResp()

    qsh = QuarterlySalesHistory()
    qsh.client = FakeClient()
    qsh.summary_report()
    with pytest.raises(InvalidRequest):
        qsh.get()


def test_quarterly_sales_history_http_status_error():
    class FailingClient:
        def post(self, url, data, headers=None):
            req = httpx.Request("POST", url)
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("server error", request=req, response=resp)

    qsh = QuarterlySalesHistory()
    qsh.client = FailingClient()
    qsh.summary_report()
    with pytest.raises(HttpError):
        qsh.get()


def test_quarterly_sales_history_request_error():
    class FailingClient:
        def post(self, url, data, headers=None):
            raise httpx.RequestError("network fail", request=httpx.Request("POST", url))

    qsh = QuarterlySalesHistory()
    qsh.client = FailingClient()
    qsh.summary_report()
    with pytest.raises(HttpError):
        qsh.get()


def test_quarterly_sales_history_no_endpoint():
    qsh = QuarterlySalesHistory()
    with pytest.raises(InvalidRequest):
        qsh.get()


def test_quarterly_sales_historydata_from_dict():
    data = {
        "jurisdiction_name": "Austin",
        "jurisdiction_type": "City",
        "industry_label": "Retail Trade",
        "summary_type": "In-State",
        "report_kind": "Summary",
        "year": "2023",
        "quarter": "2",
        "gross_sales": "2,000",
        "taxable_sales": "1,500",
        "num_outlets": "20",
    }
    dto = QuarterlySalesHistoryData.from_dict(data)

    assert isinstance(dto, QuarterlySalesHistoryData)
    assert dto.year == 2023
    assert dto.quarter == 2
    assert dto.gross_sales == 2000.0
    assert dto.taxable_sales == 1500.0
    assert dto.num_outlets == 20

def test_quarterly_sales_history_with_summary_type_success(monkeypatch):
    class FakeResp:
        text = HTML_SAMPLE
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, url, data, headers=None): return FakeResp()

    qsh = QuarterlySalesHistory()
    qsh.client = FakeClient()
    results = (
        qsh.summary_report("In-State")
        .with_summary_type("Grand Totals")
        .with_industry("Retail Trade")
        .get()
    )
    assert all(r.summary_type == "Grand Totals" for r in results)

def test_quarterly_sales_history_skips_incomplete_rows(monkeypatch):
    class FakeResp:
        text = HTML_MISSING_COLS
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, url, data, headers=None): return FakeResp()

    qsh = QuarterlySalesHistory()
    qsh.client = FakeClient()
    qsh.summary_report("In-State").with_industry("Retail Trade")
    with pytest.raises(InvalidRequest):  # no valid rows remain
        qsh.get()

def test_quarterly_sales_history_no_records(monkeypatch):
    class FakeResp:
        text = HTML_EMPTY
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, url, data, headers=None): return FakeResp()

    qsh = QuarterlySalesHistory()
    qsh.client = FakeClient()
    qsh.summary_report("In-State").with_industry("Retail Trade")
    with pytest.raises(InvalidRequest):
        qsh.get()
