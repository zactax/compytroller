import httpx
from typing import List
from src.data.responses.franchise_tax import FranchiseTaxPermitHolderData
from src.data.exceptions import HttpError, InvalidRequest

class ActiveFranchiseTaxPermitHolders:
    DATASET_ID = "9cir-efmm"

    def __init__(self, socrata_client):
        self.client = socrata_client
        self._params = {}
        self._where_clauses = []
        
    def for_taxpayer(self, number: str):
        self._params["taxpayer_number"] = number
        return self
    
    def in_city(self, city: str):
        self._params["taxpayer_city"] = city.upper()
        return self
    
    def for_org_type(self, org_type: str):
        """
        AB          TEXAS BUSINESS ASSOC            
        AC          FRGN BUSINESS ASSOC             
        AF          FOREIGN PROFESSIONAL ASSOCIATION
        AP          TEXAS PROFESSIONAL ASSOCIATION  
        AR          OTHER ASSOCIATION               
        C           CORPORATION                     
        CF          FOREIGN PROFIT CORPORATION      
        CI          FOREIGN LMTD LIAB CO - OOS      
        CL          TEXAS LIMITED LIABILITY COMPANY 
        CM          FOREIGN NON-PROFIT CORP - OOS   
        CN          TEXAS NON-PROFIT CORPORATION    
        CP          TEXAS PROFESSIONAL CORPORATION  
        CR          TEXAS INSURANCE CORPORATION     
        CS          FOREIGN INSURANCE CORP - OOS    
        CT          TEXAS PROFIT CORPORATION        
        CU          FOREIGN PROFESSIONAL CORPORATION
        CW          TEXAS RAILROAD CORPORATION                          
        CX          FOREIGN RAILROAD CORPORATION                        
        DC          REGISTERED DATA CENTER
        ES          ESTATE                                              
        FA          FINANCIAL INSTITUTION - STATE SAVINGS & LOAN - OOS  
        FB          FINANCIAL INSTITUTION - STATE SAVINGS B ANK - TX    
        FC          FINANCIAL INSTITUTION - FEDERAL CREDIT UNION        
        FD          FINANCIAL INSTITUTION - STATE SAVINGS & LOAN - TX   
        FE          FINANCIAL INSTITUTION - FEDERAL SAVINGS & LOAN-TX   
        FF          FINANCIAL INSTITUTION - FEDERAL BANK - TX           
        FG          FINANCIAL INSTITUTION - FEDERAL SAVINGS BANK - TX   
        FH          FINANCIAL INSTITUTION - STATE SAVINGS BANK - OOS    
        FI          FINANCIAL INSTITUTION - STATE CREDIT UNION - TX     
        FJ          FINANCIAL INSTITUTION - FEDERAL BANK - OOS    
        FK          FINANCIAL INSTITUTION - FEDERAL SAVINGS BANK - OOS  
        FL          FINANCIAL INSTITUTION - STATE LIMITED BANK ASSOC    
        FM          FINANCIAL INSTITUTION - TRUST COMPANY              
        FN          FINANCIAL INSTITUTION - FEDERAL SAVINGS & LOAN-OOS 
        FO          FINANCIAL INSTITUTION - STATE BANK - OOS           
        FP          FINANCIAL INSTITUTION                              
        FR          FINANCIAL INSTITUTION - FOREIGN COUNTRY BANK       
        FS          FINANCIAL INSTITUTION - STATE BANK - TX            
        FT          FINANCIAL INSTITUTION - STATE CREDIT UNION - OOS   
        GC          CITY                                               
        GD          FEDERAL AGENCY                                     
        GF          STATE AGENCY - OOS                                 
        GJ          JUNIOR COLLEGE                                     
        GL          LOCAL OFFICIAL                                     
        GM          MASS TRANSIT                                       
        GO          COUNTY                                             
        GP          SPECIAL PURPOSE DISTRICT                           
        GR          RAPID TRANSIT              
        GS          SCHOOL DISTRICT            
        GT          STATE AGENCY - TX          
        GU          STATE COLLEGE/UNIVERSITY   
        GY          COMMUNITY COLLEGE          
        HF          FRGN HOLDING COMPANY       
        HS          HISTORIC STRUCTURE
        IS          INDIVIDUAL - SOLE OWNER    
        J           JOINT VENTURE              
        L           LIMITED (LIABILITY) COMPANY
        M           LIMITED (LIABILITY) PARTNERSHIP 
        O           OTHER                           
        P           GENERAL PARTNERSHIP             
        PB          BUS GENERAL PRTNSHP             
        PF          FRGN LIMITED PRTNSHP            
        PI          IND GENERAL PRTNSHP             
        PL          TX LIMITED PRTNSHP              
        PO          OIL & GAS SPECIAL               
        PV          TEXAS JOINT VENTURE             
        PW          FRGN JOINT VENTURE              
        PX          TX LLP REGISTRATION             
        PY          FRGN LLP REGISTRATION           
        PZ          IND SUCCESSOR PRTSHP            
        S           SOLE PROPRIETORSHIP             
        SF          FRGN JOINT STOCK CO             
        ST          TEXAS JOINT STOCK CO            
        TF          FOREIGN BUSINESS TRUST               
        TH          TX RL EST INV TRST                   
        TI          FOREIGN REAL ESTATE INVESTMENT TRUST 
        TR          TRUST                                
        UF          UNKNOWN - FRANCHISE                  
        UK          UNKNOWN  
        """
        self._params["taxpayer_organizational_type"] = org_type.upper()
        return self
    
    def with_right_to_transact(self, status: str):
        """
        A = Active
        D = Active - Eligible for Termination/Withdrawal
        N = Forfeited
        I = Franchise Tax Involuntarily Ended
        U = Franchise Tax Not Established
        blank = Franchise Tax Ended
        """
        self._params["right_to_transact_business_code"] = status.upper()
        return self
    
    def with_exempt_reason(self, reason: str):
        """
        00 = Not Exempt
        01 = Gross Receipts, Sec.171.052
        02 = Railway Terminal Corporation, Sec.171.053
        03 = Nonprofit Corporation Organized to Promote County, City or,
            Another Area, Sec.171.057
        04 = Nonprofit Corporation Organized for Religious Purposes,
            Sec.171.058
        05 = Nonprofit Corporation Organized to Provide Burial Places,
            Sec.171.059
        06 = Nonprofit Corporation Organized for Agricultural Purposes,
            Sec.171.060
        07 = Nonprofit Corporation Organized for Educational Purposes,
            Sec.171.061
        08 = Nonprofit Corporation Organized for Public Charity,
            Sec.171.062
        09 = Savings and Loan Association, Sec.171.054
        10 = Open-End Investment Company, Sec.171.055
        11 = Nonprofit Corporation Organized for Conservation Purposes,
            Sec.171.064
        12 = Nonprofit Corporation Organized to Provide Water Supply or 
            Sewer Services, Sec.171.064
        13 = Nonprofit Corporation involved with City Natural Gas 
            Facility, Sec.171.066
        14 = Nonprofit Corporation Organized to provide Convalescent 
            Homes for Elderly, Sec.171.067
        15 = Nonprofit Corporation Organized to provide Cooperative 
            Housing, Sec.171.068
        16 = Lodges, Sec.171.070
        17 = Provisional - 90 Day Temporary Exemption Granted by the 
            Comptroller's Office
        18 = Corporation with Business Interest in Solar Energy Devices,
            Sec.171.056
        19 = 501(c)(3) Nonprofit Corporation Exempt From Federal Income
            Tax, Sec.171.063
        20 = 501(c)(4) Nonprofit Corporation Exempt From Federal Income 
            Tax, Sec.171.063
        21 = 501(c)(5) Nonprofit Corporation Exempt From Federal Income 
            Tax, Sec.171.063
        22 = 501(c)(6) Nonprofit Corporation Exempt From Federal Income 
            Tax, Sec.171.063
        23 = 501(c)(7) Nonprofit Corporation Exempt From Federal Income 
            Tax, Sec.171.063
        24 = Certain Homeowners' Associations, Sec.171.082
        25 = Marketing Associations, Sec.171.069
        26 = Farmers' Cooperative Society, Sec.171.071
        27 = Housing Finance Corporation, Sec.171.072
        28 = Hospital Laundry Cooperative Association, Sec.171.073
        29 = Development Corporation, Sec.171.074
        30 = Cooperative Association, Sec.171.075
        31 = Cooperative Credit Association, Sec.171.076
        32 = Credit Union, Sec.171.077
        33 = Banks, Sec.171.078
        34 = Electric Cooperative Corporation, Sec.171.079
        35 = Telephone Cooperative Corporation, Sec.171.080
        36 = Emergency Medical Service Corporation, Sec.171.083
        37 = 501(c)(3) Special, Assigned by the Comptroller's Office
        38 = 501(c)(4) Special, Assigned by the Comptroller's Office
        39 = 501(c)(5) Special, Assigned by the Comptroller's Office
        40 = 501(c)(6) Special, Assigned by the Comptroller's Office
        41 = 501(c)(7) Special, Assigned by the Comptroller's Office
        42 = Corporation Exempt by Another Law, Sec.171.081
        43 = 501(c)(2) Special, Assigned by the Comptroller's Office
        44 = 501(c)(25) Special, Assigned by the Comptroller's Office
        45 = Certain Trade Show Participants, Sec.171.084
        46 = 501(c)(16) Special, Assigned by the Comptroller's Office
        47 = Sludge Recycling Operation, Sec.171.085
        48 = Corporations Formed by the Texas National Research 
            Laboratory Commission, Sec.171.086
        49 = Exemption by Secretary of State is being honored by the 
            Comptroller
        50 = 501(c)(8) Nonprofit Corporation Exempt From Federal Income 
            Tax, Sec.171.063
        51 = 501(c)(10) Nonprofit Corporation Exempt From Federal Income 
            Tax, Sec.171.063
        52 = 501(c)(19) Nonprofit Corporation Exempt From Federal Income 
            Tax, Sec.171.063
        53 = Nonprofit Corporation Organized for Student Loan Funds or 
            Student Scholarship Purpose, Sec.171.087
        54 = Public Interest-Volunteer Fire Dept.
        55 = Public Interest-Texas Transportation Code
        56 = Public Interest-Chamber of Commerce
        57 = Public Interest-Youth Athletic Organization
        58 = Public Interest-Tourist Organizations
        59 = Other Chapter-Repealed- Ag Code, Section 57.085
        60 = Other Chapter-Local government code
        61 = Other Chapter-State Government Entity
        62 = Other Chapter-Local Government Entity
        63 = Other Chapter-Federal Government Entity
        64 = Other Chapter-Health and Safety Code, 221.033
        65 = Other Chapter-Education Code 53.35(b)
        66 = Nonprofit 501(c)(3) GROUP 
        67 = Nonprofit 501(c)(4) GROUP 
        68 = Nonprofit 501(c)(8) GROUP 
        69 = Nonprofit 501(c)(10) GROUP
        70 = Nonprofit 501(c)(19) GROUP
        71 = Nonprofit 501(c)(6)       
        72 = Nonprofit 501(c)(6)             
        73 = Cooperative Association-Health and Safety Code 301.042
        74 = Religious/Independent-religious org, not recognized under a group 
        75 = Other Chapter-Article 1528(m)
        76 = Other Chapter-Section 151.307(A)
        77 = Other Chapter-Government Code Section481.024
        78 = Other Chapter-Government Code 2306.556
        79 = Public Interest-Article 1396
        80 = Public Interest-Local Government Code 39288
        88 = Educational-Out of State Institute of Higher Education, no  hotel
        89 = Public Interest-Beach Clean-up, Hotel only
        90 = Nonprofit 501(c)(3)             
        91 = Nonprofit 501(c)(4)             
        92 = PUBLIC INTEREST           
        93 = Nonprofit 501(c)(6)             
        94 = Nonprofit 501(c)(8)*            
        95 = Nonprofit 501(c)(10)*           
        96 = Nonprofit 501(c)(19)*           
        97 = OTHER CHAPTER  
        98 = 501(c)(2) GROUP
        99 = 501(c)(5) GROUP
        100 = 501(c)(6) GROUP 
        101 = 501(c)(7) GROUP 
        102 = 501(c)(16) GROUP
        """
        self._params["current_exempt_reason_code"] = reason
        return self
    
    def responsibility_begin_before(self, date: str):
        self._where_clauses.append(f"responsibility_beginning_date < '{date}'")
        return self
    
    def responsibility_begin_after(self, date: str):
        self._where_clauses.append(f"responsibility_beginning_date > '{date}'")
        return self
    
    def responsibility_begin_between(self, start: str, end: str):
        self._where_clauses.append(
            f"responsibility_beginning_date BETWEEN '{start}' AND '{end}'"
        )
        return self
    
    def exempt_begin_before(self, date: str):
        self._where_clauses.append(f"exempt_begin_date < '{date}'")
        return self
    
    def exempt_begin_after(self, date: str):
        self._where_clauses.append(f"exempt_begin_date > '{date}'")
        return self
    
    def exempt_begin_between(self, start: str, end: str):
        self._where_clauses.append(
            f"exempt_begin_date BETWEEN '{start}' AND '{end}'"
        )
        return self
    
    def for_naics_code(self, naics_code: str):
        self._params["_621111"] = naics_code
        return self
    
    def sort_by(self, field: str, desc: bool = False):
        self._params["$order"] = f"{field} DESC" if desc else field
        return self
    
    def limit(self, n: int):
        self._params["$limit"] = n
        return self
    
    def reset(self):
        self._params = {}
        self._where_clauses = []
        return self

    def get(self) -> List[FranchiseTaxPermitHolderData]:
        if self._where_clauses:
            self._params["$where"] = " AND ".join(self._where_clauses)
        
        try:
            records = self.client.get(self.DATASET_ID, self._params)
        except httpx.HTTPStatusError as exc:
            raise HttpError.from_httpx_exception(exc)
        except httpx.RequestError as exc:
            raise HttpError(str(exc))

        if not records:
            raise InvalidRequest("No records returned from Active Franchise Tax Permit Holders dataset")

        return [FranchiseTaxPermitHolderData.from_dict(r) for r in records]