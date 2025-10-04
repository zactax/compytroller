import pytest
import httpx
from data.resources.sales_tax.marketplace_provider import MarketplaceProvider
from data.responses.sales_tax import MarketplaceProviderData
from data.exceptions import HttpError, InvalidRequest


CSV_SAMPLE = """Taxpayer Number,Taxpayer Name,Begin Date,End Date
123456789,ACME INC,2020-01-01,2021-01-01
987654321,FOO LLC,2019-06-15,
"""


def test_marketplace_provider_parsing(monkeypatch):
    class FakeResp:
        text = CSV_SAMPLE
        def raise_for_status(self): return None
    class FakeClient:
        def get(self, url): return FakeResp()

    mp = MarketplaceProvider()
    mp.client = FakeClient()
    records = mp.get()

    assert len(records) == 2
    r1 = records[0]
    assert isinstance(r1, MarketplaceProviderData)
    assert r1.taxpayer_number == "123456789"
    assert r1.name == "ACME INC"
    assert r1.begin_date.year == 2020
    assert r1.end_date.year == 2021

    r2 = records[1]
    assert r2.taxpayer_number == "987654321"
    assert r2.end_date is None


def test_marketplace_provider_http_status_error():
    class FailingClient:
        def get(self, url):
            req = httpx.Request("GET", url)
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("server error", request=req, response=resp)

    mp = MarketplaceProvider()
    mp.client = FailingClient()
    with pytest.raises(HttpError):
        mp.get()


def test_marketplace_provider_request_error():
    class FailingClient:
        def get(self, url):
            raise httpx.RequestError("network down", request=httpx.Request("GET", url))

    mp = MarketplaceProvider()
    mp.client = FailingClient()
    with pytest.raises(HttpError):
        mp.get()


def test_marketplace_provider_empty_csv():
    class FakeResp:
        text = "Taxpayer Number,Taxpayer Name,Begin Date,End Date\n"
        def raise_for_status(self): return None
    class FakeClient:
        def get(self, url): return FakeResp()

    mp = MarketplaceProvider()
    mp.client = FakeClient()
    with pytest.raises(InvalidRequest):
        mp.get()


def test_marketplace_providerdata_from_dict():
    data = {
        "Taxpayer Number": "5555",
        "Taxpayer Name": "TEST INC ",
        "Begin Date": "2022-05-01",
        "End Date": "",
    }
    dto = MarketplaceProviderData.from_dict(data)

    assert isinstance(dto, MarketplaceProviderData)
    assert dto.taxpayer_number == "5555"
    assert dto.name == "TEST INC"  # strips whitespace
    assert dto.begin_date.year == 2022
    assert dto.end_date is None
