from datetime import time
from pydantic import BaseModel, field_validator


class FlightModel(BaseModel):
    """
    FlightModel class represents a model for flight data.

    Attributes:
        flight_no (int): The flight number.
        dep (str): The departure station IATA code.
        arr (str): The arrival station IATA code.
        actype (str): The aircraft type.
        etd (str): The estimated time of departure.
        eta (str): The estimated time of arrival.
        duration (str): The duration of the flight.

    Validations:
        - flight_no: Validates the length of the flight number. It should be either 3 or 4 characters long.
        - dep: Validates the departure station IATA code. It should not be empty and should contain 3 alphabetical characters.
        - arr: Validates the arrival station IATA code. It should not be empty and should contain 3 alphabetical characters.
        - actype: Validates the aircraft type. It should not be empty, should contain 4 alphanumeric characters, and should be 4 characters long.

    """

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
        if not value:
            raise ValueError("A/C Type cannot be empty.")
        if not value.isalnum():
            raise ValueError("A/C Type must only contain 4 Alphanumeric Charaters")
        if len(value) != 4:
            raise ValueError("Provide a valid 4 character A/C Type Certification")
        return value.title()
