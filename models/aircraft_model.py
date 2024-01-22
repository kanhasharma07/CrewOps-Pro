from typing import Optional
from pydantic import BaseModel, field_validator


class AircraftModel(BaseModel):
    
    # Data Fields
    msn: int
    actype: str
    regn: str
    availability: bool
    engine: Optional[str]
    engine_hours: int
    
    # Validations
    # MSN Validation
    @field_validator('msn')
    @classmethod
    def is_msn_valid(cls, value):
        # Should not be Empty
        if not value:
            raise ValueError('MSN can not be empty')
        
        # should be unique
        def is_msn_unique():
            pass
            return True
        if not is_msn_unique():
            raise ValueError('MSN is already assigned to an Airframe')
        
        return value
    
    # A/C type validation
    @field_validator("actype")
    @classmethod
    def is_actype_valid(cls, value):
        """
        Check if the A/C Type value is valid.

        Parameters:
        - value (str): The A/C Type value to be validated. Auto-passed.

        Raises:
        - ValueError: If the A/C Type value is empty or contains any non-alphanumeric characters or is not exactly 4 characters long.

        Returns:
        - str: The validated A/C Type value.

        """
        if not value:
            raise ValueError("A/C Type cannot be empty.")
        if not value.isalnum():
            raise ValueError("A/C Type must only contain 4 Alphanumeric Charaters")
        if len(value) != 4:
            raise ValueError("Provide a valid 4 character A/C Type Certification")
        return value.title()
    
    # Registration Validation    
    @field_validator('regn')
    @classmethod
    def is_regn_valid(cls, value: str):
        # Not Empty
        if not value:
            raise ValueError("Registration cannot be empty.")
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
    
