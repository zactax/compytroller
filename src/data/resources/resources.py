from src.data.resources.sales_tax.allocation_payment_detail import LocalAllocationPaymentDetail
from src.data.resources.sales_tax.comparison_summary import ComparisonSummary
from src.data.resources.sales_tax.marketplace_provider_allocations import MarketplaceProviders
from src.data.resources.sales_tax.single_local_allocations import SingleLocalAllocations
from src.data.resources.sales_tax.permitted_locations import PermittedLocations
from src.data.resources.sales_tax.active_permits import ActivePermits
from src.data.resources.sales_tax.rates import SalesTaxRates
from src.data.resources.sales_tax.direct_pay import DirectPayTaxpayers
from src.data.resources.mixed_beverage.gross_receipts import MixedBeverageGrossReceipts
from src.data.resources.mixed_beverage.history import MixedBeverageHistory
from src.data.resources.franchise.active_permit_holders import ActiveFranchiseTaxPermitHolders

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
    