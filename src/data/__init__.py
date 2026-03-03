"""Compytroller - Texas Comptroller of Public Accounts Data API Client."""

from .client import ComptrollerClient
from .exceptions import HttpError, InvalidRequest, TexasComptrollerError
from .fields import (
    ActivePermitField,
    AllocationPaymentDetailField,
    AuthorityType,
    ComparisonSummaryField,
    CountySPDMTAAllocationField,
    DirectPayTaxpayerField,
    FranchiseTaxPermitHolderField,
    MarketplaceProviderAllocationField,
    MixedBeverageGrossReceiptsField,
    PermittedLocationField,
    RightToTransactCode,
    SalesTaxRateField,
    SalesTaxRateType,
    SingleLocalAllocationField,
)

__version__ = "0.1.0"

__all__ = [
    "ComptrollerClient",
    "HttpError",
    "InvalidRequest",
    "TexasComptrollerError",
    "__version__",
    # Field enums
    "ActivePermitField",
    "AllocationPaymentDetailField",
    "ComparisonSummaryField",
    "CountySPDMTAAllocationField",
    "DirectPayTaxpayerField",
    "FranchiseTaxPermitHolderField",
    "MarketplaceProviderAllocationField",
    "MixedBeverageGrossReceiptsField",
    "PermittedLocationField",
    "SalesTaxRateField",
    "SingleLocalAllocationField",
    # Categorical enums
    "AuthorityType",
    "RightToTransactCode",
    "SalesTaxRateType",
]
