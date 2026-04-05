import pytest
import httpx
from unittest.mock import patch
from compytroller.socrata import SocrataClient

class FakeResponse:
    def __init__(self, json_data=None, status_code=200, raise_error=None):
        self._json = json_data or []
        self._status_code = status_code
        self._raise_error = raise_error

    def raise_for_status(self):
        if self._raise_error:
            raise self._raise_error

    def json(self):
        return self._json

def test_socrata_client_init(monkeypatch):
    monkeypatch.setenv("app_token", "dummy")

    # Patch httpx.Client so it never runs
    with patch("compytroller.socrata.httpx.Client") as MockHttpx:
        MockHttpx.return_value = object()  # stub out the client
        client = SocrataClient("https://data.texas.gov", "dummy")
        assert isinstance(client, SocrataClient)
        # our stub should have been attached
        assert client.http is not None

def test_socrata_client_get_success(monkeypatch):
    def fake_get(url, params=None):
        assert "dataset123.json" in url
        assert params == {"$limit": 5}
        return FakeResponse(json_data=[{"id": "1", "name": "Austin"}])

    client = SocrataClient("fake-token", base_url="https://example.com/resource")
    client.http.get = fake_get  # patch
    result = client.get("dataset123", {"$limit": 5})

    assert isinstance(result, list)
    assert result[0]["name"] == "Austin"


def test_socrata_client_get_http_status_error(monkeypatch):
    error = httpx.HTTPStatusError(
        "Server error",
        request=httpx.Request("GET", "https://example.com"),
        response=httpx.Response(500, request=httpx.Request("GET", "https://example.com")),
    )

    def fake_get(url, params=None):
        return FakeResponse(raise_error=error)

    client = SocrataClient("fake-token", base_url="https://example.com/resource")
    client.http.get = fake_get

    with pytest.raises(httpx.HTTPStatusError):
        client.get("dataset123")
