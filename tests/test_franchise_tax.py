import pytest
from datetime import date
from src.data.responses.franchise_tax import FranchiseTaxPermitHolderData


def test_franchise_tax_permit_holder_data_from_dict_valid():
    data = {
        "taxpayer_number": "123456789",
        "taxpayer_name": "BizCo LLC",
        "taxpayer_address": "123 Main St",
        "taxpayer_city": "Austin",
        "taxpayer_state": "TX",
        "taxpayer_zip": "78701",
        "taxpayer_county_code": "201",
        "taxpayer_organizational_type": "LLC",
        "record_type_code": "P",
        "responsibility_beginning_date": "2020-01-01",
        "secretary_of_state_sos_or_coa_file_number": "987654321",
        "sos_charter_date": "2020-02-01",
        "sos_status_date": "2021-01-01",
        "sos_status_code": "A",
        "right_to_transact_business_code": "Y",
    }

    dto = FranchiseTaxPermitHolderData.from_dict(data)
    assert dto.taxpayer_number == "123456789"
    assert dto.taxpayer_name == "BizCo LLC"
    assert dto.taxpayer_state == "TX"
    assert isinstance(dto.responsibility_beginning_date, date)
    assert dto.secretary_of_state_file_number == "987654321"
    assert dto.sos_status_code == "A"


def test_franchise_tax_permit_holder_data_from_dict_with_missing_and_invalid_dates():
    data = {
        "taxpayer_number": "123456789",
        "taxpayer_name": "BizCo LLC",
        "responsibility_beginning_date": None,  # triggers parse_date None
        "sos_charter_date": "not-a-date",       # triggers parse_date failure
        "sos_status_date": "",                  # empty string
    }

    dto = FranchiseTaxPermitHolderData.from_dict(data)
    assert dto.responsibility_beginning_date is None
    assert dto.sos_charter_date is None
    assert dto.sos_status_date is None
