import pytest
import httpx
from src.compytroller.resources.sales_tax.marketplace_provider import MarketplaceProvider
from src.compytroller.responses.sales_tax import MarketplaceProviderData
from src.compytroller.exceptions import HttpError, InvalidRequest


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


def test_marketplace_provider_from_date():
    CSV_FILTERED = """Taxpayer Number,Taxpayer Name,Begin Date,End Date
123,EARLY INC,2020-01-01,2021-01-01
456,LATE LLC,2023-06-15,
"""
    class FakeResp:
        text = CSV_FILTERED
        def raise_for_status(self): return None
    class FakeClient:
        def get(self, url): return FakeResp()

    mp = MarketplaceProvider()
    mp.client = FakeClient()
    records = mp.after_date("2022-01-01").get()

    # Only LATE LLC should be returned (begin_date > 2022-01-01)
    assert len(records) == 1
    assert records[0].taxpayer_number == "456"


def test_marketplace_provider_to_date():
    CSV_FILTERED = """Taxpayer Number,Taxpayer Name,Begin Date,End Date
123,EARLY INC,2020-01-01,2021-01-01
456,LATE LLC,2023-06-15,2024-01-01
"""
    class FakeResp:
        text = CSV_FILTERED
        def raise_for_status(self): return None
    class FakeClient:
        def get(self, url): return FakeResp()

    mp = MarketplaceProvider()
    mp.client = FakeClient()
    records = mp.before_date("2022-01-01").get()

    # Only EARLY INC should be returned (end_date < 2022-01-01)
    assert len(records) == 1
    assert records[0].taxpayer_number == "123"


def test_marketplace_provider_reset():
    mp = MarketplaceProvider()
    mp.after_date("2022-01-01").before_date("2023-01-01")
    assert len(mp.instructions) > 0

    mp.reset()
    assert mp.instructions == {}
