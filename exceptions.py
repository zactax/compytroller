# exceptions.py

class TexasComptrollerError(Exception):
    """Base exception for the Texas Comptroller client."""


class HttpError(TexasComptrollerError):
    """Raised when an HTTP request fails."""

    def __init__(self, message: str, status_code: int = None, url: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.url = url

    @classmethod
    def from_httpx_exception(cls, exc):
        """Build from an httpx.HTTPStatusError or requests.HTTPError."""
        status_code = getattr(exc.response, "status_code", None)
        url = str(getattr(exc.request, "url", None))
        return cls(str(exc), status_code=status_code, url=url)


class InvalidRequest(TexasComptrollerError):
    """Raised when a request is incomplete or invalid."""

    def __init__(self, message: str = None):
        if message is None:
            message = (
                "The request was incomplete, you should probably use one of "
                "the helper methods to fetch a report."
            )
        super().__init__(message)
