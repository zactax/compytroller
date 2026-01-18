import pytest
import httpx
from src.data.resources.franchise.active_permit_holders import ActiveFranchiseTaxPermitHolders
from src.data.responses.franchise_tax import FranchiseTaxPermitHolderData
from src.data.exceptions import HttpError, InvalidRequest


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
    holders = ActiveFranchiseTaxPermitHolders(client).get()
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
        ActiveFranchiseTaxPermitHolders(FailingClient()).get()
    assert "Server error" in str(excinfo.value)
    assert excinfo.value.status_code == 500


def test_active_permit_holders_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            # Simulate a low-level network error
            raise httpx.RequestError("Connection error", request=httpx.Request("GET", "https://data.texas.gov"))

    with pytest.raises(HttpError) as excinfo:
        ActiveFranchiseTaxPermitHolders(FailingClient()).get()
    assert "Connection error" in str(excinfo.value)


def test_active_permit_holders_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        ActiveFranchiseTaxPermitHolders(client).get()


def test_active_permit_holders_for_taxpayer(dummy_client):
    sample = [{
        "taxpayer_number": "12345678901",
        "taxpayer_name": "TEST CORP",
        "taxpayer_city": "AUSTIN",
    }]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.for_taxpayer("12345678901")
    assert resource._params["taxpayer_number"] == "12345678901"


def test_active_permit_holders_in_city(dummy_client):
    sample = [{"taxpayer_name": "TEST"}]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.in_city("Austin")
    assert resource._params["taxpayer_city"] == "AUSTIN"


def test_active_permit_holders_for_org_type(dummy_client):
    sample = [{"taxpayer_name": "TEST"}]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.for_org_type("ct")
    assert resource._params["taxpayer_organizational_type"] == "CT"


def test_active_permit_holders_with_right_to_transact(dummy_client):
    sample = [{"taxpayer_name": "TEST"}]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.with_right_to_transact("a")
    assert resource._params["right_to_transact_business_code"] == "A"


def test_active_permit_holders_with_exempt_reason(dummy_client):
    sample = [{"taxpayer_name": "TEST"}]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.with_exempt_reason("01")
    assert resource._params["current_exempt_reason_code"] == "01"


def test_active_permit_holders_responsibility_start_before(dummy_client):
    sample = [{"taxpayer_name": "TEST"}]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.responsibility_start_before("2023-01-01")
    assert "responsibility_beginning_date < '2023-01-01'" in resource._where_clauses


def test_active_permit_holders_responsibility_start_after(dummy_client):
    sample = [{"taxpayer_name": "TEST"}]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.responsibility_start_after("2023-01-01")
    assert "responsibility_beginning_date > '2023-01-01'" in resource._where_clauses


def test_active_permit_holders_responsibility_start_between(dummy_client):
    sample = [{"taxpayer_name": "TEST"}]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.responsibility_start_between("2023-01-01", "2023-12-31")
    assert "responsibility_beginning_date BETWEEN '2023-01-01' AND '2023-12-31'" in resource._where_clauses


def test_active_permit_holders_exempt_begin_before(dummy_client):
    sample = [{"taxpayer_name": "TEST"}]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.exempt_begin_before("2023-01-01")
    assert "exempt_begin_date < '2023-01-01'" in resource._where_clauses


def test_active_permit_holders_exempt_begin_after(dummy_client):
    sample = [{"taxpayer_name": "TEST"}]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.exempt_begin_after("2023-01-01")
    assert "exempt_begin_date > '2023-01-01'" in resource._where_clauses


def test_active_permit_holders_exempt_begin_between(dummy_client):
    sample = [{"taxpayer_name": "TEST"}]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.exempt_begin_between("2023-01-01", "2023-12-31")
    assert "exempt_begin_date BETWEEN '2023-01-01' AND '2023-12-31'" in resource._where_clauses


def test_active_permit_holders_for_naics_code(dummy_client):
    sample = [{"taxpayer_name": "TEST"}]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.for_naics_code("621111")
    assert resource._params["_621111"] == "621111"


def test_active_permit_holders_sort_by(dummy_client):
    sample = [{"taxpayer_name": "TEST"}]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.sort_by("taxpayer_name", desc=True)
    assert resource._params["$order"] == "taxpayer_name DESC"

    resource.sort_by("taxpayer_name", desc=False)
    assert resource._params["$order"] == "taxpayer_name"


def test_active_permit_holders_limit(dummy_client):
    sample = [{"taxpayer_name": "TEST"}]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.limit(10)
    assert resource._params["$limit"] == 10


def test_active_permit_holders_reset(dummy_client):
    sample = [{"taxpayer_name": "TEST"}]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    resource.for_taxpayer("123").in_city("Austin").responsibility_start_before("2023-01-01")
    assert len(resource._params) > 0
    assert len(resource._where_clauses) > 0

    resource.reset()
    assert resource._params == {}
    assert resource._where_clauses == []


def test_active_permit_holders_with_where_clauses(dummy_client):
    """Test that where clauses are properly added to params when get() is called."""
    sample = [{
        "taxpayer_number": "12345678901",
        "taxpayer_name": "TEST CORP",
        "responsibility_beginning_date": "2023-06-01T00:00:00.000",
    }]
    client = dummy_client(sample)
    resource = ActiveFranchiseTaxPermitHolders(client)
    results = resource.responsibility_start_after("2023-01-01").exempt_begin_before("2024-01-01").get()

    # Verify where clauses were properly constructed
    assert len(results) == 1
    # The where clauses should have been added to params during get()
    assert "$where" in resource._params
    assert "responsibility_beginning_date > '2023-01-01'" in resource._params["$where"]
    assert "exempt_begin_date < '2024-01-01'" in resource._params["$where"]
