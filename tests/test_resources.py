import pytest

from src.data.resources.resources import (
    SalesTaxResource,
    MixedBeverageResource,
    FranchiseResource,
)
from src.data.resources.sales_tax.allocation_payment_detail import LocalAllocationPaymentDetail
from src.data.resources.sales_tax.city_county_comparison_summary import CityCountyComparisonSummary
from src.data.resources.sales_tax.marketplace_provider_allocations import MarketplaceProviderAllocations
from src.data.resources.sales_tax.single_local_allocations import SingleLocalAllocations
from src.data.resources.sales_tax.permitted_locations import PermittedLocations
from src.data.resources.sales_tax.active_permits import ActivePermits
from src.data.resources.sales_tax.rates import SalesTaxRates
from src.data.resources.sales_tax.direct_pay import DirectPayTaxpayers
from src.data.resources.mixed_beverage.gross_receipts import MixedBeverageGrossReceipts
from src.data.resources.mixed_beverage.history import MixedBeverageHistory
from src.data.resources.franchise.active_permit_holders import ActiveFranchiseTaxPermitHolders


class DummyClient:
    """Minimal fake client."""
    def get(self, dataset_id, params=None):
        return []


def test_sales_tax_resource_factories():
    from src.data.resources.sales_tax.county_city_mta_allocations import CountySPDMTAAllocations

    st = SalesTaxResource(DummyClient())

    assert isinstance(st.local_allocation_payment_details(), LocalAllocationPaymentDetail)
    assert isinstance(st.city_county_comparison_summary(), CityCountyComparisonSummary)
    assert isinstance(st.county_spd_mta_allocations(), CountySPDMTAAllocations)
    assert isinstance(st.single_local_allocations(), SingleLocalAllocations)
    assert isinstance(st.marketplace_provider_allocations(), MarketplaceProviderAllocations)
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
    # The comparison_summaries method no longer takes a type parameter
    # This test is no longer relevant
    pass


def test_sales_tax_resource_no_client_raises_error():
    """Test that methods requiring a client raise ValueError when client is None."""
    st = SalesTaxResource(None)

    with pytest.raises(ValueError) as excinfo:
        st.local_allocation_payment_details()
    assert "Socrata client is not initialized" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        st.city_county_comparison_summary()
    assert "Socrata client is not initialized" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        st.county_spd_mta_allocations()
    assert "Socrata client is not initialized" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        st.single_local_allocations()
    assert "Socrata client is not initialized" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        st.marketplace_provider_allocations()
    assert "Socrata client is not initialized" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        st.permitted_locations()
    assert "Socrata client is not initialized" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        st.active_permits()
    assert "Socrata client is not initialized" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        st.rates()
    assert "Socrata client is not initialized" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        st.direct_pay_taxpayers()
    assert "Socrata client is not initialized" in str(excinfo.value)


def test_sales_tax_resource_methods_not_requiring_client():
    """Test methods that don't require a client work without one."""
    from src.data.resources.sales_tax.allocation_history import SalesTaxAllocationHistory
    from src.data.resources.sales_tax.marketplace_provider import MarketplaceProvider
    from src.data.resources.sales_tax.quarterly_sales_history import QuarterlySalesHistory
    from src.data.resources.sales_tax.single_local_tax_rates import SingleLocalTaxRates

    st = SalesTaxResource(None)

    # These should work without a client
    assert isinstance(st.allocation_history(), SalesTaxAllocationHistory)
    assert isinstance(st.marketplace_provider(), MarketplaceProvider)
    assert isinstance(st.quarterly_sales_history(), QuarterlySalesHistory)
    assert isinstance(st.single_local_tax_rates(), SingleLocalTaxRates)
