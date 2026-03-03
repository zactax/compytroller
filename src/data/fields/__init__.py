"""Type-safe field enums for Compytroller datasets.

Import field enums for use with ``sort_by()`` and categorical enums for
``for_type()`` and similar filter methods::

    from data.fields import ActivePermitField, AuthorityType

    results = (client.sales_tax()
        .active_permits()
        .sort_by(ActivePermitField.OUTLET_CITY)
        .limit(100)
        .get())

All enums inherit from ``str``, so plain strings continue to work everywhere.
"""

from .franchise_tax import (
    FranchiseTaxPermitHolderField,
    RightToTransactCode,
)
from .mixed_beverage import MixedBeverageGrossReceiptsField
from .sales_tax import (
    ActivePermitField,
    AllocationPaymentDetailField,
    AuthorityType,
    ComparisonSummaryField,
    CountySPDMTAAllocationField,
    DirectPayTaxpayerField,
    MarketplaceProviderAllocationField,
    PermittedLocationField,
    SalesTaxRateField,
    SalesTaxRateType,
    SingleLocalAllocationField,
)

__all__ = [
    # Sales tax field enums
    "ActivePermitField",
    "AllocationPaymentDetailField",
    "ComparisonSummaryField",
    "CountySPDMTAAllocationField",
    "DirectPayTaxpayerField",
    "MarketplaceProviderAllocationField",
    "PermittedLocationField",
    "SalesTaxRateField",
    "SingleLocalAllocationField",
    # Franchise tax field enums
    "FranchiseTaxPermitHolderField",
    # Mixed beverage field enums
    "MixedBeverageGrossReceiptsField",
    # Categorical enums
    "AuthorityType",
    "RightToTransactCode",
    "SalesTaxRateType",
]
