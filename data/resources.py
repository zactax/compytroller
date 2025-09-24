from data.sales_tax.allocations import LocalAllocationPaymentDetail
from data.sales_tax.comparison_summaries import ComparisonSummary
from data.sales_tax.marketplace_provider_allocations import MarketplaceProviders
from data.sales_tax.single_local_allocations import SingleLocalAllocations
from data.sales_tax.permitted_locations import PermittedLocations
from data.sales_tax.active_permits import ActivePermits
from data.sales_tax.rates import SalesTaxRates
from data.sales_tax.direct_pay import DirectPayTaxpayers
from data.mixed_beverage.mixed_beverage_gross_receipts import MixedBeverageGrossReceipts
from data.mixed_beverage.mixed_beverage_history import MixedBeverageHistory
from data.franchise.active_franchise_tax_permit_holders import ActiveFranchiseTaxPermitHolders

class SalesTaxResource:
    def __init__(self, socrata_client):
        self.client = socrata_client

    def local_allocation_payment_details(self):
        return LocalAllocationPaymentDetail(self.client)

    def comparison_summaries(self, summary_type: str):
        return ComparisonSummary(self.client, summary_type)

    def single_local_allocations(self):
        return SingleLocalAllocations(self.client)
    
    def marketplace_providers(self):
        return MarketplaceProviders(self.client)
    
    def permitted_locations(self):
        return PermittedLocations(self.client)
    
    def active_permits(self):
        return ActivePermits(self.client)
    
    def rates(self):
        return SalesTaxRates(self.client)
    
    def direct_pay_taxpayers(self):
        return DirectPayTaxpayers(self.client)
    
class MixedBeverageResource:
    def __init__(self, socrata_client):
        self.client = socrata_client

    def history(self):
        return MixedBeverageHistory(self.client)

    def gross_receipts(self):
        return MixedBeverageGrossReceipts(self.client)
    
class FranchiseResource:
    def __init__(self, socrata_client):
        self.client = socrata_client

    def active_permit_holders(self):
        return ActiveFranchiseTaxPermitHolders(self.client)
    