# socrata.py
import httpx

class SocrataClient:
    """Low-level HTTP client for Socrata Open Data API.

    This client handles authentication and HTTP requests to the Socrata Open Data
    API, primarily used for accessing data.texas.gov datasets. It manages the API
    token and provides a simple interface for GET requests.

    Attributes:
        app_token: The Socrata API application token for authentication.
        base_url: The base URL for the Socrata API endpoint.
        http: The underlying httpx.Client instance for HTTP requests.
    """

    def __init__(self, app_token: str, base_url: str = "https://data.texas.gov/resource"):
        """Initialize the Socrata HTTP client.

        Args:
            app_token: Socrata API application token for authentication.
            base_url: Base URL for the Socrata API endpoint. Defaults to the Texas
                data portal. Trailing slashes are automatically removed.
        """
        self.app_token = app_token
        self.base_url = base_url.rstrip("/")
        self.http = httpx.Client(
            headers={"X-App-Token": app_token},
            timeout=30,
        )

    def get(self, dataset_id: str, params: dict = None):
        """Perform a GET request against a Socrata dataset.

        Constructs the full URL from the dataset ID and executes an HTTP GET
        request with optional query parameters. The response is automatically
        parsed as JSON.

        Args:
            dataset_id: The Socrata dataset identifier (e.g., "3p4v-vsr3").
            params: Optional query parameters as a dictionary. Supports standard
                Socrata query parameters like $where, $limit, $order, etc.

        Returns:
            Parsed JSON response as a list of dictionaries, where each dictionary
            represents one record from the dataset.

        Raises:
            httpx.HTTPStatusError: If the server returns an HTTP error status code.
            httpx.RequestError: If the request fails due to network or connection issues.
        """
        url = f"{self.base_url}/{dataset_id}.json"
        response = self.http.get(url, params=params or {})
        response.raise_for_status()
        return response.json()
