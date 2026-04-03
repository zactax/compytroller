from src.compytroller.responses.sales_tax import SalesTaxRateData
import pytest
import httpx
from src.compytroller.resources.sales_tax.rates import SalesTaxRates
from src.compytroller.exceptions import HttpError, InvalidRequest


def test_sales_tax_rates_parsing(dummy_client):
    sample = [{
        "type": "CITY",
        "city_name": "Austin",
        "county_name": "Travis",
        "old_rate": "0.015",
        "new_rate": "0.020",
        "effective_date": "2024-01-01",
        "report_month": "1",
        "report_year": "2024",
        "report_period_type": "MONTHLY",
    }]
    client = dummy_client(sample)
    results = (
        SalesTaxRates(client)
        .for_city("Austin")
        .in_county("Travis")
        .for_type("CITY")
        .for_year(2024)
        .sort_by("report_month", desc=True)
        .limit(1)
        .get()
    )

    assert len(results) == 1
    r = results[0]
    assert isinstance(r, SalesTaxRateData)
    assert r.city_name == "Austin"
    assert r.county_name == "Travis"
    assert r.old_rate == 0.015
    assert r.new_rate == 0.020
    assert r.report_month == 1
    assert r.report_year == 2024
    assert r.effective_date == "2024-01-01"


def test_sales_tax_rates_http_status_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            req = httpx.Request("GET", "https://fake")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("server error", request=req, response=resp)

    with pytest.raises(HttpError):
        SalesTaxRates(FailingClient()).get()


def test_sales_tax_rates_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            raise httpx.RequestError("network down", request=httpx.Request("GET", "https://fake"))

    with pytest.raises(HttpError):
        SalesTaxRates(FailingClient()).get()


def test_sales_tax_rates_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        SalesTaxRates(client).get()


def test_sales_tax_rate_data_from_dict_handles_bad_values():
    data = {
        "type": "COUNTY",
        "city_name": None,
        "county_name": "Bexar",
        "old_rate": "not-a-float",
        "new_rate": None,
        "effective_date": None,
        "report_month": "not-an-int",
        "report_year": None,
        "report_period_type": None,
    }
    dto = SalesTaxRateData.from_dict(data)
    assert dto.old_rate is None
    assert dto.new_rate is None
    assert dto.report_month is None
    assert dto.report_year is None
    assert dto.county_name == "Bexar"


def test_sales_tax_rates_reset(dummy_client):
    sample = [{"city_name": "Austin"}]
    client = dummy_client(sample)
    resource = SalesTaxRates(client)
    resource.for_city("Austin").for_year(2024).sort_by("report_month")
    assert len(resource._params) > 0

    resource.reset()
    assert resource._params == {}
