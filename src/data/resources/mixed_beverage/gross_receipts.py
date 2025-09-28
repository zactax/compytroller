from typing import List
from data.responses.mixed_beverage_tax import MixedBeverageGrossReceiptsData

class MixedBeverageGrossReceipts:
    DATASET_ID = "naix-2893"  # CSV endpoint or JSON, depending on your preference

    def __init__(self, socrata_client):
        self.client = socrata_client

    def get_all(self) -> List[MixedBeverageGrossReceiptsData]:
        records = self.client.get(self.DATASET_ID)
        return [MixedBeverageGrossReceiptsData.from_dict(r) for r in records]