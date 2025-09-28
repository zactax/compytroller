from typing import List
from data.responses.franchise_tax import FranchiseTaxPermitHolderData

class ActiveFranchiseTaxPermitHolders:
    DATASET_ID = "9cir-efmm"

    def __init__(self, socrata_client):
        self.client = socrata_client

    def get_all(self) -> List[FranchiseTaxPermitHolderData]:
        records = self.client.get(self.DATASET_ID)
        return [FranchiseTaxPermitHolderData.from_dict(r) for r in records]
