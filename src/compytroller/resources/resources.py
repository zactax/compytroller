from src.compytroller.resources.sales_tax.allocation_payment_detail import LocalAllocationPaymentDetail
from src.compytroller.resources.sales_tax.county_spd_mta_allocations import CountySPDMTAAllocations
from src.compytroller.resources.sales_tax.city_county_comparison_summary import CityCountyComparisonSummary
from src.compytroller.resources.sales_tax.marketplace_provider_allocations import MarketplaceProviderAllocations
from src.compytroller.resources.sales_tax.single_local_allocations import SingleLocalAllocations
from src.compytroller.resources.sales_tax.permitted_locations import PermittedLocations
from src.compytroller.resources.sales_tax.active_permits import ActivePermits
from src.compytroller.resources.sales_tax.rates import SalesTaxRates
from src.compytroller.resources.sales_tax.direct_pay import DirectPayTaxpayers
from src.compytroller.resources.mixed_beverage.gross_receipts import MixedBeverageGrossReceipts
from src.compytroller.resources.mixed_beverage.history import MixedBeverageHistory
from src.compytroller.resources.franchise.active_permit_holders import ActiveFranchiseTaxPermitHolders
from src.compytroller.resources.sales_tax.single_local_tax_rates import SingleLocalTaxRates
from src.compytroller.resources.sales_tax.allocation_history import SalesTaxAllocationHistory
from src.compytroller.resources.sales_tax.marketplace_provider import MarketplaceProvider
from src.compytroller.resources.sales_tax.quarterly_sales_history import QuarterlySalesHistory

class SalesTaxResource:
    """Factory class for accessing sales tax data resources.

    This class provides factory methods to create resource instances for
    querying various sales tax datasets from the Texas Comptroller's office.
    Each method returns a resource object with a fluent API for building
    and executing queries.

    Attributes:
        client: The SocrataClient used for API requests.
    """

    def __init__(self, socrata_client = None):
        """
        Initialize the SalesTaxResource.

        Args:
            socrata_client: Optional SocrataClient instance for API communication.
        """
        self.client = socrata_client

    def local_allocation_payment_details(self):
        """
        Access local allocation payment detail data.

        Returns:
            LocalAllocationPaymentDetail instance for querying payment details.

        Raises:
            ValueError: If the Socrata client is not initialized.
        """
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return LocalAllocationPaymentDetail(self.client)

    def city_county_comparison_summary(self):
        """
        Access city and county comparison summary data.

        Returns:
            CityCountyComparisonSummary instance for querying comparison data.

        Raises:
            ValueError: If the Socrata client is not initialized.
        """
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return CityCountyComparisonSummary(self.client)

    def county_spd_mta_allocations(self):
        """
        Access county, special purpose district, and MTA allocation data.

        Returns:
            CountySPDMTAAllocations instance for querying allocation data.

        Raises:
            ValueError: If the Socrata client is not initialized.
        """
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return CountySPDMTAAllocations(self.client)

    def single_local_allocations(self):
        """
        Access single local jurisdiction allocation data.

        Returns:
            SingleLocalAllocations instance for querying allocation data.

        Raises:
            ValueError: If the Socrata client is not initialized.
        """
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return SingleLocalAllocations(self.client)

    def marketplace_provider_allocations(self):
        """
        Access marketplace provider allocation data.

        Returns:
            MarketplaceProviderAllocations instance for querying provider allocations.

        Raises:
            ValueError: If the Socrata client is not initialized.
        """
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return MarketplaceProviderAllocations(self.client)

    def permitted_locations(self):
        """
        Access sales tax permitted location data.

        Returns:
            PermittedLocations instance for querying location data.

        Raises:
            ValueError: If the Socrata client is not initialized.
        """
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return PermittedLocations(self.client)

    def active_permits(self):
        """
        Access active sales tax permit data.

        Returns:
            ActivePermits instance for querying active permit data.

        Raises:
            ValueError: If the Socrata client is not initialized.
        """
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return ActivePermits(self.client)

    def rates(self):
        """
        Access sales tax rate data by jurisdiction.

        Returns:
            SalesTaxRates instance for querying tax rate data.

        Raises:
            ValueError: If the Socrata client is not initialized.
        """
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return SalesTaxRates(self.client)

    def direct_pay_taxpayers(self):
        """
        Access direct pay taxpayer data.

        Returns:
            DirectPayTaxpayers instance for querying direct pay taxpayer data.

        Raises:
            ValueError: If the Socrata client is not initialized.
        """
        if not self.client:
            raise ValueError("Socrata client is not initialized.")
        return DirectPayTaxpayers(self.client)

    def allocation_history(self):
        """
        Access historical sales tax allocation data.

        This method scrapes data from the Comptroller's allocation website
        and does not require a Socrata client.

        Returns:
            SalesTaxAllocationHistory instance for querying historical allocation data.
        """
        return SalesTaxAllocationHistory()

    def marketplace_provider(self):
        """
        Access marketplace provider data.

        This method downloads data from a CSV file and does not require
        a Socrata client.

        Returns:
            MarketplaceProvider instance for querying provider data.
        """
        return MarketplaceProvider()

    def quarterly_sales_history(self):
        """
        Access quarterly sales history data.

        This method scrapes data from the Comptroller's website and does
        not require a Socrata client.

        Returns:
            QuarterlySalesHistory instance for querying quarterly sales data.
        """
        return QuarterlySalesHistory()

    def single_local_tax_rates(self):
        """
        Access single local tax rate data.

        This method downloads data from a CSV file and does not require
        a Socrata client.

        Returns:
            SingleLocalTaxRates instance for querying tax rate data.
        """
        return SingleLocalTaxRates()

class MixedBeverageResource:
    """
    Factory class for accessing mixed beverage tax data resources.

    This class provides factory methods to create resource instances for
    querying mixed beverage tax datasets from the Texas Comptroller's office.

    Attributes:
        client: The SocrataClient used for API requests.
    """

    def __init__(self, socrata_client):
        """
        Initialize the MixedBeverageResource.

        Args:
            socrata_client: SocrataClient instance for API communication.
        """
        self.client = socrata_client

    def history(self):
        """
        Access historical mixed beverage tax allocation data.

        This method scrapes data from the Comptroller's allocation website
        and does not require a Socrata client.

        Returns:
            MixedBeverageHistory instance for querying historical allocation data.
        """
        return MixedBeverageHistory()

    def gross_receipts(self):
        """
        Access mixed beverage gross receipts data.

        Returns:
            MixedBeverageGrossReceipts instance for querying gross receipts data.
        """
        return MixedBeverageGrossReceipts(self.client)

class FranchiseResource:
    """
    Factory class for accessing franchise tax data resources.

    This class provides factory methods to create resource instances for
    querying franchise tax datasets from the Texas Comptroller's office.

    Attributes:
        client: The SocrataClient used for API requests.
    """

    def __init__(self, socrata_client):
        """
        Initialize the FranchiseResource.

        Args:
            socrata_client: SocrataClient instance for API communication.
        """
        self.client = socrata_client

    def active_permit_holders(self):
        """
        Access active franchise tax permit holder data.

        Returns:
            ActiveFranchiseTaxPermitHolders instance for querying permit holder data.
        """
        return ActiveFranchiseTaxPermitHolders(self.client)
    