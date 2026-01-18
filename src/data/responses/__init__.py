"""Response data models for Texas Comptroller data."""

from .franchise_tax import FranchiseTaxPermitHolderData
from .mixed_beverage_tax import MixedBeverageGrossReceiptsData, MixedBeverageHistoryData
from .sales_tax import (
    ActivePermitData,
    AllocationHistoryData,
    ComparisonSummaryData,
    CountySPDMTAAllocationData,
    DirectPayTaxpayerData,
    LocalAllocationPaymentDetailsData,
    MarketplaceProviderAllocationData,
    MarketplaceProviderData,
    PermittedLocationData,
    QuarterlySalesHistoryData,
    SalesTaxRateData,
    SingleLocalAllocationData,
    SingleLocalTaxRateData,
)

__all__ = [
    # Franchise tax
    "FranchiseTaxPermitHolderData",
    # Mixed beverage tax
    "MixedBeverageGrossReceiptsData",
    "MixedBeverageHistoryData",
    # Sales tax
    "ActivePermitData",
    "AllocationHistoryData",
    "ComparisonSummaryData",
    "CountySPDMTAAllocationData",
    "DirectPayTaxpayerData",
    "LocalAllocationPaymentDetailsData",
    "MarketplaceProviderAllocationData",
    "MarketplaceProviderData",
    "PermittedLocationData",
    "QuarterlySalesHistoryData",
    "SalesTaxRateData",
    "SingleLocalAllocationData",
    "SingleLocalTaxRateData",
]
