from datetime import date
from typing import Optional
from pydantic import BaseModel, field_validator

class FlightCrew(BaseModel):
    
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
    login: Optional[str]
    pw: str
    
    
    # Validations
    # StaffID Validation
    @field_validator("sap")
    @classmethod
    def is_sap_valid(cls, sap_value):
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
        sap_str = str(sap_value)
        if len(sap_str) != sap_len:
            raise ValueError(f"SAP (Staff ID) Must be exactly {sap_len} digits long.")
        return sap_value
    
    # First Name Validation
    @field_validator("fname")
    @classmethod
    def is_fname_valid(cls, fname_value):
        """
        Check if the first name value is valid.

        Parameters:
        - fname_value (str): The first name value to be validated. Auto-passed.

        Raises:
        - ValueError: If the first name value is empty or contains any special characters.

        Returns:
        - str: The validated first name value.

        """
        if not fname_value:
            raise ValueError("First name cannot be empty.")
        if not fname_value.isalpha():
            raise ValueError("First name should only contain alphabetic characters.")
        return fname_value.title()

    # Last Name Validation
    @field_validator("lname")
    @classmethod
    def is_lname_valid(cls, lname_value):
        """
        Check if the last name value is valid.

        Parameters:
        - lname_value (str): The last name value to be validated. Auto-passed.

        Raises:
        - ValueError: If the last name value is empty or contains any special characters.

        Returns:
        - str: The validated last name value.

        """
        if not lname_value:
            raise ValueError("Last name cannot be empty.")
        if not lname_value.isalpha():
            raise ValueError("Last name should only contain alphabetic characters.")
        return lname_value.title()
    
    # Designation Validation
    @field_validator("desig")
    @classmethod
    def is_desig_valid(cls, desig_value):
        """
        Check if the designation value is valid.

        Parameters:
        - desig_value (str): The designation value to be validated. Auto-passed.

        Raises:
        - ValueError: If the designation value is empty or contains any special characters.

        Returns:
        - str: The validated designation value.

        """
        if not desig_value:
            raise ValueError("Designation cannot be empty.")
        if not desig_value.replace(" ", "").isalpha():
            raise ValueError("Designation should only contain alphabetic characters and spaces.")
        return desig_value.title()
    
    # Mobile Number Validation
    @field_validator("mob")
    @classmethod
    def is_mob_valid(cls, mob_value):
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
        mob_str = str(mob_value)
        if len(mob_str) != mob_len:
            raise ValueError(f"Mobile number Must be exactly {mob_len} digits long.")
        return mob_value
    
    # ATPL Holder Validation
    @field_validator("atpl_holder")
    @classmethod
    def is_atpl_holder_valid(cls, atpl_holder_value):
        """
        Check if the ATPL holder value is valid.

        Parameters:
        - atpl_holder_value (bool): The ATPL holder value to be validated. Auto-passed.

        Raises:
        - ValueError: If the ATPL holder value is not a boolean.

        Returns:
        - bool: The validated ATPL holder value.

        """
        if not isinstance(atpl_holder_value, bool):
            raise ValueError("ATPL holder value should be a boolean.")
        return atpl_holder_value
    
    # Licence No. Validity
    @field_validator("licence")
    @classmethod
    def is_licence_valid(cls, licence_value):
        """
        Check if the license value is valid.

        Parameters:
        - licence_value (int): The license value to be validated. Auto-passed.

        Raises:
        - ValueError: If the license value is negative or empty.

        Returns:
        - int: The validated license value.

        """

        if licence_value < 0:
            raise ValueError("License value cannot be negative.")
        if not licence_value:
            raise ValueError("Licence Number is mandatory and can not be empty")
        return licence_value
    
    # Medical Validity Validation
    @field_validator("medical_validity")
    @classmethod
    def is_medical_validity_valid(cls, medical_validity_value):
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
        if medical_validity_value < today:
            raise ValueError("Medical validity date cannot be in the past.")
        return medical_validity_value
    
    # Base Ops Validation
    @field_validator("base_ops")
    @classmethod
    def is_base_ops_valid(cls, base_ops_value):
        """
        Check if the base ops value is valid.

        Parameters:
        - base_ops_value (str): The base ops value to be validated. Auto-passed.

        Raises:
        - ValueError: If the base ops value is not exactly 3 alphabetical characters.

        Returns:
        - str: The validated base ops value.

        """
        if not base_ops_value:
            raise ValueError("Base ops cannot be empty.")
        if not base_ops_value.isalpha() or len(base_ops_value) != 3:
            raise ValueError("Base ops should only contain 3 alphabetical characters.")
        return base_ops_value.upper()
    
    # Availability Validation
    @field_validator("availability")
    @classmethod
    def is_availability_valid(cls, availability_value):
        """
        Check if the availability value is valid.

        Parameters:
        - availability_value (bool): The availability value to be validated. Auto-passed.

        Raises:
        - ValueError: If the availabilty value is not a boolean.

        Returns:
        - bool: The validated availability value.

        """
        if not isinstance(availability_value, bool):
            raise ValueError("Availability value should be a boolean.")
        return availability_value
    
    # Login Validation
    @field_validator("login")
    @classmethod
    def is_login_valid(cls, login_value, values):
        """
        Check if the login value is valid.

        Parameters:
        - login_value (str): The login value to be validated. Auto-passed.

        Raises:
        - ValueError: If the login value is not alphanumeric.

        Returns:
        - str: The validated login value of SAP if "login" was empty, else returns provided value.

        """
        #Raise error if login is not alphanumeric
        if not login_value.isalnum():
            raise ValueError("Login may only contain alphanumeric characters") 
        
        # Check if provided login value is unique
        def login_isUnique():
            pass
        
        validated_login = values.get("sap") if not login_value else login_value
        return validated_login

    #Password Validation
    @field_validator("pw")
    @classmethod
    def is_pw_valid(cls, pw_value):
        """
        Check if the password value is valid.

        Parameters:
        - pw_value (str): The password value to be validated. Auto-passed.

        Raises:
        - ValueError: If the password value is empty.

        Returns:
        - str: The validated password value.

        """
        if not pw_value:
            raise ValueError("Password cannot be empty.")
        return pw_value
    
    