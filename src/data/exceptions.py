# exceptions.py

class TexasComptrollerError(Exception):
    """
    Base exception for all Texas Comptroller client errors.

    This is the parent exception class for all custom exceptions raised by
    the Texas Comptroller client library. Catching this exception will catch
    all library-specific errors.
    """

class HttpError(TexasComptrollerError):
    """
    Raised when an HTTP request to the Socrata API fails.

    This exception is raised for network errors, connection failures, timeout
    errors, or when the API returns an HTTP error status code (4xx, 5xx).

    Attributes:
        status_code: The HTTP status code from the failed request, if available.
        url: The URL that was being requested when the error occurred.
    """

    def __init__(self, message: str, status_code: int = None, url: str = None):
        """
        Initialize an HttpError.

        Args:
            message: A description of the HTTP error.
            status_code: The HTTP status code from the failed request, if available.
            url: The URL that was being requested when the error occurred.
        """
        super().__init__(message)
        self.status_code = status_code
        self.url = url

    @classmethod
    def from_httpx_exception(cls, exc):
        """
        Create an HttpError from an httpx exception.

        Factory method that extracts error details from an httpx library exception
        and constructs an HttpError instance with the relevant information.

        Args:
            exc: An httpx.HTTPStatusError or httpx.RequestError exception.

        Returns:
            A new HttpError instance containing details from the httpx exception.
        """
        status_code = getattr(exc.response, "status_code", None)
        url = str(getattr(exc.request, "url", None))
        return cls(str(exc), status_code=status_code, url=url)

class InvalidRequest(TexasComptrollerError):
    """
    Raised when a request is incomplete, invalid, or returns no data.

    This exception is typically raised when:
    - Required query parameters are missing
    - A query returns zero records
    - Invalid method call sequence (e.g., calling get() without setting filters)
    - Invalid parameter values
    """

    def __init__(self, message: str = None):
        """
        Initialize an InvalidRequest exception.

        Args:
            message: A description of why the request is invalid. If None, a
                default message suggesting the use of helper methods is used.
        """
        if message is None:
            message = (
                "The request was incomplete, you should probably use one of "
                "the helper methods to fetch a report."
            )
        super().__init__(message)
