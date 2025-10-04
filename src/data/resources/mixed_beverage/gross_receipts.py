import httpx
from typing import List
from data.responses.mixed_beverage_tax import MixedBeverageGrossReceiptsData
from data.exceptions import HttpError, InvalidRequest

class MixedBeverageGrossReceipts:
    DATASET_ID = "naix-2893"

    def __init__(self, socrata_client):
        self.client = socrata_client

    def get_all(self) -> List[MixedBeverageGrossReceiptsData]:
        try:
            records = self.client.get(self.DATASET_ID)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest("No records returned from Mixed Beverage Gross Receipts dataset")

        return [MixedBeverageGrossReceiptsData.from_dict(r) for r in records]
