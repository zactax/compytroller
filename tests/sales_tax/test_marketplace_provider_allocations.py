import pytest
import httpx
from data.resources.sales_tax.marketplace_provider_allocations import MarketplaceProviderAllocations
from data.responses.sales_tax import MarketplaceProviderAllocationData
from data.exceptions import HttpError, InvalidRequest


def test_marketplace_provider_allocations_parsing(dummy_client):
    sample = [{
        "authority_type": "CITY",
        "authority_id": "1001",
        "authority_name": "Austin",
        "allocation_year": "2023",
        "allocation_month": "5",
        "amount_allocated": "12345.67",
    }]
    client = dummy_client(sample)
    results = (
        MarketplaceProviderAllocations(client)
        .for_authority("Austin")
        .for_type("city")
        .for_year(2023)
        .sort_by("allocation_year", desc=True)
        .limit(10)
        .get()
    )

    assert len(results) == 1
    r = results[0]
    assert isinstance(r, MarketplaceProviderAllocationData)
    assert r.authority_type == "CITY"
    assert r.authority_id == "1001"
    assert r.authority_name == "Austin"
    assert r.allocation_year == 2023
    assert r.allocation_month == 5
    assert r.amount_allocated == 12345.67


def test_marketplace_provider_allocations_http_status_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            req = httpx.Request("GET", "https://fake")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("server error", request=req, response=resp)

    with pytest.raises(HttpError):
        MarketplaceProviderAllocations(FailingClient()).get()


def test_marketplace_provider_allocations_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            raise httpx.RequestError("network down", request=httpx.Request("GET", "https://fake"))

    with pytest.raises(HttpError):
        MarketplaceProviderAllocations(FailingClient()).get()


def test_marketplace_provider_allocations_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        MarketplaceProviderAllocations(client).get()
