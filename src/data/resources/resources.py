from src.data.resources.sales_tax.allocation_payment_detail import LocalAllocationPaymentDetail
from src.data.resources.sales_tax.county_city_mta_allocations import CountySPDMTAAllocations
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
from src.data.resources.sales_tax.single_local_tax_rates import SingleLocalTaxRates
from src.data.resources.sales_tax.allocation_history import SalesTaxAllocationHistory
from src.data.resources.sales_tax.marketplace_provider import MarketplaceProvider
from src.data.resources.sales_tax.quarterly_sales_history import QuarterlySalesHistory

class SalesTaxResource:
    def __init__(self, socrata_client = None):
        self.client = socrata_client

    def local_allocation_payment_details(self):
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return LocalAllocationPaymentDetail(self.client)

    def city_county_comparison_summary(self):
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return CityCountyComparisonSummary(self.client)
    
    def county_spd_mta_allocations(self):
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return CountySPDMTAAllocations(self.client)

    def single_local_allocations(self):
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return SingleLocalAllocations(self.client)
    
    def marketplace_provider_allocations(self):
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return MarketplaceProviderAllocations(self.client)
    
    def permitted_locations(self):
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return PermittedLocations(self.client)
    
    def active_permits(self):
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return ActivePermits(self.client)
    
    def rates(self):
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return SalesTaxRates(self.client)
    
    def direct_pay_taxpayers(self):
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return DirectPayTaxpayers(self.client)
    
    def allocation_history(self, client=None):
        return SalesTaxAllocationHistory()

    def marketplace_provider(self, client=None):
        return MarketplaceProvider()
    
    def quarterly_sales_history(self, client=None):
        return QuarterlySalesHistory()
    
    def single_local_tax_rates(self, client=None):
        return SingleLocalTaxRates()

class MixedBeverageResource:
    def __init__(self, socrata_client):
        self.client = socrata_client

    def history(self):
        return MixedBeverageHistory()

    def gross_receipts(self):
        return MixedBeverageGrossReceipts(self.client)
    
class FranchiseResource:
    def __init__(self, socrata_client):
        self.client = socrata_client

    def active_permit_holders(self):
        return ActiveFranchiseTaxPermitHolders(self.client)
    