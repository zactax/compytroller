import pytest
from datetime import date
from data.responses.sales_tax import (
    ComparisonSummaryData,
    SingleLocalAllocationData,
    SingleLocalTaxRateData,
    LocalAllocationPaymentDetailsData,
    MarketplaceProviderAllocationData,
    MarketplaceProviderData,
    PermittedLocationData,
    ActivePermitData,
    SalesTaxRateData,
    DirectPayTaxpayerData,
    AllocationHistoryData,
    QuarterlySalesHistoryData,
)


#  ComparisonSummaryData
def test_comparison_summary_data_from_dict_handles_variants():
    data = {
        "city": "Austin",
        "county": "Travis",
        "type": "CITY",
        "report_year": "2023",
        "report_month": "5",
        "net_payment_this_period": "100.0",
        "comparable_payment_prior_year": "90.0",
        "payments_to_date": "200.0",
        "previous_payments_to_date": "180.0",
        "period_percent_change": "5.0",
    }
    dto = ComparisonSummaryData.from_dict(data)
    assert dto.jurisdiction == "Austin"
    assert dto.percent_change == 5.0


#  SingleLocalAllocationData 
def test_single_local_allocation_data_handles_bad_values():
    data = {
        "authority_type": "COUNTY",
        "tax_authority": "Travis",
        "report_year": "not-an-int",
        "report_month": None,
        "current_net_payment": "bad-float",
        "prior_year_net_payment": None,
        "yoy_percent_change": "NaN",
        "payment_ytd": "",
        "prior_year_payment_ytd": "12345.67",
        "ytd_percent_change": None,
    }
    dto = SingleLocalAllocationData.from_dict(data)
    assert dto.report_year is None
    assert dto.current_net_payment is None
    assert dto.prior_year_payment_ytd == 12345.67


#  SingleLocalTaxRateData 
def test_single_local_tax_rate_data_invalid_dates():
    data = {
        "taxpayer_number": "111",
        "name": "TestCo",
        "begin_date": "not-a-date",
        "end_date": None,
    }
    dto = SingleLocalTaxRateData.from_dict(data)
    assert dto.begin_date is None
    assert dto.end_date is None


#  LocalAllocationPaymentDetailsData 
def test_local_allocation_payment_details_parsing():
    data = {
        "authority_id": "123",
        "authority_name": "Austin",
        "allocation_month": "2023-05-01",
        "allocation_date": "2023-05-01T00:00:00.000",
        "total_collections": "1000.0",
    }
    dto = LocalAllocationPaymentDetailsData.from_dict(data)
    assert dto.authority_name == "Austin"
    assert isinstance(dto.allocation_month, date)
    assert dto.total_collections == 1000.0


#  MarketplaceProviderAllocationData 
def test_marketplace_provider_allocation_data_from_dict():
    data = {
        "authority_type": "CITY",
        "authority_id": "001",
        "authority_name": "Austin",
        "allocation_year": "2023",
        "allocation_month": "5",
        "amount_allocated": "1234.56",
    }
    dto = MarketplaceProviderAllocationData.from_dict(data)
    assert dto.amount_allocated == 1234.56
    assert dto.allocation_year == 2023


#  MarketplaceProviderData 
def test_marketplace_provider_data_invalid_dates():
    data = {
        "Taxpayer Number": "123",
        "Taxpayer Name": "Bad Inc",
        "Begin Date": "not-a-date",
        "End Date": "bad-date",
    }
    dto = MarketplaceProviderData.from_dict(data)
    assert dto.begin_date is None
    assert dto.end_date is None


