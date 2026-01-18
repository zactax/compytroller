import pytest
import httpx
from datetime import date
from src.data.resources.sales_tax.allocation_payment_detail import LocalAllocationPaymentDetail
from src.data.responses.sales_tax import LocalAllocationPaymentDetailsData
from src.data.exceptions import HttpError, InvalidRequest


def test_allocation_payment_detail_parsing(dummy_client):
    sample = [{
        "authority_id": "2005023",
        "authority_name": "ARCHER CITY",
        "allocation_month": "2024-07-01T00:00:00.000",
        "allocation_date": "2024-07-09T00:00:00.000",
        "total_coll": "1000",
        "prior_coll": None,
        "current_coll": "2000.5",
        "future_coll": "",
        "audit_coll": "123.45",
        "unidentified_coll": None,
        "single_local_tax_coll": "50",
        "service_fee": "454.97",
        "current_retainage": "445.87",
        "prior_retainage": "593.14",
        "net_payment": "22440.84",
    }]
    client = dummy_client(sample)
    details = (
        LocalAllocationPaymentDetail(client)
        .with_authority_id("2005023")
        .sort_by("allocation_date", desc=True)
        .limit(5)
        .get()
    )

    assert len(details) == 1
    d = details[0]
    assert isinstance(d, LocalAllocationPaymentDetailsData)

    # Strings -> fields
    assert d.authority_id == "2005023"
    assert d.authority_name == "ARCHER CITY"

    # Dates
    assert isinstance(d.allocation_month, date)
    assert d.allocation_month.year == 2024 and d.allocation_month.month == 7
    assert isinstance(d.allocation_date, date)
    assert d.allocation_date.day == 9

    # Floats
    assert d.total_collections == 1000.0
    assert d.current_collections == 2000.5
    assert d.audit_collections == 123.45
    assert d.single_local_tax_collections == 50.0
    assert d.service_fee == 454.97
    assert d.current_retainage == 445.87
    assert d.prior_retainage == 593.14
    assert d.net_payment == 22440.84

    # Missing/empty -> None
    assert d.prior_collections is None
    assert d.future_collections is None
    assert d.unidentified_collections is None


def test_allocation_payment_detail_http_status_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            req = httpx.Request("GET", "https://fake")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("Server error", request=req, response=resp)

    with pytest.raises(HttpError):
        LocalAllocationPaymentDetail(FailingClient()).get()


def test_allocation_payment_detail_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            raise httpx.RequestError("Network fail", request=httpx.Request("GET", "https://fake"))

    with pytest.raises(HttpError):
        LocalAllocationPaymentDetail(FailingClient()).get()


def test_allocation_payment_detail_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        LocalAllocationPaymentDetail(client).get()


def test_allocation_payment_detail_sort_by(dummy_client):
    sample = [{"authority_id": "123", "authority_name": "TEST"}]
    client = dummy_client(sample)
    resource = LocalAllocationPaymentDetail(client)
    resource.sort_by("allocation_date", desc=True)
    assert resource._params["$order"] == "allocation_date DESC"

    resource.sort_by("allocation_date", desc=False)
    assert resource._params["$order"] == "allocation_date"


def test_allocation_payment_detail_reset(dummy_client):
    sample = [{"authority_id": "123"}]
    client = dummy_client(sample)
    resource = LocalAllocationPaymentDetail(client)
    resource.with_authority_id("123").sort_by("allocation_date")
    assert len(resource._params) > 0

    resource.reset()
    assert resource._params == {}


def test_allocation_payment_detail_for_city(dummy_client):
    sample = [{"authority_name": "AUSTIN"}]
    client = dummy_client(sample)
    resource = LocalAllocationPaymentDetail(client)
    resource.for_city("Austin")
    assert resource._params["authority_name"] == "'AUSTIN'"


def test_allocation_payment_detail_for_month(dummy_client):
    sample = [{"allocation_month": "2024-01-01T00:00:00"}]
    client = dummy_client(sample)
    resource = LocalAllocationPaymentDetail(client)
    resource.for_month("2024-01-01T00:00:00")
    assert resource._params["allocation_month"] == "'2024-01-01T00:00:00'"