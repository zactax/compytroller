import pytest
import httpx
from data.resources.mixed_beverage.history import MixedBeverageHistory
from data.responses.mixed_beverage_tax import MixedBeverageHistoryData
from data.exceptions import HttpError, InvalidRequest


HTML_FIXTURE = """
<html>
  <body>
    <table class="resultsTable">
      <thead><tr><th><span>2025</span></th></tr></thead>
      <tbody>
        <tr><td>January</td><td>1,234.56</td></tr>
        <tr><td>February</td><td>.</td></tr>
        <tr><td>TOTAL</td><td>ignored</td></tr>
      </tbody>
    </table>
  </body>
</html>
"""


def test_history_parsing(monkeypatch):
    class FakeResp:
        status_code = 200
        text = HTML_FIXTURE
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, *a, **kw): return FakeResp()

    h = MixedBeverageHistory()
    h.client = FakeClient()
    records = h.for_city("Austin").with_summary_type("Total Taxes").get()
    assert len(records) == 2
    assert isinstance(records[0], MixedBeverageHistoryData)
    assert records[0].jurisdiction_name == "Austin"
    assert records[0].net_payment == 1234.56
    assert records[1].net_payment is None  # February "."


def test_history_http_status_error(monkeypatch):
    class FailingClient:
        def post(self, *a, **kw):
            req = httpx.Request("POST", "https://fake")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("Server error", request=req, response=resp)

    h = MixedBeverageHistory()
    h.client = FailingClient()
    h.for_city("Austin")
    with pytest.raises(HttpError):
        h.get()


def test_history_request_error(monkeypatch):
    class FailingClient:
        def post(self, *a, **kw):
            raise httpx.RequestError("Connection failed", request=httpx.Request("POST", "https://fake"))

    h = MixedBeverageHistory()
    h.client = FailingClient()
    h.for_city("Austin")
    with pytest.raises(HttpError):
        h.get()


def test_history_error_page(monkeypatch):
    class FakeResp:
        text = "Oops! Something went wrong!"
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, *a, **kw): return FakeResp()

    h = MixedBeverageHistory()
    h.client = FakeClient()
    h.for_city("Austin")
    with pytest.raises(InvalidRequest):
        h.get()


def test_history_no_endpoint():
    h = MixedBeverageHistory()
    with pytest.raises(InvalidRequest):
        h.get()

def test_history_for_county_sets_payload():
    h = MixedBeverageHistory().for_county("Travis")
    assert h.endpoint == "CtyCntyAllocMixBevResults"
    assert h.payload["ccmOption"] == "County"
    assert h.payload["countyName"] == "Travis"


def test_history_for_special_district_sets_payload():
    h = MixedBeverageHistory().for_special_district("SPD-123")
    assert h.endpoint == "SPDAllocResults"
    assert h.payload["ccmOption"] == "MSA"
    assert h.payload["msaOptions"] == "SPD-123"

def test_history_no_results_table(monkeypatch):
    class FakeResp:
        text = "<html><body><p>No tables here</p></body></html>"
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, *a, **kw): return FakeResp()

    h = MixedBeverageHistory()
    h.client = FakeClient()
    h.for_city("Austin")
    with pytest.raises(InvalidRequest):
        h.get()

def test_history_invalid_month_skipped(monkeypatch):
    bad_html = """
    <table class="resultsTable">
      <thead><tr><th><span>2025</span></th></tr></thead>
      <tbody>
        <tr><td>NotAMonth</td><td>123</td></tr>
      </tbody>
    </table>
    """
    class FakeResp:
        text = bad_html
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, *a, **kw): return FakeResp()

    h = MixedBeverageHistory()
    h.client = FakeClient()
    h.for_city("Austin")
    records = h.get()
    assert records == []  # skipped due to ValueError

def test_history_invalid_float_parsing(monkeypatch):
    bad_html = """
    <table class="resultsTable">
      <thead><tr><th><span>2025</span></th></tr></thead>
      <tbody>
        <tr><td>January</td><td>not_a_number</td></tr>
      </tbody>
    </table>
    """
    class FakeResp:
        text = bad_html
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, *a, **kw): return FakeResp()

    h = MixedBeverageHistory()
    h.client = FakeClient()
    h.for_city("Austin")
    records = h.get()
    assert len(records) == 1
    assert records[0].net_payment is None  # value skipped
