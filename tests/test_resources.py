import pytest

from data.resources.resources import (
    SalesTaxResource,
    MixedBeverageResource,
    FranchiseResource,
)
from data.resources.sales_tax.allocation_payment_detail import LocalAllocationPaymentDetail
from data.resources.sales_tax.comparison_summary import ComparisonSummary
from data.resources.sales_tax.marketplace_provider_allocations import MarketplaceProviderAllocations
from data.resources.sales_tax.single_local_allocations import SingleLocalAllocations
from data.resources.sales_tax.permitted_locations import PermittedLocations
from data.resources.sales_tax.active_permits import ActivePermits
from data.resources.sales_tax.rates import SalesTaxRates
from data.resources.sales_tax.direct_pay import DirectPayTaxpayers
from data.resources.mixed_beverage.gross_receipts import MixedBeverageGrossReceipts
from data.resources.mixed_beverage.history import MixedBeverageHistory
from data.resources.franchise.active_permit_holders import ActiveFranchiseTaxPermitHolders


class DummyClient:
    """Minimal fake client."""
    def get(self, dataset_id, params=None):
        return []


def test_sales_tax_resource_factories():
    st = SalesTaxResource(DummyClient())

    assert isinstance(st.local_allocation_payment_details(), LocalAllocationPaymentDetail)
    assert isinstance(st.comparison_summaries("cities"), ComparisonSummary)
    assert isinstance(st.single_local_allocations(), SingleLocalAllocations)
    assert isinstance(st.marketplace_providers(), MarketplaceProviderAllocations)
    assert isinstance(st.permitted_locations(), PermittedLocations)
    assert isinstance(st.active_permits(), ActivePermits)
    assert isinstance(st.rates(), SalesTaxRates)
    assert isinstance(st.direct_pay_taxpayers(), DirectPayTaxpayers)


def test_mixed_beverage_resource_factories():
    mb = MixedBeverageResource(DummyClient())

    assert isinstance(mb.history(), MixedBeverageHistory)
    assert isinstance(mb.gross_receipts(), MixedBeverageGrossReceipts)


def test_franchise_resource_factories():
    fr = FranchiseResource(DummyClient())

    assert isinstance(fr.active_permit_holders(), ActiveFranchiseTaxPermitHolders)


def test_comparison_summary_invalid_type():
    st = SalesTaxResource(DummyClient())
    with pytest.raises(ValueError):
        st.comparison_summaries("not-a-valid-type")
