from datetime import date
from typing import Any, Optional
from pydantic import BaseModel, field_validator


class FlightCrewModel(BaseModel):
    """
    FlightCrewModel class represents a model for flight crew members.

    Attributes:
        sap (int): The SAP (Staff ID) of the flight crew member.
        fname (str): The first name of the flight crew member.
        lname (str): The last name of the flight crew member.
        desig (str): The designation of the flight crew member.
        mob (int): The mobile number of the flight crew member.
        atpl_holder (bool): Indicates whether the flight crew member is an ATPL holder or not.
        licence (int): The license number of the flight crew member.
        medical_validity (date): The medical validity date of the flight crew member.
        base_ops (str): The base operations of the flight crew member.
        availability (bool): Indicates whether the flight crew member is available or not.
        login (Optional[str]): The login of the flight crew member. Defaults to None.
        pw (str): The password of the flight crew member.

    Methods:
        model_post_init(__context: Any) -> None:
            Initializes the login attribute to the SAP value if it is None.
        
        is_sap_valid(value) -> int:
            Validates the SAP (Staff ID) value.
            - The SAP value must be exactly 8 digits long.
        
        is_fname_valid(value) -> str:
            Validates the first name value.
            - The first name cannot be empty.
            - The first name should only contain alphabetic characters.
            - The length of the first name should not exceed 255 characters.
        
        is_lname_valid(value: str) -> str:
            Validates the last name value.
            - The last name cannot be empty.
            - The last name should only contain alphabetic characters.
            - The length of the last name should not exceed 255 characters.
        
        is_desig_valid(value: str) -> str:
            Validates the designation value.
            - The designation cannot be empty.
            - The designation should only contain alphabetic characters and spaces.
            - The length of the designation should not exceed 255 characters.
        
        is_mob_valid(value) -> int:
            Validates the mobile number value.
            - The mobile number must be exactly 10 digits long.
        
        is_atpl_holder_valid(value) -> bool:
            Validates the ATPL holder value.
            - The ATPL holder value should be a boolean.
        
        is_licence_valid(value) -> int:
            Validates the license value.
            - The license value cannot be negative.
            - The license number is mandatory and cannot be empty.
        
        is_medical_validity_valid(value) -> date:
            Validates the medical validity value.
            - The medical validity date cannot be in the past.
        
        is_base_ops_valid(value) -> str:
            Validates the base ops value.
            - The base ops cannot be empty.
            - The base ops should only contain 3 alphabetical characters.
        
        is_availability_valid(value) -> bool:
            Validates the availability value.
            - The availability value should be a boolean.
        
        is_pw_valid(value) -> str:
            Validates the password value.
            - The password cannot be empty.
            - The length of the password should not exceed 20 characters.
    """

    # Data Fields
    sap: int
    fname: str
    lname: str
    desig: str
    mob: int
    atpl_holder: bool
    licence: int
    medical_validity: date
    base_ops: str
    availability: bool
    login: Optional[str] = None
    pw: str

    # INIT to set Login=SAP
    def model_post_init(self, __context: Any) -> None:
        if self.login is None:
            self.login = str(self.sap)
        return super().model_post_init(__context)

    # Validations
    # StaffID Validation
    @field_validator("sap")
    @classmethod
    def is_sap_valid(cls, value):
        sap_len = 8
        sap_str = str(value)
        if len(sap_str) != sap_len:
            raise ValueError(f"SAP (Staff ID) Must be exactly {sap_len} digits long.")
        return value

    # First Name Validation
    @field_validator("fname")
    @classmethod
    def is_fname_valid(cls, value):
        if not value:
            raise ValueError("First name cannot be empty.")
        if not value.isalpha():
            raise ValueError("First name should only contain alphabetic characters.")
        if len(value) > 255:
            raise ValueError("First Name length should not exceed 255 characters.")
        return value.title()

    # Last Name Validation
    @field_validator("lname")
    @classmethod
    def is_lname_valid(cls, value: str):
        if not value:
            raise ValueError("Last name cannot be empty.")
        if not value.isalpha():
            raise ValueError("Last name should only contain alphabetic characters.")
        if len(value) > 255:
            raise ValueError("Last Name length should not exceed 255 characters.")
        return value.title()

    # Designation Validation
    @field_validator("desig")
    @classmethod
    def is_desig_valid(cls, value: str):
        if not value:
            raise ValueError("Designation cannot be empty.")
        if not value.replace(" ", "").isalpha():
            raise ValueError(
                "Designation should only contain alphabetic characters and spaces."
            )
        if len(value) > 255:
            raise ValueError("Designation length should not exceed 255 characters.")
        return value.upper()

    # Mobile Number Validation
    @field_validator("mob")
    @classmethod
    def is_mob_valid(cls, value):
        mob_len = 10
        mob_str = str(value)
        if len(mob_str) != mob_len:
            raise ValueError(f"Mobile number Must be exactly {mob_len} digits long.")
        return value

    # ATPL Holder Validation
    @field_validator("atpl_holder")
    @classmethod
    def is_atpl_holder_valid(cls, value):
        if not isinstance(value, bool):
            raise ValueError("ATPL holder value should be a boolean.")
        return value

    # Licence No. Validity
    @field_validator("licence")
    @classmethod
    def is_licence_valid(cls, value):
        if value < 0:
            raise ValueError("License value cannot be negative.")
        if not value:
            raise ValueError("Licence Number is mandatory and can not be empty")
        return value

    # Medical Validity Validation
    @field_validator("medical_validity")
    @classmethod
    def is_medical_validity_valid(cls, value):
        today = date.today()
        if value < today:
            raise ValueError("Medical validity date cannot be in the past.")
        return value

    # Base Ops Validation
    @field_validator("base_ops")
    @classmethod
    def is_base_ops_valid(cls, value):
        if not value:
            raise ValueError("Base ops cannot be empty.")
        if not value.isalpha() or len(value) != 3:
            raise ValueError("Base ops should only contain 3 alphabetical characters.")
        return value.upper()

    # Availability Validation
    @field_validator("availability")
    @classmethod
    def is_availability_valid(cls, value):
        if not isinstance(value, bool):
            raise ValueError("Availability value should be a boolean.")
        return value

    # Password Validation
    @field_validator("pw")
    @classmethod
    def is_pw_valid(cls, value):
        if not value:
            raise ValueError("Password cannot be empty.")
        if len(value) > 20:
            raise ValueError("Password length should not exceed 20 characters.")
        return value
