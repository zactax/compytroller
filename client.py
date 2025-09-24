# compytroller/client.py
from socrata import SocrataClient
from data.resources import SalesTaxResource
from data.resources import FranchiseResource
from data.resources import MixedBeverageResource

class ComptrollerClient:
    def __init__(self, app_token: str, base_url: str = "https://data.texas.gov/resource"):
        self.socrata = SocrataClient(app_token, base_url)

    @classmethod
    def factory(cls, app_token: str):
        return cls(app_token)

    def sales_tax(self) -> SalesTaxResource:
        return SalesTaxResource(self.socrata)
    
    def franchise(self):
        return FranchiseResource(self.socrata)
    
    def mixed_beverage(self):
        return MixedBeverageResource(self.socrata)

    def get(self, dataset_id: str, params: dict = None):
        return self.socrata.get(dataset_id, params or {})