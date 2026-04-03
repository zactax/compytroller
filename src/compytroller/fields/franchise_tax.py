"""Field enums for franchise tax datasets.

Provides ``str``-based enums for Socrata column names exposed by the
franchise tax resources, plus categorical enums for common filter values.
"""

from ._base import FieldEnum


class FranchiseTaxPermitHolderField(FieldEnum):
    """Sortable fields for the Active Franchise Tax Permit Holders dataset (9cir-efmm)."""

    TAXPAYER_NUMBER = "taxpayer_number"
    TAXPAYER_NAME = "taxpayer_name"
    TAXPAYER_ADDRESS = "taxpayer_address"
    TAXPAYER_CITY = "taxpayer_city"
    TAXPAYER_STATE = "taxpayer_state"
    TAXPAYER_ZIP = "taxpayer_zip"
    TAXPAYER_COUNTY_CODE = "taxpayer_county_code"
    TAXPAYER_ORGANIZATIONAL_TYPE = "taxpayer_organizational_type"
    RECORD_TYPE_CODE = "record_type_code"
    RESPONSIBILITY_BEGINNING_DATE = "responsibility_beginning_date"
    SECRETARY_OF_STATE_FILE_NUMBER = "secretary_of_state_sos_or_coa_file_number"
    SOS_CHARTER_DATE = "sos_charter_date"
    SOS_STATUS_DATE = "sos_status_date"
    SOS_STATUS_CODE = "sos_status_code"
    RIGHT_TO_TRANSACT_BUSINESS_CODE = "right_to_transact_business_code"
    CURRENT_EXEMPT_REASON_CODE = "current_exempt_reason_code"
    EXEMPT_BEGIN_DATE = "exempt_begin_date"
    NAICS_CODE = "_621111"


# ---------------------------------------------------------------------------
# Categorical enums
# ---------------------------------------------------------------------------


class RightToTransactCode(FieldEnum):
    """Right-to-transact business status codes for franchise tax permit holders.

    Used with ``with_right_to_transact()`` on
    :class:`ActiveFranchiseTaxPermitHolders`.
    """

    ACTIVE = "A"
    ELIGIBLE_FOR_TERMINATION = "D"
    FORFEITED = "N"
    INVOLUNTARILY_ENDED = "I"
    NOT_ESTABLISHED = "U"
