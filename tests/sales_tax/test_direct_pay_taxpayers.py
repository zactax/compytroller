import pytest
import httpx
from datetime import date
from src.data.resources.sales_tax.direct_pay import DirectPayTaxpayers, DirectPayTaxpayerData
from src.data.exceptions import HttpError, InvalidRequest


def test_direct_pay_parsing(dummy_client):
    sample = [{
        "id": "1",
        "name": "BIG RETAIL INC",
        "address": "123 MAIN ST",
        "city": "Austin",
        "state": "TX",
        "zip": "78701",
        "county": "TRAVIS",
        "business_type": "Retail",
        "naics_code": "445120",
        "responsibility_begin_date": "2020-01-15T00:00:00.000",
    }]
    client = dummy_client(sample)
    taxpayers = (
        DirectPayTaxpayers(client)
        .with_naics("445120")
        .for_city("austin")
        .in_county("travis")
        .sort_by("name", desc=True)
        .limit(10)
        .get()
    )

    assert len(taxpayers) == 1
    t = taxpayers[0]
    assert isinstance(t, DirectPayTaxpayerData)
    assert t.name == "BIG RETAIL INC"
    assert t.city == "Austin"
    assert t.responsibility_begin_date == date(2020, 1, 15)


def test_direct_pay_http_status_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            req = httpx.Request("GET", "https://fake")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("Server error", request=req, response=resp)

    with pytest.raises(HttpError):
        DirectPayTaxpayers(FailingClient()).get()


def test_direct_pay_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            raise httpx.RequestError("Network down", request=httpx.Request("GET", "https://fake"))

    with pytest.raises(HttpError):
        DirectPayTaxpayers(FailingClient()).get()


def test_direct_pay_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        DirectPayTaxpayers(client).get()


def test_direct_pay_reset(dummy_client):
    sample = [{"name": "TEST"}]
    client = dummy_client(sample)
    resource = DirectPayTaxpayers(client)
    resource.with_naics("445120").for_city("Austin").sort_by("name")
    assert len(resource._params) > 0

    resource.reset()
    assert resource._params == {}
