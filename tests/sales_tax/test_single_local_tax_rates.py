from src.compytroller.responses.sales_tax import SingleLocalTaxRateData
import pytest
import httpx
from src.compytroller.resources.sales_tax.single_local_tax_rates import SingleLocalTaxRates
from src.compytroller.exceptions import HttpError, InvalidRequest


CSV_SAMPLE = """Taxpayer Number,Taxpayer Name,Begin Date,End Date
123456789,ACME INC,2020-01-01,2021-01-01
987654321,FOO LLC,2019-06-15,
"""


def test_single_local_tax_rates_parsing(monkeypatch):
    class FakeResp:
        text = CSV_SAMPLE
        def raise_for_status(self): return None

    class FakeClient:
        def get(self, url): return FakeResp()

    sltr = SingleLocalTaxRates()
    sltr.client = FakeClient()
    records = sltr.get_all()

    assert len(records) == 2
    r1 = records[0]
    assert isinstance(r1, SingleLocalTaxRateData)
    assert r1.taxpayer_number == "123456789"
    assert r1.name == "ACME INC"
    assert r1.begin_date.year == 2020
    assert r1.end_date.year == 2021

    r2 = records[1]
    assert r2.taxpayer_number == "987654321"
    assert r2.end_date is None


def test_single_local_tax_rates_http_status_error():
    class FailingClient:
        def get(self, url):
            req = httpx.Request("GET", url)
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("server error", request=req, response=resp)

    sltr = SingleLocalTaxRates()
    sltr.client = FailingClient()
    with pytest.raises(HttpError):
        sltr.get_all()


def test_single_local_tax_rates_request_error():
    class FailingClient:
        def get(self, url):
            raise httpx.RequestError("network down", request=httpx.Request("GET", url))

    sltr = SingleLocalTaxRates()
    sltr.client = FailingClient()
    with pytest.raises(HttpError):
        sltr.get_all()


def test_single_local_tax_rates_empty_csv(monkeypatch):
    class FakeResp:
        text = "Taxpayer Number,Taxpayer Name,Begin Date,End Date\n"
        def raise_for_status(self): return None

    class FakeClient:
        def get(self, url): return FakeResp()

    sltr = SingleLocalTaxRates()
    sltr.client = FakeClient()
    with pytest.raises(InvalidRequest):
        sltr.get_all()


def test_single_local_tax_rate_data_from_dict_handles_bad_values():
    data = {
        "taxpayer_number": "111111111",
        "name": "BAD INC",
        "begin_date": "not-a-date",
        "end_date": None,
    }
    dto = SingleLocalTaxRateData.from_dict(data)
    assert dto.begin_date is None
    assert dto.end_date is None
    assert dto.name == "BAD INC"


def test_single_local_tax_rates_get_after_date():
    CSV_FILTERED = """Taxpayer Number,Taxpayer Name,Begin Date,End Date
123,EARLY INC,2020-01-01,2021-01-01
456,LATE LLC,2023-06-15,
"""
    class FakeResp:
        text = CSV_FILTERED
        def raise_for_status(self): return None
    class FakeClient:
        def get(self, url): return FakeResp()

    sltr = SingleLocalTaxRates()
    sltr.client = FakeClient()
    records = sltr.get_after_date("2022-01-01")

    # Only LATE LLC should be returned (begin_date > 2022-01-01)
    assert len(records) == 1
    assert records[0].taxpayer_number == "456"


def test_single_local_tax_rates_get_before_date():
    CSV_FILTERED = """Taxpayer Number,Taxpayer Name,Begin Date,End Date
123,EARLY INC,2020-01-01,2021-01-01
456,LATE LLC,2023-06-15,2024-01-01
"""
    class FakeResp:
        text = CSV_FILTERED
        def raise_for_status(self): return None
    class FakeClient:
        def get(self, url): return FakeResp()

    sltr = SingleLocalTaxRates()
    sltr.client = FakeClient()
    records = sltr.get_before_date("2022-01-01")

    # Only EARLY INC should be returned (end_date < 2022-01-01)
    assert len(records) == 1
    assert records[0].taxpayer_number == "123"
