import pytest
import httpx
from data.resources.franchise.active_permit_holders import ActiveFranchiseTaxPermitHolders
from data.responses.franchise_tax import FranchiseTaxPermitHolderData
from data.exceptions import HttpError, InvalidRequest


def test_active_permit_holders_parsing(dummy_client):
    sample = [{
        "taxpayer_number": "32094594283",
        "taxpayer_name": "SALUS CURA VENTURES",
        "taxpayer_address": "509 S PACIFIC ST STE 433",
        "taxpayer_city": "MINEOLA",
        "taxpayer_state": "TX",
        "taxpayer_zip": "75773",
        "taxpayer_county_code": "250",
        "taxpayer_organizational_type": "CN",
        "record_type_code": "U",
        "responsibility_beginning_date": "2024-04-10T00:00:00.000",
        "secretary_of_state_sos_or_coa_file_number": "0805503141",
        "sos_charter_date": "2024-04-10T00:00:00.000",
        "sos_status_date": "2024-04-10T00:00:00.000",
        "sos_status_code": "A",
        "right_to_transact_business_code": "A"
    }]
    client = dummy_client(sample)
    holders = ActiveFranchiseTaxPermitHolders(client).get_all()
    assert len(holders) == 1
    holder = holders[0]
    assert isinstance(holder, FranchiseTaxPermitHolderData)
    assert holder.taxpayer_name == "SALUS CURA VENTURES"
    assert holder.responsibility_beginning_date.year == 2024


def test_active_permit_holders_http_status_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            req = httpx.Request("GET", "https://data.texas.gov")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("Server error", request=req, response=resp)

    with pytest.raises(HttpError) as excinfo:
        ActiveFranchiseTaxPermitHolders(FailingClient()).get_all()
    assert "Server error" in str(excinfo.value)
    assert excinfo.value.status_code == 500


def test_active_permit_holders_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            # Simulate a low-level network error
            raise httpx.RequestError("Connection error", request=httpx.Request("GET", "https://data.texas.gov"))

    with pytest.raises(HttpError) as excinfo:
        ActiveFranchiseTaxPermitHolders(FailingClient()).get_all()
    assert "Connection error" in str(excinfo.value)


def test_active_permit_holders_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        ActiveFranchiseTaxPermitHolders(client).get_all()
