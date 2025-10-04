import pytest
import httpx
from data.resources.mixed_beverage.gross_receipts import MixedBeverageGrossReceipts
from data.responses.mixed_beverage_tax import MixedBeverageGrossReceiptsData
from data.exceptions import HttpError, InvalidRequest


def test_mixed_beverage_parsing(dummy_client):
    sample = [{
        "taxpayer_number": "17604990295",
        "taxpayer_name": "BUFFARE CORPORATION",
        "taxpayer_address": "4408 W 12TH ST",
        "taxpayer_city": "HOUSTON",
        "taxpayer_state": "TX",
        "taxpayer_zip": "77055",
        "location_name": "ARCODORO",
        "location_address": "5000 WESTHEIMER RD STE 120",
        "location_city": "HOUSTON",
        "location_state": "TX",
        "location_zip": "77056",
        "inside_outside_city_limits_code_y_n": "Y",
        "tabc_permit_number": "MB267335",
        "responsibility_begin_date_yyyymmdd": "1996-07-16T00:00:00.000",
        "responsibility_end_date_yyyymmdd": "2018-04-03T00:00:00.000",
        "obligation_end_date_yyyymmdd": "2014-04-30T00:00:00.000",
        "liquor_receipts": "24817",
        "wine_receipts": "61844",
        "beer_receipts": "6161",
        "cover_charge_receipts": "0",
        "total_receipts": "92822",
    }]
    client = dummy_client(sample)
    receipts = MixedBeverageGrossReceipts(client).get_all()
    assert len(receipts) == 1
    r = receipts[0]
    assert isinstance(r, MixedBeverageGrossReceiptsData)
    assert r.tp_name == "BUFFARE CORPORATION"
    assert r.total_receipts == 92822.0


def test_mixed_beverage_http_status_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            req = httpx.Request("GET", "https://data.texas.gov")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("Server error", request=req, response=resp)

    with pytest.raises(HttpError):
        MixedBeverageGrossReceipts(FailingClient()).get_all()


def test_mixed_beverage_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            raise httpx.RequestError("Connection error", request=httpx.Request("GET", "https://data.texas.gov"))

    with pytest.raises(HttpError):
        MixedBeverageGrossReceipts(FailingClient()).get_all()


def test_mixed_beverage_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        MixedBeverageGrossReceipts(client).get_all()
