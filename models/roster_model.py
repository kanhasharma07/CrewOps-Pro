from pydantic import BaseModel, field_validator
from datetime import date


class RosterModel(BaseModel):
    """
    The 'RosterModel' class represents a model for a roster entry. It inherits from the 'BaseModel' class provided by the 'pydantic' library.

    Attributes:
        flight_date (date): The date of the flight.
        flight_no (int): The flight number.
        msn (int): The MSN (Manufacturer Serial Number) of the aircraft.
        p1_id (int): The SAP (Staff ID) of the first crew member.
        p2_id (int): The SAP (Staff ID) of the second crew member.

    Validations:
        - Flight Date Validation: The 'flight_date' attribute must not be in the past.
        - Flight Number Validation: The 'flight_no' attribute must have a length of either 4 or 5.
        - MSN Validation: The 'msn' attribute must not be empty.
        - P1 SAP Validation: The 'p1_id' attribute must be exactly 8 digits long.
        - P2 SAP Validation: The 'p2_id' attribute must be exactly 8 digits long.
    """
    # Data Fields
    flight_date: date
    flight_no: int
    msn: int
    p1_id: int
    p2_id: int

    # Validations
    # Flight Date Validation
    @field_validator("flight_date")
    @classmethod
    def is_flightdate_valid(cls, value):
        today = date.today()
        if value < today:
            raise ValueError("Flight Date date cannot be in the past.")
        return value

    # Flight_no Validation
    @field_validator("flight_no")
    @classmethod
    def is_flightno_valid(cls, value):
        # Length 5 or 6 only
        if not (len(value) == 4 or len(value) == 5):
            raise ValueError("Length of Flight Number must either 4 or 5")
        return value.upper()

    # MSN Validation
    @field_validator("msn")
    @classmethod
    def is_msn_valid(cls, value):
        # Should not be Empty
        if not value:
            raise ValueError("MSN can not be empty")

        return value

    # P1 SAP Validation
    @field_validator("p1_id")
    @classmethod
    def is_p1id_valid(cls, value):
        sap_len = 8
        sap_str = str(value)
        if len(sap_str) != sap_len:
            raise ValueError(
                f"P1 SAP (Staff ID) Must be exactly {sap_len} digits long."
            )
        return value

    # P2 SAP Validation
    @field_validator("p2_id")
    @classmethod
    def is_p2id_valid(cls, value):
        sap_len = 8
        sap_str = str(value)
        if len(sap_str) != sap_len:
            raise ValueError(
                f"P2 SAP (Staff ID) Must be exactly {sap_len} digits long."
            )
        return value
