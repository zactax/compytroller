import pytest
import httpx
from data.resources.sales_tax.active_permits import ActivePermits
from data.responses.sales_tax import ActivePermitData
from data.exceptions import HttpError, InvalidRequest


def test_active_permits_parsing(dummy_client):
    sample = [{
        "taxpayer_number": "123",
        "outlet_number": "1",
        "outlet_name": "ABC STORE",
        "outlet_address": "123 MAIN ST",
        "outlet_city": "Austin",
        "outlet_state": "TX",
        "outlet_zip": "78701",
        "outlet_county_code": "227",
        "outlet_permit_issue_date": "2020-01-01T00:00:00.000",
        "outlet_first_sales_date": "2020-02-01T00:00:00.000",
        "outlet_naics_code": "445120",
    }]
    client = dummy_client(sample)
    permits = (
        ActivePermits(client)
        .for_taxpayer("123")
        .in_city("Austin")
        .in_county("227")
        .with_naics("445120")
        .issued_after("2019-01-01")
        .first_sale_after("2019-02-01")
        .between_issue_dates("2019-01-01", "2021-01-01")
        .sort_by("outlet_city", desc=True)
        .limit(10)
        .get()
    )

    assert len(permits) == 1
    p = permits[0]
    assert isinstance(p, ActivePermitData)
    assert p.outlet_city == "Austin"
    assert p.outlet_naics_code == "445120"


def test_active_permits_http_status_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            req = httpx.Request("GET", "https://fake")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("Server error", request=req, response=resp)

    with pytest.raises(HttpError):
        ActivePermits(FailingClient()).get()


def test_active_permits_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            raise httpx.RequestError("Network error", request=httpx.Request("GET", "https://fake"))

    with pytest.raises(HttpError):
        ActivePermits(FailingClient()).get()


def test_active_permits_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        ActivePermits(client).get()
