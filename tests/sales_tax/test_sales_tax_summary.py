import pytest
import httpx
from compytroller.resources.sales_tax.city_county_comparison_summary import CityCountyComparisonSummary
from compytroller.responses.sales_tax import ComparisonSummaryData
from compytroller.exceptions import HttpError, InvalidRequest

## FIX
def test_comparison_summary_parsing(dummy_client):
    sample = [{
        "city": "Austin",
        "county": "Travis",
        "type": "CITY",
        "year": "2024",
        "month": "01",
        "net_payment_this_period": "12345.67",
    }]
    client = dummy_client(sample)
    summaries = (
        CityCountyComparisonSummary(client)
        .for_city("Austin")
        .in_county("Travis")
        .sort_by("year", desc=True)
        .limit(5)
        .get()
    )

    assert len(summaries) == 1
    s = summaries[0]
    assert isinstance(s, ComparisonSummaryData)
    assert s.city == "Austin"
    assert s.net_payment_this_period == 12345.67


def test_comparison_summary_http_status_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            req = httpx.Request("GET", "https://fake")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("Server error", request=req, response=resp)

    with pytest.raises(HttpError):
        CityCountyComparisonSummary(FailingClient()).get()


def test_comparison_summary_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            raise httpx.RequestError("Network down", request=httpx.Request("GET", "https://fake"))

    with pytest.raises(HttpError):
        CityCountyComparisonSummary(FailingClient()).get()


def test_comparison_summary_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        CityCountyComparisonSummary(client).get()


def test_comparison_summary_reset(dummy_client):
    sample = [{"city": "Austin"}]
    client = dummy_client(sample)
    resource = CityCountyComparisonSummary(client)
    resource.for_city("Austin").in_county("Travis").sort_by("year")
    assert len(resource._params) > 0

    resource.reset()
    assert resource._params == {}
