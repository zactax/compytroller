from data.responses.sales_tax import SingleLocalAllocationData
import pytest
import httpx
from data.resources.sales_tax.single_local_allocations import SingleLocalAllocations
from data.exceptions import HttpError, InvalidRequest


def test_single_local_allocations_parsing(dummy_client):
    sample = [{
        "authority_type": "CITY",
        "tax_authority": "Austin",
        "report_year": "2024",
        "report_month": "6",
        "current_net_payment": "12345.67",
        "prior_year_net_payment": "11111.11",
        "yoy_percent_change": "11.11",
        "payment_ytd": "98765.43",
        "prior_year_payment_ytd": "87654.32",
        "ytd_percent_change": "12.34",
    }]
    client = dummy_client(sample)
    results = (
        SingleLocalAllocations(client)
        .for_authority("Austin")
        .for_type("city")
        .for_year(2024)
        .sort_by("report_month", desc=True)
        .limit(1)
        .get()
    )

    assert len(results) == 1
    r = results[0]
    assert isinstance(r, SingleLocalAllocationData)
    assert r.tax_authority == "Austin"
    assert r.authority_type == "CITY"  # uppercased in for_type
    assert r.report_year == 2024
    assert r.report_month == 6
    assert r.current_net_payment == 12345.67
    assert r.yoy_percent_change == 11.11
    assert r.payment_ytd == 98765.43


def test_single_local_allocations_http_status_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            req = httpx.Request("GET", "https://fake")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("server error", request=req, response=resp)

    with pytest.raises(HttpError):
        SingleLocalAllocations(FailingClient()).get()


def test_single_local_allocations_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            raise httpx.RequestError("network down", request=httpx.Request("GET", "https://fake"))

    with pytest.raises(HttpError):
        SingleLocalAllocations(FailingClient()).get()


def test_single_local_allocations_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        SingleLocalAllocations(client).get()


def test_single_local_allocation_data_from_dict_handles_bad_values():
    data = {
        "authority_type": "COUNTY",
        "tax_authority": "Travis",
        "report_year": "not-an-int",
        "report_month": None,
        "current_net_payment": "bad-float",
        "prior_year_net_payment": None,
        "yoy_percent_change": "NaN",
        "payment_ytd": "",
        "prior_year_payment_ytd": "12345.67",
        "ytd_percent_change": None,
    }
    dto = SingleLocalAllocationData.from_dict(data)

    assert dto.report_year is None
    assert dto.report_month is None
    assert dto.current_net_payment is None
    assert dto.prior_year_net_payment is None
    assert dto.yoy_percent_change is None
    assert dto.payment_ytd is None
    assert dto.prior_year_payment_ytd == 12345.67
    assert dto.ytd_percent_change is None