#  PermittedLocationData 
def test_permitted_location_data_with_bad_dates():
    data = {
        "tp_number": "1",
        "tp_name": "Biz",
        "tp_address": "123 St",
        "tp_city": "Austin",
        "tp_state": "TX",
        "tp_zip": "78701",
        "tp_county": "Travis",
        "org_type": "LLC",
        "loc_number": "10",
        "loc_name": "Main",
        "loc_city": "Austin",
        "loc_state": "TX",
        "loc_zip": "78701",
        "loc_county": "Travis",
        "naics": "1234",
        "juris_city": None,
        "city_taid": None,
        "mass_transit_auth1_taid": None,
        "mass_transit_auth2_taid": None,
        "county_taid": None,
        "special_purp_dist1_taid": None,
        "special_purp_dist2_taid": None,
        "special_purp_dist3_taid": None,
        "special_purp_dist4_taid": None,
        "unique_taid": None,
        "first_sale_date": "bad-date",
        "out_of_business_date": None,
    }
    dto = PermittedLocationData.from_dict(data)
    assert dto.first_sale_date is None
    assert dto.out_of_business_date is None


#  ActivePermitData 
def test_active_permit_data_from_dict():
    data = {
        "taxpayer_number": "123",
        "taxpayer_name": "BizCo",
        "taxpayer_address": "123 St",
        "taxpayer_city": "Austin",
        "taxpayer_state": "TX",
        "taxpayer_zip_code": "78701",
        "taxpayer_county_code": "201",
        "taxpayer_organization_type": "LLC",
        "outlet_number": "1",
        "outlet_name": "Shop",
        "outlet_address": "123 St",
        "outlet_city": "Austin",
        "outlet_state": "TX",
        "outlet_zip_code": "78701",
        "outlet_county_code": "201",
        "outlet_naics_code": "1234",
        "outlet_inside_outside_city_limits_indicator": "I",
        "outlet_permit_issue_date": "2023-01-01",
        "outlet_first_sales_date": "2023-01-02",
    }
    dto = ActivePermitData.from_dict(data)
    assert dto.taxpayer_name == "BizCo"
    assert dto.outlet_name == "Shop"


#  SalesTaxRateData 
def test_sales_tax_rate_data_from_dict():
    data = {
        "type": "CITY",
        "city_name": "Austin",
        "county_name": "Travis",
        "old_rate": "0.01",
        "new_rate": "0.02",
        "effective_date": "2023-01-01",
        "report_month": "5",
        "report_year": "2023",
        "report_period_type": "MONTH",
    }
    dto = SalesTaxRateData.from_dict(data)
    assert dto.old_rate == 0.01
    assert dto.report_year == 2023


#  DirectPayTaxpayerData 
def test_direct_pay_taxpayer_data_empty_and_invalid_date():
    # empty value
    data = {"id": "1", "name": "Test", "responsibility_begin_date": None}
    dto = DirectPayTaxpayerData.from_dict(data)
    assert dto.responsibility_begin_date is None

    # bad value
    data = {"id": "2", "name": "Bad", "responsibility_begin_date": "not-a-date"}
    dto = DirectPayTaxpayerData.from_dict(data)
    assert dto.responsibility_begin_date is None


#  AllocationHistoryData 
def test_allocation_history_data_invalid_amount_and_month():
    # invalid amount triggers float exception
    row = ["January", "not-a-float"]
    result = AllocationHistoryData.from_row(row, "2020", "123", "Authority")
    assert result.net_payment is None

    # invalid month triggers both ValueError paths
    row = ["NotAMonth", "1000"]
    result = AllocationHistoryData.from_row(row, "2020", "123", "Authority")
    assert result is None


#  QuarterlySalesHistoryData 
def test_quarterly_sales_history_data_from_dict():
    data = {
        "jurisdiction_name": "Austin",
        "jurisdiction_type": "CITY",
        "industry_label": "Retail Trade",
        "summary_type": "In-State",
        "report_kind": "Summary",
        "year": "2023",
        "quarter": "2",
        "gross_sales": "1234.56",
        "taxable_sales": "1200.00",
        "num_outlets": "50",
    }
    dto = QuarterlySalesHistoryData.from_dict(data)
    assert dto.year == 2023
    assert dto.quarter == 2
    assert dto.gross_sales == 1234.56
    assert dto.num_outlets == 50
