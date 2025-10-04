import pytest
import httpx
from datetime import date
from data.resources.sales_tax.allocation_payment_detail import LocalAllocationPaymentDetail
from data.responses.sales_tax import LocalAllocationPaymentDetailsData
from data.exceptions import HttpError, InvalidRequest


def test_allocation_payment_detail_parsing(dummy_client):
    sample = [{
        "authority_id": "2005023",
        "authority_name": "ARCHER CITY",
        "allocation_month": "2024-07-01T00:00:00.000",
        "allocation_date": "2024-07-09T00:00:00.000",
        "total_collections": "1000",
        "prior_collections": None,
        "current_collections": "2000.5",
        "future_collections": "",
        "audit_collections": "123.45",
        "unidentified_collections": None,
        "single_local_tax_collections": "50",
        "service_fee": "454.97",
        "current_retainage": "445.87",
        "prior_retainage": "593.14",
        "net_payment": "22440.84",
    }]
    client = dummy_client(sample)
    details = (
        LocalAllocationPaymentDetail(client)
        .where("authority_name", "ARCHER CITY")
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