"""Tests for field and categorical enums."""

import pytest

from src.compytroller.fields import (
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
from src.compytroller.resources.sales_tax.active_permits import ActivePermits
from src.compytroller.resources.sales_tax.rates import SalesTaxRates
from src.compytroller.resources.franchise.active_permit_holders import (
    ActiveFranchiseTaxPermitHolders,
)
from src.compytroller.resources.mixed_beverage.gross_receipts import MixedBeverageGrossReceipts


# ---------------------------------------------------------------------------
# str behaviour: every enum member IS a string
# ---------------------------------------------------------------------------


class TestEnumsAreStrings:
    """Enum members must compare equal to their raw string values."""

    def test_active_permit_field(self):
        assert ActivePermitField.OUTLET_CITY == "outlet_city"
        assert isinstance(ActivePermitField.OUTLET_CITY, str)

    def test_permitted_location_field(self):
        assert PermittedLocationField.TP_NUMBER == "tp_number"

    def test_sales_tax_rate_field(self):
        assert SalesTaxRateField.CITY_NAME == "city_name"

    def test_comparison_summary_field(self):
        assert ComparisonSummaryField.NET_PAYMENT_THIS_PERIOD == "net_payment_this_period"

    def test_county_spd_mta_allocation_field(self):
        assert CountySPDMTAAllocationField.TYPE == "type"

    def test_single_local_allocation_field(self):
        assert SingleLocalAllocationField.TAX_AUTHORITY == "tax_authority"

    def test_allocation_payment_detail_field(self):
        assert AllocationPaymentDetailField.TOTAL_COLLECTIONS == "total_coll"

    def test_marketplace_provider_allocation_field(self):
        assert MarketplaceProviderAllocationField.AMOUNT_ALLOCATED == "amount_allocated"

    def test_direct_pay_taxpayer_field(self):
        assert DirectPayTaxpayerField.ID == "id"
        assert DirectPayTaxpayerField.ZIP == "zip"

    def test_franchise_tax_permit_holder_field(self):
        assert FranchiseTaxPermitHolderField.NAICS_CODE == "_621111"
        assert (
            FranchiseTaxPermitHolderField.SECRETARY_OF_STATE_FILE_NUMBER
            == "secretary_of_state_sos_or_coa_file_number"
        )

    def test_mixed_beverage_gross_receipts_field(self):
        assert (
            MixedBeverageGrossReceiptsField.INSIDE_OUTSIDE_CITY_LIMITS
            == "inside_outside_city_limits_code_y_n"
        )
        assert (
            MixedBeverageGrossReceiptsField.RESPONSIBILITY_BEGIN_DATE
            == "responsibility_begin_date_yyyymmdd"
        )


# ---------------------------------------------------------------------------
# Categorical enums: verify known values
# ---------------------------------------------------------------------------


class TestCategoricalEnums:
    def test_authority_type_values(self):
        assert AuthorityType.CITY == "CITY"
        assert AuthorityType.COUNTY == "COUNTY"
        assert AuthorityType.SPD == "SPD"
        assert AuthorityType.MTA == "MTA"
        assert AuthorityType.TRANSIT == "TRANSIT"

    def test_sales_tax_rate_type_values(self):
        assert SalesTaxRateType.CITY_LIST == "City List"
        assert SalesTaxRateType.SPD_LIST == "SPD List"

    def test_right_to_transact_code_values(self):
        assert RightToTransactCode.ACTIVE == "A"
        assert RightToTransactCode.ELIGIBLE_FOR_TERMINATION == "D"
        assert RightToTransactCode.FORFEITED == "N"
        assert RightToTransactCode.INVOLUNTARILY_ENDED == "I"
        assert RightToTransactCode.NOT_ESTABLISHED == "U"


# ---------------------------------------------------------------------------
# Integration: enums work with sort_by and filter methods
# ---------------------------------------------------------------------------


class TestEnumsWithResources:
    """Enums can be passed directly to resource methods that accept strings."""

    def test_sort_by_with_active_permit_field(self, dummy_client):
        sample = [{"taxpayer_number": "123", "taxpayer_name": "Test"}]
        resource = ActivePermits(dummy_client(sample))
        resource.sort_by(ActivePermitField.OUTLET_CITY)
        assert resource._params["$order"] == "outlet_city"

    def test_sort_by_desc_with_enum(self, dummy_client):
        sample = [{"taxpayer_number": "123", "taxpayer_name": "Test"}]
        resource = ActivePermits(dummy_client(sample))
        resource.sort_by(ActivePermitField.TAXPAYER_NAME, desc=True)
        assert resource._params["$order"] == "taxpayer_name DESC"

    def test_sort_by_with_sales_tax_rate_field(self, dummy_client):
        sample = [{"type": "City List", "city_name": "Austin"}]
        resource = SalesTaxRates(dummy_client(sample))
        resource.sort_by(SalesTaxRateField.CITY_NAME)
        assert resource._params["$order"] == "city_name"

    def test_sort_by_with_franchise_field(self, dummy_client):
        sample = [{"taxpayer_number": "123", "taxpayer_name": "Test"}]
        resource = ActiveFranchiseTaxPermitHolders(dummy_client(sample))
        resource.sort_by(FranchiseTaxPermitHolderField.TAXPAYER_CITY)
        assert resource._params["$order"] == "taxpayer_city"

    def test_sort_by_with_mixed_beverage_field(self, dummy_client):
        sample = [{"taxpayer_name": "Test", "taxpayer_address": "123 Main"}]
        resource = MixedBeverageGrossReceipts(dummy_client(sample))
        resource.sort_by(MixedBeverageGrossReceiptsField.TOTAL_RECEIPTS, desc=True)
        assert resource._params["$order"] == "total_receipts DESC"

    def test_for_type_with_authority_type(self, dummy_client):
        from src.compytroller.resources.sales_tax.marketplace_provider_allocations import (
            MarketplaceProviderAllocations,
        )

        sample = [
            {
                "authority_type": "CITY",
                "authority_id": "1",
                "authority_name": "Austin",
            }
        ]
        resource = MarketplaceProviderAllocations(dummy_client(sample))
        resource.for_type(AuthorityType.CITY)
        assert resource._params["authority_type"] == "CITY"

    def test_for_type_with_rate_type(self, dummy_client):
        sample = [{"type": "City List", "city_name": "Austin"}]
        resource = SalesTaxRates(dummy_client(sample))
        resource.for_type(SalesTaxRateType.CITY_LIST)
        assert resource._params["type"] == "City List"

    def test_with_right_to_transact_code(self, dummy_client):
        sample = [{"taxpayer_number": "123", "taxpayer_name": "Test"}]
        resource = ActiveFranchiseTaxPermitHolders(dummy_client(sample))
        resource.with_right_to_transact(RightToTransactCode.ACTIVE)
        assert resource._params["right_to_transact_business_code"] == "A"


# ---------------------------------------------------------------------------
# Package-level imports work
# ---------------------------------------------------------------------------


class TestPackageImports:
    """Enums are importable from the top-level data package."""

    def test_import_from_compytroller(self):
        from src.compytroller import ActivePermitField as APF

        assert APF.OUTLET_CITY == "outlet_city"

    def test_import_from_data_fields(self):
        from src.compytroller.fields import ActivePermitField as APF

        assert APF.OUTLET_CITY == "outlet_city"
