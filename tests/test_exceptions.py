import httpx
import pytest
from src.compytroller.exceptions import TexasComptrollerError, HttpError, InvalidRequest


def test_texas_comptroller_error_is_base_class():
    with pytest.raises(TexasComptrollerError):
        raise TexasComptrollerError("Base error")


def test_http_error_init_and_attributes():
    err = HttpError("Something went wrong", status_code=500, url="https://example.com")
    assert isinstance(err, TexasComptrollerError)
    assert str(err) == "Something went wrong"
    assert err.status_code == 500
    assert err.url == "https://example.com"


def test_http_error_from_httpx_exception():
    request = httpx.Request("GET", "https://example.com/data")
    response = httpx.Response(404, request=request)
    exc = httpx.HTTPStatusError("Not Found", request=request, response=response)

    err = HttpError.from_httpx_exception(exc)
    assert isinstance(err, HttpError)
    assert "Not Found" in str(err)
    assert err.status_code == 404
    assert "https://example.com/data" in err.url


def test_invalid_request_with_custom_message():
    err = InvalidRequest("Bad params")
    assert isinstance(err, TexasComptrollerError)
    assert str(err) == "Bad params"


def test_invalid_request_with_default_message():
    err = InvalidRequest()
    assert "The request was incomplete" in str(err)
