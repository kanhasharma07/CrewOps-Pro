from datetime import time
from pydantic import BaseModel, field_validator


class FlightModel(BaseModel):

    # Data Fields
    flight_no: int
    dep: str
    arr: str
    actype: str
    etd: str  # Estimated Time of Departure
    eta: str  # Estimated Time of Arrival
    duration: str

    # Validations
    # Flight_no Validation
    @field_validator("flight_no")
    @classmethod
    def is_flightno_valid(cls, value):
        # Length 5 or 6 only
        if not (len(str(value)) == 3 or len(str(value)) == 4):
            raise ValueError("Length of Flight Number must either 4 or 3")
        return value

    # DEP Validations
    @field_validator("dep")
    @classmethod
    def is_dep_valid(cls, value: str):
        """
        Check if the station IATA Code Value is valid.

        Parameters:
        - value (str): The base ops value to be validated. Auto-passed.

        Raises:
        - ValueError: If the IATA Code value is not exactly 3 alphabetical characters.

        Returns:
        - str: The validated base ops value.

        """
        if not value:
            raise ValueError("Departure/Arrival Station IATA Code cannot be empty.")
        if not value.isalpha() or len(value) != 3:
            raise ValueError(
                "Station IATA Code should only contain 3 alphabetical characters."
            )
        return value.upper()

    # ARR Validations
    @field_validator("arr")
    @classmethod
    def is_arr_valid(cls, value: str):
        """
        Check if the station IATA Code Value is valid.

        Parameters:
        - value (str): The base ops value to be validated. Auto-passed.

        Raises:
        - ValueError: If the IATA Code value is not exactly 3 alphabetical characters.

        Returns:
        - str: The validated base ops value.

        """
        if not value:
            raise ValueError("Departure/Arrival Station IATA Code cannot be empty.")
        if not value.isalpha() or len(value) != 3:
            raise ValueError(
                "Station IATA Code should only contain 3 alphabetical characters."
            )
        return value.upper()

    # A/C Type Validations
    @field_validator("actype")
    @classmethod
    def is_actype_valid(cls, value: str):
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
