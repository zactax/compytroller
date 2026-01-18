# compytroller/client.py
from src.data.resources import FranchiseResource, MixedBeverageResource, SalesTaxResource
from src.data.socrata import SocrataClient

class ComptrollerClient:
    """Main client for accessing Texas Comptroller of Public Accounts data.

    This client provides access to various tax-related datasets from the Texas
    Comptroller's office through the Socrata Open Data API. It supports sales tax,
    franchise tax, and mixed beverage tax data retrieval.

    Example:
        >>> client = ComptrollerClient(app_token="your_token")
        >>> sales_data = client.sales_tax().active_permits().in_city("Austin").get()

    Attributes:
        socrata: The underlying SocrataClient used for HTTP requests.
    """

    def __init__(self, app_token: str, base_url: str = "https://data.texas.gov/resource"):
        """Initialize the Comptroller client.

        Args:
            app_token: Socrata API application token for authentication.
            base_url: Base URL for the Socrata API endpoint. Defaults to Texas data portal.
        """
        self.socrata = SocrataClient(app_token, base_url)

    @classmethod
    def factory(cls, app_token: str):
        """Factory method to create a ComptrollerClient instance.

        Args:
            app_token: Socrata API application token for authentication.

        Returns:
            A new ComptrollerClient instance.
        """
        return cls(app_token)

    def sales_tax(self) -> SalesTaxResource:
        """Access sales tax data resources.

        Returns:
            SalesTaxResource instance for querying sales tax datasets.
        """
        return SalesTaxResource(self.socrata)

    def franchise_tax(self):
        """Access franchise tax data resources.

        Returns:
            FranchiseResource instance for querying franchise tax datasets.
        """
        return FranchiseResource(self.socrata)

    def mixed_beverage_tax(self):
        """Access mixed beverage tax data resources.

        Returns:
            MixedBeverageResource instance for querying mixed beverage tax datasets.
        """
        return MixedBeverageResource(self.socrata)

    def get(self, dataset_id: str, params: dict = None):
        """Execute a direct GET request to a Socrata dataset.

        Args:
            dataset_id: The Socrata dataset identifier (e.g., "jrea-zgmq").
            params: Optional query parameters for filtering and pagination.

        Returns:
            Raw JSON response as a list of dictionaries.

        Raises:
            HttpError: If the HTTP request fails.
        """
        return self.socrata.get(dataset_id, params or {})