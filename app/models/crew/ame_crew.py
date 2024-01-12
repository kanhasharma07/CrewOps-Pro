from typing import Any, Optional
from pydantic import BaseModel, field_validator

class AMECrew(BaseModel):
    """
    AMECrew class represents a crew member in the AME (Aircraft Maintenance Engineer) system.

    Attributes:
        sap (int): The SAP (Staff ID) of the crew member. Must be exactly 8 digits long.
        name (str): The name of the crew member. Should only contain alphabetic characters and spaces, and should not exceed 255 characters.
        fleet_cert (str): The fleet certification of the crew member. Must be exactly 4 alphanumeric characters.
        login (Optional[str]): The login of the crew member. If not provided, it will be set to the SAP value.
        pw (str): The password of the crew member. Should not exceed 20 characters.
    """
    # Data Fields
    sap: int
    name: str
    fleet_cert: str
    login: Optional[str] = None
    pw: str
    
    #INIT to set Login = SAP
    def model_post_init(self, __context: Any) -> None:
        if self.login is None:
            self.login = str(self.sap)
        return super().model_post_init(__context)
    
    # Validations
    # SAP Validation
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
    
    # Name Validation
    @field_validator("name")
    @classmethod
    def is_name_valid(cls, value):
        """
        Check if the name value is valid.

        Parameters:
        - fname_value (str): The name value to be validated. Auto-passed.

        Raises:
        - ValueError: If the name value is empty or contains any special characters or is longer than 255 chars.

        Returns:
        - str: The validated name value.

        """
        if not value:
            raise ValueError("Name cannot be empty.")
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name should only contain alphabetic characters and spaces.")
        if len(value) > 255:
            raise ValueError("Name length should not exceed 255 characters.")
        return value.title()
    
    # Fleet Certified Validation
    @field_validator("fleet_cert")
    @classmethod
    def is_fleet_valid(cls, value):
        """
        Check if the Fleet Certification value is valid.

        Parameters:
        - value (str): The fleet_cert value to be validated. Auto-passed.

        Raises:
        - ValueError: If the fleet_cert value is empty or contains any non-alphanumeric characters or is not exactly 4 characters long.

        Returns:
        - str: The validated fleet_cert value.

        """
        if not value:
            raise ValueError("Fleet cannot be empty.")
        if not value.isalnum():
            raise ValueError("Fleet must only contain 4 Alphanumeric Charaters")
        if len(value) != 4:
            raise ValueError("Provide a valid 4 character Fleet Certification")
        return value.title()
    
    # Login Validation
    @field_validator("login")
    @classmethod
    def is_login_valid(cls, value):
        """
        Check if the login value is valid.

        Parameters:
        - login_value (str): The login value to be validated. Auto-passed.

        Raises:
        - ValueError: If the login value is not alphanumeric or exceeds 20 chars in length

        Returns:
        - str: Provided "login" value.

        """
            
        # Raise error if login is not alphanumeric
        if not value.isalnum():
            raise ValueError("Login may only contain alphanumeric characters")
        if len(value) > 20:
            raise ValueError("Login length should not exceed 20 characters.")  
        # Check if provided login value is unique
        def login_isUnique():
            pass
            
        return value  # Return the login value
    # Password Validation
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
    