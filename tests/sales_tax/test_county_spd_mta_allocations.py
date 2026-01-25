import pytest
import httpx
from data.resources.sales_tax.county_spd_mta_allocations import CountySPDMTAAllocations
from src.data.responses.sales_tax import CountySPDMTAAllocationData
from src.data.exceptions import HttpError, InvalidRequest


def test_county_spd_mta_allocations_parsing(dummy_client):
    sample = [{
        "type": "COUNTY",
        "name": "Travis",
        "allocation_amount": "12345.67",
        "allocation_year": "2023",
        "allocation_month": "6",
    }]
    client = dummy_client(sample)
    results = (
        CountySPDMTAAllocations(client)
        .for_type("County")
        .with_name("Travis")
        .sort_by("allocation_year", desc=True)
        .limit(10)
        .get()
    )

    assert len(results) == 1
    r = results[0]
    assert isinstance(r, CountySPDMTAAllocationData)
    assert r.jurisdiction_type == "COUNTY"
    assert r.name == "Travis"


def test_county_spd_mta_allocations_in_county(dummy_client):
    sample = [{"type": "COUNTY", "name": "Travis"}]
    client = dummy_client(sample)
    resource = CountySPDMTAAllocations(client)
    resource.for_type("County")
    assert resource._params["type"] == "COUNTY"


def test_county_spd_mta_allocations_for_city(dummy_client):
    sample = [{"type": "CITY", "name": "Austin"}]
    client = dummy_client(sample)
    resource = CountySPDMTAAllocations(client)
    resource.for_type("City").with_name("Austin")
    assert resource._params["type"] == "CITY"
    assert resource._params["name"] == "Austin"


def test_county_spd_mta_allocations_for_mta(dummy_client):
    sample = [{"type": "MTA", "name": "MTA-123"}]
    client = dummy_client(sample)
    resource = CountySPDMTAAllocations(client)
    resource.for_type("MTA").with_name("MTA-123")
    assert resource._params["type"] == "MTA"


def test_county_spd_mta_allocations_for_spd(dummy_client):
    sample = [{"type": "SPD", "name": "SPD-456"}]
    client = dummy_client(sample)
    resource = CountySPDMTAAllocations(client)
    resource.for_type("SPD").with_name("SPD-456")
    assert resource._params["type"] == "SPD"


def test_county_spd_mta_allocations_sort_by(dummy_client):
    sample = [{"type": "COUNTY"}]
    client = dummy_client(sample)
    resource = CountySPDMTAAllocations(client)
    resource.sort_by("allocation_year", desc=True)
    assert resource._params["$order"] == "allocation_year DESC"

    resource.sort_by("allocation_year", desc=False)
    assert resource._params["$order"] == "allocation_year"


def test_county_spd_mta_allocations_limit(dummy_client):
    sample = [{"type": "COUNTY"}]
    client = dummy_client(sample)
    resource = CountySPDMTAAllocations(client)
    resource.limit(50)
    assert resource._params["$limit"] == 50


def test_county_spd_mta_allocations_reset(dummy_client):
    sample = [{"type": "COUNTY"}]
    client = dummy_client(sample)
    resource = CountySPDMTAAllocations(client)
    resource.for_type("County").with_name("Travis").sort_by("allocation_year")
    assert len(resource._params) > 0

    resource.reset()
    assert resource._params == {}


def test_county_spd_mta_allocations_http_status_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            req = httpx.Request("GET", "https://fake")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("server error", request=req, response=resp)

    with pytest.raises(HttpError):
        CountySPDMTAAllocations(FailingClient()).get()


def test_county_spd_mta_allocations_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            raise httpx.RequestError("network down", request=httpx.Request("GET", "https://fake"))

    with pytest.raises(HttpError):
        CountySPDMTAAllocations(FailingClient()).get()


def test_county_spd_mta_allocations_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        CountySPDMTAAllocations(client).get()
