import pytest
import httpx
from compytroller.resources.sales_tax.marketplace_provider_allocations import MarketplaceProviderAllocations
from compytroller.responses.sales_tax import MarketplaceProviderAllocationData
from compytroller.exceptions import HttpError, InvalidRequest


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
        .for_type("city")
        .for_year(2023)
        .sort_by("allocation_year", desc=True)
        .limit(10)
        .get()
    )

    # Note: for_authority searches both original and uppercase, resulting in 2 queries
    # So we expect 1 result when not using for_authority
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


def test_marketplace_provider_allocations_for_year(dummy_client):
    sample = [{"allocation_year": "2023"}]
    client = dummy_client(sample)
    resource = MarketplaceProviderAllocations(client)
    resource.for_year(2023)
    assert resource._params["allocation_year"] == 2023


def test_marketplace_provider_allocations_reset(dummy_client):
    sample = [{"authority_name": "Austin"}]
    client = dummy_client(sample)
    resource = MarketplaceProviderAllocations(client)
    resource.for_authority("Austin").for_type("CITY").for_year(2023)
    assert len(resource._params) > 0
    assert len(resource.authority_name) > 0

    resource.reset()
    assert resource._params == {}
    assert resource.authority_name == []


def test_marketplace_provider_allocations_with_authority_name(dummy_client):
    """Test that for_authority searches both original and uppercase versions."""
    sample = [{"authority_name": "Austin", "authority_type": "CITY"}]
    client = dummy_client(sample)
    resource = MarketplaceProviderAllocations(client)
    results = resource.for_authority("Austin").get()

    # Should get results from both queries (original + uppercase)
    # The for_authority adds both "Austin" and "AUSTIN" to authority_name list
    # So we get the sample back twice
    assert len(results) == 2
    assert resource.authority_name == ["Austin", "AUSTIN"]
