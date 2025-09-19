# socrata.py
import httpx


class SocrataClient:
    """
    Low-level client for Socrata Open Data API (data.texas.gov).
    Handles authentication and GET requests.
    """

    def __init__(self, app_token: str, base_url: str = "https://data.texas.gov/resource"):
        self.app_token = app_token
        self.base_url = base_url.rstrip("/")
        self.http = httpx.Client(
            headers={"X-App-Token": app_token},
            timeout=30,
        )

    def get(self, dataset_id: str, params: dict = None):
        """
        Perform a GET request against a dataset.

        Args:
            dataset_id: The Socrata dataset identifier (e.g., "3p4v-vsr3").
            params: Optional query parameters (dict).

        Returns:
            Parsed JSON (list of dicts).
        """
        url = f"{self.base_url}/{dataset_id}.json"
        response = self.http.get(url, params=params or {})
        response.raise_for_status()
        return response.json()
