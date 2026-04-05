from dataclasses import dataclass
from datetime import date
from typing import Any, Dict, Optional

from compytroller.utils import parse_date


@dataclass
class FranchiseTaxPermitHolderData:
    """Franchise tax permit holder data for Texas businesses.

    Represents detailed information about businesses that are subject to Texas
    franchise tax reporting requirements. This includes taxpayer identification,
    contact information, organizational details, Secretary of State filing information,
    and exemption status.

    Attributes:
        taxpayer_number: Unique identification number assigned to the taxpayer.
        taxpayer_name: Legal name of the taxpayer or business entity.
        taxpayer_address: Taxpayer's mailing address.
        taxpayer_city: Taxpayer's city.
        taxpayer_state: Taxpayer's state.
        taxpayer_zip: Taxpayer's ZIP code.
        taxpayer_county_code: County code where the taxpayer is located.
        taxpayer_organizational_type: Type of organization (e.g., "Corporation", "LLC", "Partnership").
        record_type_code: Code indicating the type of franchise tax record.
        responsibility_beginning_date: Date when franchise tax responsibility began.
        secretary_of_state_file_number: File number assigned by the Texas Secretary of State or Certificate of Authority.
        sos_charter_date: Date when the entity's charter was filed with the Secretary of State.
        sos_status_date: Date of the most recent status update with the Secretary of State.
        sos_status_code: Status code indicating the entity's standing with the Secretary of State.
        right_to_transact_business_code: Code indicating the entity's right to conduct business in Texas.
        current_exempt_reason_code: Code indicating the reason for franchise tax exemption (if applicable).
        exempt_begin_date: Date when the franchise tax exemption began (if applicable).
        naics_code: North American Industry Classification System code for the business.
    """
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
    current_exempt_reason_code: Optional[str]
    exempt_begin_date: Optional[date]
    naics_code: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create instance from a dictionary.

        Parses a dictionary (typically from JSON API response) and constructs
        a FranchiseTaxPermitHolderData instance with properly typed fields. Note that
        the Secretary of State file number field has a long key name in the source data,
        and the NAICS code is retrieved from an unusual field name "_621111".

        Args:
            data: Dictionary containing the raw data from the API response.

        Returns:
            A new FranchiseTaxPermitHolderData instance with parsed and typed data.
        """
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
            current_exempt_reason_code = data.get("current_exempt_reason_code"),
            exempt_begin_date = parse_date(data.get("exempt_begin_date")),
            naics_code = data.get("_621111")
        )