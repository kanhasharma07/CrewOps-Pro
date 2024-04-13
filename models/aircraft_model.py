from typing import Optional
from pydantic import BaseModel, field_validator


class AircraftModel(BaseModel):
    """
    AircraftModel class represents an aircraft model with various attributes and validations.

    Attributes:
    - msn (int): The unique identification number of the aircraft.
    - actype (str): The type of the aircraft.
    - regn (str): The registration number of the aircraft.
    - availability (bool): The availability status of the aircraft.
    - engine (Optional[str]): The engine type of the aircraft (optional).
    - engine_hours (int): The number of hours the engine has been used.

    Validations:
    - is_msn_valid(cls, value): Validates the msn attribute. Raises ValueError if msn is empty.
    - is_actype_valid(cls, value): Validates the actype attribute. Raises ValueError if actype is empty, contains non-alphanumeric characters, or is not exactly 4 characters long.
    - is_regn_valid(cls, value): Validates the regn attribute. Raises ValueError if regn is empty.
    - is_availability_valid(cls, value): Validates the availability attribute. Raises ValueError if availability is not a boolean.

    """
    
    # Data Fields
    msn: int
    actype: str
    regn: str
    availability: bool
    engine: Optional[str]
    engine_hours: int

    # Validations
    # MSN Validation
    @field_validator("msn")
    @classmethod
    def is_msn_valid(cls, value):
        # Should not be Empty
        if not value:
            raise ValueError("MSN can not be empty")
        return value

    # A/C type validation
    @field_validator("actype")
    @classmethod
    def is_actype_valid(cls, value: str):
        if not value:
            raise ValueError("A/C Type cannot be empty.")
        if not value.isalnum():
            raise ValueError("A/C Type must only contain 4 Alphanumeric Charaters")
        if len(value) != 4:
            raise ValueError("Provide a valid 4 character A/C Type Certification")
        return value.title()

    # Registration Validation
    @field_validator("regn")
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
        if not isinstance(value, bool):
            raise ValueError("Availability value should be a boolean.")
        return value
