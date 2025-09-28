from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import date
from data.utils import parse_date

@dataclass
class FranchiseTaxPermitHolderData:
    taxpayer_number: str
    taxpayer_name: str
    taxpayer_address: Optional[str]
    taxpayer_city: Optional[str]
    taxpayer_state: Optional[str]
    taxpayer_zip: Optional[str]
    taxpayer_county_code: Optional[str]
    taxpayer_organizational_type: Optional[str]
    record_type_code: Optional[str]

    responsibility_beginning_date: Optional[date]
    secretary_of_state_file_number: Optional[str]
    sos_charter_date: Optional[date]
    sos_status_date: Optional[date]
    sos_status_code: Optional[str]
    right_to_transact_business_code: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            taxpayer_number=data.get("taxpayer_number"),
            taxpayer_name=data.get("taxpayer_name"),
            taxpayer_address=data.get("taxpayer_address"),
            taxpayer_city=data.get("taxpayer_city"),
            taxpayer_state=data.get("taxpayer_state"),
            taxpayer_zip=data.get("taxpayer_zip"),
            taxpayer_county_code=data.get("taxpayer_county_code"),
            taxpayer_organizational_type=data.get("taxpayer_organizational_type"),
            record_type_code=data.get("record_type_code"),
            responsibility_beginning_date=parse_date(data.get("responsibility_beginning_date")),
            secretary_of_state_file_number=data.get("secretary_of_state_sos_or_coa_file_number"),
            sos_charter_date=parse_date(data.get("sos_charter_date")),
            sos_status_date=parse_date(data.get("sos_status_date")),
            sos_status_code=data.get("sos_status_code"),
            right_to_transact_business_code=data.get("right_to_transact_business_code"),
        )
