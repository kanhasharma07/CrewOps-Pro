from datetime import date
from typing import Any, Optional
from pydantic import BaseModel, field_validator

class FlightCrewModel(BaseModel):
    """
    FlightCrew class represents a flight crew member.

    Attributes:
        sap (int): The SAP (Staff ID) of the crew member.
        fname (str): The first name of the crew member.
        lname (str): The last name of the crew member.
        desig (str): The designation of the crew member.
        mob (int): The mobile number of the crew member.
        atpl_holder (bool): Indicates whether the crew member holds an ATPL license.
        licence (int): The license number of the crew member.
        medical_validity (date): The date of medical validity for the crew member.
        base_ops (str): The base operations of the crew member.
        availability (bool): Indicates whether the crew member is available.
        login (Optional[str]): The login of the crew member. Defaults to None.
        pw (str): The password of the crew member.
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

    #INIT to set Login=SAP
    def model_post_init(self, __context: Any) -> None:
        if self.login is None:
            self.login = str(self.sap)
        return super().model_post_init(__context)
    
    # Validations
    # StaffID Validation
    @field_validator("sap")
    @classmethod
    def is_sap_valid(cls, value):
        """
        Check if the SAP (Staff ID) value is valid.

        Parameters:
        - sap_value (int): The SAP (Staff ID) value to be validated. Auto-passed.

        Raises:
        - ValueError: If the SAP (Staff ID) value is not exactly 8 digits long.

        Returns:
        - int: The validated SAP (Staff ID) value.

        """
        sap_len = 8
        sap_str = str(value)
        if len(sap_str) != sap_len:
            raise ValueError(f"SAP (Staff ID) Must be exactly {sap_len} digits long.")
        return value
    
    # First Name Validation
    @field_validator("fname")
    @classmethod
    def is_fname_valid(cls, value):
        """
        Check if the first name value is valid.

        Parameters:
        - fname_value (str): The first name value to be validated. Auto-passed.

        Raises:
        - ValueError: If the first name value is empty or contains any special characters or is longer than 255 chars.

        Returns:
        - str: The validated first name value.

        """
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
    def is_lname_valid(cls, value):
        """
        Check if the last name value is valid.

        Parameters:
        - lname_value (str): The last name value to be validated. Auto-passed.

        Raises:
        - ValueError: If the last name value is empty or contains any special characters, or is longer than 255 chars.

        Returns:
        - str: The validated last name value.

        """
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
    def is_desig_valid(cls, value):
        """
        Check if the designation value is valid.

        Parameters:
        - desig_value (str): The designation value to be validated. Auto-passed.

        Raises:
        - ValueError: If the designation value is empty, contains any special characters, or exceeds the length limit.

        Returns:
        - str: The validated designation value.

        """
        if not value:
            raise ValueError("Designation cannot be empty.")
        if not value.replace(" ", "").isalpha():
            raise ValueError("Designation should only contain alphabetic characters and spaces.")
        if len(value) > 255:
            raise ValueError("Designation length should not exceed 255 characters.")
        return value.upper()
    
    # Mobile Number Validation
    @field_validator("mob")
    @classmethod
    def is_mob_valid(cls, value):
        """
        Check if the mobile number value is valid.

        Parameters:
        - mob_value (int): The mobile number value to be validated. Auto-passed.

        Raises:
        - ValueError: If the mobile number value is not exactly 10 digits long.

        Returns:
        - int: The validated mobile number value.

        """
        mob_len = 10
        mob_str = str(value)
        if len(mob_str) != mob_len:
            raise ValueError(f"Mobile number Must be exactly {mob_len} digits long.")
        return value
    
    # ATPL Holder Validation
    @field_validator("atpl_holder")
    @classmethod
    def is_atpl_holder_valid(cls, value):
        """
        Check if the ATPL holder value is valid.

        Parameters:
        - atpl_holder_value (bool): The ATPL holder value to be validated. Auto-passed.

        Raises:
        - ValueError: If the ATPL holder value is not a boolean.

        Returns:
        - bool: The validated ATPL holder value.

        """
        if not isinstance(value, bool):
            raise ValueError("ATPL holder value should be a boolean.")
        return value
    
    # Licence No. Validity
    @field_validator("licence")
    @classmethod
    def is_licence_valid(cls, value):
        """
        Check if the license value is valid.

        Parameters:
        - licence_value (int): The license value to be validated. Auto-passed.

        Raises:
        - ValueError: If the license value is negative or empty.

        Returns:
        - int: The validated license value.

        """

        if value < 0:
            raise ValueError("License value cannot be negative.")
        if not value:
            raise ValueError("Licence Number is mandatory and can not be empty")
        return value
    
    # Medical Validity Validation
    @field_validator("medical_validity")
    @classmethod
    def is_medical_validity_valid(cls, value):
        """
        Check if the medical validity value is valid.

        Parameters:
        - medical_validity_value (date): The medical validity value to be validated. Auto-passed.

        Raises:
        - ValueError: If the medical validity value is in the past.

        Returns:
        - date: The validated medical validity value.

        """
        today = date.today()
        if value < today:
            raise ValueError("Medical validity date cannot be in the past.")
        return value
    
    # Base Ops Validation
    @field_validator("base_ops")
    @classmethod
    def is_base_ops_valid(cls, value):
        """
        Check if the base ops value is valid.

        Parameters:
        - base_ops_value (str): The base ops value to be validated. Auto-passed.

        Raises:
        - ValueError: If the base ops value is not exactly 3 alphabetical characters.

        Returns:
        - str: The validated base ops value.

        """
        if not value:
            raise ValueError("Base ops cannot be empty.")
        if not value.isalpha() or len(value) != 3:
            raise ValueError("Base ops should only contain 3 alphabetical characters.")
        return value.upper()
    
    # Availability Validation
    @field_validator("availability")
    @classmethod
    def is_availability_valid(cls, value):
        """
        Check if the availability value is valid.

        Parameters:
        - availability_value (bool): The availability value to be validated. Auto-passed.

        Raises:
        - ValueError: If the availabilty value is not a boolean.

        Returns:
        - bool: The validated availability value.

        """
        if not isinstance(value, bool):
            raise ValueError("Availability value should be a boolean.")
        return value
    
    # Login Validation
    @field_validator("login")
    @classmethod
    def is_login_valid(cls, value):
        """
        Check if the login value is valid.

        Parameters:
        - login_value (str): The login value to be validated. Auto-passed.

        Raises:
        - ValueError: If the login value is a duplicate.
        Returns:
        - str: Provided "login" value.

        """ 
        
        # Check if provided login value is unique
        def login_isUnique():
            pass
            
        return value  # Return the modified login value

    #Password Validation
    @field_validator("pw")
    @classmethod
    def is_pw_valid(cls, value):
        """
        Check if the password value is valid.

        Parameters:
        - pw_value (str): The password value to be validated. Auto-passed.

        Raises:
        - ValueError: If the password value is empty.

        Returns:
        - str: The validated password value.

        """
        if not value:
            raise ValueError("Password cannot be empty.")
        if len(value) > 20:
            raise ValueError("Password length should not exceed 20 characters.")
        return value
