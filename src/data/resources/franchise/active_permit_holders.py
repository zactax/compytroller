import httpx
from typing import List
from data.responses.franchise_tax import FranchiseTaxPermitHolderData
from data.exceptions import HttpError, InvalidRequest

class ActiveFranchiseTaxPermitHolders:
    DATASET_ID = "9cir-efmm"

    def __init__(self, socrata_client):
        self.client = socrata_client

    def get_all(self) -> List[FranchiseTaxPermitHolderData]:
        try:
            records = self.client.get(self.DATASET_ID)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest("No records returned from Active Franchise Tax Permit Holders dataset")

        return [FranchiseTaxPermitHolderData.from_dict(r) for r in records]
