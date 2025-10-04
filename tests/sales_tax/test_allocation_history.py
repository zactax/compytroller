import pytest
import httpx
from data.resources.sales_tax.allocation_history import SalesTaxAllocationHistory
from data.responses.sales_tax import AllocationHistoryData
from data.exceptions import HttpError, InvalidRequest


HTML_FIXTURE = """
<html>
  <body>
    <table class="resultsTable">
      <thead><tr><th><span>2024</span></th></tr></thead>
      <tbody>
        <tr><td>January</td><td>1,000</td></tr>
        <tr><td>February</td><td>2,500</td></tr>
        <tr><td>TOTAL</td><td>ignored</td></tr>
      </tbody>
    </table>
  </body>
</html>
"""


def test_for_city_and_parsing(monkeypatch):
    class FakeResp:
        text = HTML_FIXTURE
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, *a, **kw): return FakeResp()

    h = SalesTaxAllocationHistory()
    h.client = FakeClient()
    records = h.for_city("Austin").get()
    assert len(records) == 2
    assert isinstance(records[0], AllocationHistoryData)
    assert records[0].authority_id == "Austin"
    assert records[0].authority_name == "City"


def test_for_county_and_for_special_district_and_for_transit_authority():
    h1 = SalesTaxAllocationHistory().for_county("Travis")
    assert h1.params["cityCountyOption"] == "County"
    h2 = SalesTaxAllocationHistory().for_special_district("SPD-123")
    assert h2.params["spdOptions"] == "SPD-123"
    h3 = SalesTaxAllocationHistory().for_transit_authority("MCC-ABC")
    assert h3.params["mccOptions"] == "MCC-ABC"


def test_allocation_history_http_status_error():
    class FailingClient:
        def post(self, *a, **kw):
            req = httpx.Request("POST", "https://fake")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("Server error", request=req, response=resp)

    h = SalesTaxAllocationHistory()
    h.client = FailingClient()
    h.for_city("Austin")
    with pytest.raises(HttpError):
        h.get()


def test_allocation_history_request_error():
    class FailingClient:
        def post(self, *a, **kw):
            raise httpx.RequestError("Network error", request=httpx.Request("POST", "https://fake"))

    h = SalesTaxAllocationHistory()
    h.client = FailingClient()
    h.for_city("Austin")
    with pytest.raises(HttpError):
        h.get()


def test_allocation_history_no_tables(monkeypatch):
    class FakeResp:
        text = "<html><body>No table</body></html>"
        def raise_for_status(self): return None
    class FakeClient:
        def post(self, *a, **kw): return FakeResp()

    h = SalesTaxAllocationHistory()
    h.client = FakeClient()
    h.for_city("Austin")
    with pytest.raises(InvalidRequest):
        h.get()


def test_allocation_history_no_endpoint():
    h = SalesTaxAllocationHistory()
    with pytest.raises(InvalidRequest):
        h.get()
