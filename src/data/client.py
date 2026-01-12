# compytroller/client.py
from src.data.socrata import SocrataClient
from src.data.resources import SalesTaxResource
from src.data.resources import FranchiseResource
from src.data.resources import MixedBeverageResource

class ComptrollerClient:
    def __init__(self, app_token: str, base_url: str = "https://data.texas.gov/resource"):
        self.socrata = SocrataClient(app_token, base_url)

    @classmethod
    def factory(cls, app_token: str):
        return cls(app_token)

    def sales_tax(self) -> SalesTaxResource:
        return SalesTaxResource(self.socrata)
    
    def franchise_tax(self):
        return FranchiseResource(self.socrata)

    def mixed_beverage_tax(self):
        return MixedBeverageResource(self.socrata)

    def get(self, dataset_id: str, params: dict = None):
        return self.socrata.get(dataset_id, params or {})