from src.data.responses.sales_tax import PermittedLocationData
import pytest
import httpx
from datetime import date
from src.data.resources.sales_tax.permitted_locations import PermittedLocations
from src.data.exceptions import HttpError, InvalidRequest


def test_permitted_locations_parsing(dummy_client):
    sample = [{
        "tp_number": "123456789",
        "tp_name": "BIG CO INC",
        "tp_address": "123 MAIN ST",
        "tp_city": "Austin",
        "tp_state": "TX",
        "tp_zip": "78701",
        "tp_county": "TRAVIS",
        "org_type": "CORP",
        "loc_number": "L001",
        "loc_name": "BIG CO WAREHOUSE",
        "loc_city": "Austin",
        "loc_state": "TX",
        "loc_zip": "78701",
        "loc_county": "TRAVIS",
        "naics": "445120",
        "juris_city": "Austin",
        "city_taid": "123",
        "mass_transit_auth1_taid": "MTA1",
        "mass_transit_auth2_taid": "MTA2",
        "county_taid": "CNTY1",
        "special_purp_dist1_taid": "SPD1",
        "special_purp_dist2_taid": "SPD2",
        "special_purp_dist3_taid": "SPD3",
        "special_purp_dist4_taid": "SPD4",
        "unique_taid": "U001",
        "first_sale_date": "2020-01-15T00:00:00.000",
        "out_of_business_date": "2021-06-01T00:00:00.000",
    }]
    client = dummy_client(sample)
    results = (
        PermittedLocations(client)
        .in_city("austin")
        .with_naics("445120")
        .with_tp_number("123456789")
        .with_city_taid("123")
        .with_county_taid("CNTY1")
        .with_mta_taid("MTA1", slot=1)
        .with_spd_taid("SPD1", slot=2)
        .sort_by("tp_name", desc=True)
        .limit(10)
        .get()
    )

    assert len(results) == 1
    loc = results[0]
    assert isinstance(loc, PermittedLocationData)
    assert loc.tp_name == "BIG CO INC"
    assert loc.loc_name == "BIG CO WAREHOUSE"
    assert loc.first_sale_date == date(2020, 1, 15)
    assert loc.out_of_business_date == date(2021, 6, 1)


def test_permitted_locations_http_status_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            req = httpx.Request("GET", "https://fake")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("server error", request=req, response=resp)

    with pytest.raises(HttpError):
        PermittedLocations(FailingClient()).get()


def test_permitted_locations_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            raise httpx.RequestError("network down", request=httpx.Request("GET", "https://fake"))

    with pytest.raises(HttpError):
        PermittedLocations(FailingClient()).get()


def test_permitted_locations_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        PermittedLocations(client).get()


def test_permitted_locationdata_from_dict_handles_bad_dates():
    data = {
        "tp_number": "123",
        "tp_name": "BAD DATES INC",
        "tp_address": "X",
        "tp_city": "Y",
        "tp_state": "TX",
        "tp_zip": "00000",
        "tp_county": "Z",
        "loc_number": "L",
        "loc_name": "Store",
        "loc_city": "Y",
        "loc_state": "TX",
        "loc_zip": "00000",
        "loc_county": "Z",
        "first_sale_date": "not-a-date",
        "out_of_business_date": None,
    }
    dto = PermittedLocationData.from_dict(data)
    assert dto.first_sale_date is None
    assert dto.out_of_business_date is None


def test_permitted_locations_limit(dummy_client):
    sample = [{"tp_name": "TEST"}]
    client = dummy_client(sample)
    resource = PermittedLocations(client)
    resource.limit(100)
    assert resource._params["$limit"] == 100


def test_permitted_locations_reset(dummy_client):
    sample = [{"tp_name": "TEST"}]
    client = dummy_client(sample)
    resource = PermittedLocations(client)
    resource.in_city("Austin").with_naics("445120").limit(100)
    assert len(resource._params) > 0

    resource.reset()
    assert resource._params == {}

