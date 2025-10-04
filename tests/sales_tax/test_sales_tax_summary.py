import pytest
import httpx
from data.resources.sales_tax.comparison_summary import ComparisonSummary
from data.responses.sales_tax import ComparisonSummaryData
from data.exceptions import HttpError, InvalidRequest


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
        ComparisonSummary(client, "cities")
        .for_city("Austin")
        .for_county("Travis")
        .for_type("city")
        .where("extra_field", "X")
        .sort_by("year", desc=True)
        .limit(5)
        .get()
    )

    assert len(summaries) == 1
    s = summaries[0]
    assert isinstance(s, ComparisonSummaryData)
    assert s.jurisdiction == "Austin"
    assert s.net_payment_this_period == 12345.67


def test_comparison_summary_invalid_type(dummy_client):
    with pytest.raises(ValueError):
        ComparisonSummary(dummy_client, "bad_type")


def test_comparison_summary_http_status_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            req = httpx.Request("GET", "https://fake")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("Server error", request=req, response=resp)

    with pytest.raises(HttpError):
        ComparisonSummary(FailingClient(), "cities").get()


def test_comparison_summary_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            raise httpx.RequestError("Network down", request=httpx.Request("GET", "https://fake"))

    with pytest.raises(HttpError):
        ComparisonSummary(FailingClient(), "cities").get()


def test_comparison_summary_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        ComparisonSummary(client, "cities").get()
