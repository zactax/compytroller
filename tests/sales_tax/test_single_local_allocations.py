from compytroller.responses.sales_tax import SingleLocalAllocationData
import pytest
import httpx
from compytroller.resources.sales_tax.single_local_allocations import SingleLocalAllocations
from compytroller.exceptions import HttpError, InvalidRequest


def test_single_local_allocations_parsing(dummy_client):
    sample = [{
        "authority_type": "CITY",
        "tax_authority": "Austin",
        "report_year": "2024",
        "report_month": "6",
        "current_net_payment": "12345.67",
        "prior_year_net_payment": "11111.11",
        "yoy_percent_change": "11.11",
        "payment_ytd": "98765.43",
        "prior_year_payment_ytd": "87654.32",
        "ytd_percent_change": "12.34",
    }]
    client = dummy_client(sample)
    results = (
        SingleLocalAllocations(client)
        .for_city("Austin")
        .for_year(2024)
        .sort_by("report_month", desc=True)
        .limit(1)
        .get()
    )

    assert len(results) == 1
    r = results[0]
    assert isinstance(r, SingleLocalAllocationData)
    assert r.tax_authority == "Austin"
    assert r.authority_type == "CITY"  # uppercased in for_type
    assert r.report_year == 2024
    assert r.report_month == 6
    assert r.current_net_payment == 12345.67
    assert r.yoy_percent_change == 11.11
    assert r.payment_ytd == 98765.43


def test_single_local_allocations_http_status_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            req = httpx.Request("GET", "https://fake")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("server error", request=req, response=resp)

    with pytest.raises(HttpError):
        SingleLocalAllocations(FailingClient()).get()


def test_single_local_allocations_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            raise httpx.RequestError("network down", request=httpx.Request("GET", "https://fake"))

    with pytest.raises(HttpError):
        SingleLocalAllocations(FailingClient()).get()


def test_single_local_allocations_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        SingleLocalAllocations(client).get()


def test_single_local_allocation_data_from_dict_handles_bad_values():
    data = {
        "authority_type": "COUNTY",
        "tax_authority": "Travis",
        "report_year": "not-an-int",
        "report_month": None,
        "current_net_payment": "bad-float",
        "prior_year_net_payment": None,
        "yoy_percent_change": "NaN",
        "payment_ytd": "",
        "prior_year_payment_ytd": "12345.67",
        "ytd_percent_change": None,
    }
    dto = SingleLocalAllocationData.from_dict(data)

    assert dto.report_year is None
    assert dto.report_month is None
    assert dto.current_net_payment is None
    assert dto.prior_year_net_payment is None
    assert dto.yoy_percent_change is None
    assert dto.payment_ytd is None
    assert dto.prior_year_payment_ytd == 12345.67
    assert dto.ytd_percent_change is None


def test_single_local_allocations_in_county(dummy_client):
    sample = [{"tax_authority": "Travis", "authority_type": "COUNTY"}]
    client = dummy_client(sample)
    resource = SingleLocalAllocations(client)
    resource.in_county("Travis")
    assert resource._params["tax_authority"] == "Travis"
    assert resource._params["authority_type"] == "COUNTY"


def test_single_local_allocations_for_spd(dummy_client):
    sample = [{"tax_authority": "SPD-123", "authority_type": "SPD"}]
    client = dummy_client(sample)
    resource = SingleLocalAllocations(client)
    resource.for_spd("SPD-123")
    assert resource._params["tax_authority"] == "SPD-123"
    assert resource._params["authority_type"] == "SPD"


def test_single_local_allocations_for_mta(dummy_client):
    sample = [{"tax_authority": "MTA-456", "authority_type": "MTA"}]
    client = dummy_client(sample)
    resource = SingleLocalAllocations(client)
    resource.for_mta("MTA-456")
    assert resource._params["tax_authority"] == "MTA-456"
    assert resource._params["authority_type"] == "MTA"


def test_single_local_allocations_for_month_invalid():
    from compytroller.resources.sales_tax.single_local_allocations import SingleLocalAllocations
    class DummyClient:
        pass

    resource = SingleLocalAllocations(DummyClient())

    with pytest.raises(InvalidRequest) as excinfo:
        resource.for_month(0)
    assert "Month must be between 1 and 12" in str(excinfo.value)

    with pytest.raises(InvalidRequest) as excinfo:
        resource.for_month(13)
    assert "Month must be between 1 and 12" in str(excinfo.value)


def test_single_local_allocations_reset(dummy_client):
    sample = [{"tax_authority": "Austin"}]
    client = dummy_client(sample)
    resource = SingleLocalAllocations(client)
    resource.for_city("Austin").for_year(2024).for_month(6).sort_by("report_month")
    assert len(resource._params) > 0

    resource.reset()
    assert resource._params == {}


def test_single_local_allocations_get_all(dummy_client):
    sample = [{
        "authority_type": "CITY",
        "tax_authority": "Austin",
        "report_year": "2024",
        "report_month": "6",
    }]
    client = dummy_client(sample)
    resource = SingleLocalAllocations(client)
    results = resource.get_all()
    assert len(results) == 1
    assert isinstance(results[0], SingleLocalAllocationData)


def test_single_local_allocations_get_all_http_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            req = httpx.Request("GET", "https://fake")
            resp = httpx.Response(500, request=req)
            raise httpx.HTTPStatusError("server error", request=req, response=resp)

    with pytest.raises(HttpError):
        SingleLocalAllocations(FailingClient()).get_all()


def test_single_local_allocations_get_all_request_error():
    class FailingClient:
        def get(self, dataset_id, params=None):
            raise httpx.RequestError("network down", request=httpx.Request("GET", "https://fake"))

    with pytest.raises(HttpError):
        SingleLocalAllocations(FailingClient()).get_all()


def test_single_local_allocations_get_all_empty(dummy_client):
    client = dummy_client([])
    with pytest.raises(InvalidRequest):
        SingleLocalAllocations(client).get_all()

