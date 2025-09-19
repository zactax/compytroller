from compytroller.sales_tax.allocations import LocalAllocationPaymentDetail
from compytroller.sales_tax.comparison_summaries import ComparisonSummary
from compytroller.sales_tax.marketplace_providers import MarketplaceProviders
from compytroller.sales_tax.single_local_allocations import SingleLocalAllocations
from compytroller.sales_tax.permitted_locations import PermittedLocations
from compytroller.sales_tax.active_permits import ActivePermits
from compytroller.sales_tax.rates import SalesTaxRates
from compytroller.sales_tax.direct_pay import DirectPayTaxpayers

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