import pytest
from datetime import date
from data.responses.mixed_beverage_tax import (
    MixedBeverageGrossReceiptsData,
    MixedBeverageHistoryData,
)


def test_mixed_beverage_gross_receipts_data_from_dict_valid():
    data = {
        "tabc_permit_number": "MB123",
        "taxpayer_name": "Bar LLC",
        "taxpayer_address": "123 Main St",
        "taxpayer_city": "Austin",
        "taxpayer_state": "TX",
        "taxpayer_zip": "78701",
        "location_name": "Downtown Bar",
        "location_address": "123 Main St",
        "location_city": "Austin",
        "location_state": "TX",
        "location_zip": "78701",
        "inside_outside_city_limits_code_y_n": "Y",
        "responsibility_begin_date_yyyymmdd": "2020-01-01",
        "responsibility_end_date_yyyymmdd": "2020-12-31",
        "obligation_start_date_yyyymmdd": "2020-01-01",
        "obligation_end_date_yyyymmdd": "2020-12-31",
        "beer_receipts": "100.0",
        "wine_receipts": "200.0",
        "liquor_receipts": "300.0",
        "cover_charge_receipts": "50.0",
        "total_receipts": "650.0",
        "num_outlets": "2",
    }

    dto = MixedBeverageGrossReceiptsData.from_dict(data)
    assert dto.permit_number == "MB123"
    assert dto.tp_name == "Bar LLC"
    assert dto.tp_city == "Austin"
    assert dto.total_receipts == 650.0
    assert dto.num_outlets == 2
    assert isinstance(dto.responsibility_begin_date, date)
    assert isinstance(dto.obligation_end_date, date)


def test_mixed_beverage_gross_receipts_data_from_dict_with_invalids():
    data = {
        "tabc_permit_number": "MB124",
        "taxpayer_name": "Bad Bar",
        "responsibility_begin_date_yyyymmdd": "not-a-date",
        "obligation_start_date_yyyymmdd": None,
        "beer_receipts": "not-a-float",
        "num_outlets": "not-an-int",
    }

    dto = MixedBeverageGrossReceiptsData.from_dict(data)
    assert dto.responsibility_begin_date is None
    assert dto.obligation_start_date is None
    assert dto.beer_receipts is None
    assert dto.num_outlets is None


def test_mixed_beverage_history_data_instantiation():
    dto = MixedBeverageHistoryData(
        jurisdiction_name="Austin",
        jurisdiction_type="CITY",
        summary_type="Summary",
        allocation_month=date(2023, 1, 1),
        net_payment=1234.56,
    )
    assert dto.jurisdiction_name == "Austin"
    assert dto.net_payment == 1234.56
