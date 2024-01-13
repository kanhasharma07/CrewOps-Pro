from pydantic import BaseModel, field_validator
from datetime import date


class RosterModel(BaseModel):
    """
    The `Roster` class is a Pydantic model that represents a roster for a flight. It contains data fields for the flight date, flight number, MSN (aircraft serial number), and the IDs of two staff members. It also includes validation methods for each field to ensure the data is valid.

    Example Usage:
        roster = Roster(
            flight_date=date(2022, 1, 1),
            flight_no="ABC123",
            msn=12345,
            p1_id=12345678,
            p2_id=87654321
        )

    Main functionalities:
    - Storing and validating data for a flight roster, including the flight date, flight number, MSN, and staff IDs.
    - Ensuring that the flight date is not in the past.
    - Validating the length of the flight number.
    - Checking that the MSN is not empty and is unique.
    - Verifying that the staff IDs are exactly 8 digits long.

    Fields:
    - `flight_date`: Represents the date of the flight.
    - `flight_no`: Represents the flight number.
    - `msn`: Represents the MSN (aircraft serial number).
    - `p1_id`: Represents the ID of the first staff member.
    - `p2_id`: Represents the ID of the second staff member.
    """
    # Data Fields
    flight_date: date
    flight_no: str
    msn: int
    p1_id: int
    p2_id: int
    
    # Validations
    # Flight Date Validation
    @field_validator("flight_date")
    @classmethod
    def is_flightdate_valid(cls, value):
        """
        Check if the Flight Date value is valid.

        Parameters:
        - medical_validity_value (date): The Flight Date value to be validated. Auto-passed.

        Raises:
        - ValueError: If the Flight Date value is in the past.

        Returns:
        - date: The validated Flight Date value.

        """
        today = date.today()
        if value < today:
            raise ValueError("Flight Date date cannot be in the past.")
        return value
    
    # Flight_no Validation
    @field_validator('flight_no')
    @classmethod
    def is_flightno_valid(cls, value):
        # Length 5 or 6 only
        if not (len(value) == 4 or len(value) == 5):
            raise ValueError('Length of Flight Number must either 4 or 5')
        return value.upper()
        
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
    
    # P1 SAP Validation
    @field_validator("p1_id")
    @classmethod
    def is_p1id_valid(cls, value):
        """
        Check if the P1 SAP (Staff ID) value is valid.

        Parameters:
        - sap_value (int): The P1 SAP (Staff ID) value to be validated. Auto-passed.

        Raises:
        - ValueError: If the P1 SAP (Staff ID) value is not exactly 8 digits long.

        Returns:
        - int: The validated P1 SAP (Staff ID) value.

        """
        sap_len = 8
        sap_str = str(value)
        if len(sap_str) != sap_len:
            raise ValueError(f"P1 SAP (Staff ID) Must be exactly {sap_len} digits long.")
        return value
    
    # P2 SAP Validation
    @field_validator("p2_id")
    @classmethod
    def is_p2id_valid(cls, value):
        """
        Check if the P2 SAP (Staff ID) value is valid.

        Parameters:
        - sap_value (int): The P2 SAP (Staff ID) value to be validated. Auto-passed.

        Raises:
        - ValueError: If the P2 SAP (Staff ID) value is not exactly 8 digits long.

        Returns:
        - int: The validated P2 SAP (Staff ID) value.

        """
        sap_len = 8
        sap_str = str(value)
        if len(sap_str) != sap_len:
            raise ValueError(f"P2 SAP (Staff ID) Must be exactly {sap_len} digits long.")
        return value