from typing import Any
from pydantic import BaseModel, field_validator


class AMECrewModel(BaseModel):
    """
    AMECrewModel class represents a model for AME Crew members.

    Attributes:
        sap (int): The SAP (Staff ID) of the crew member.
        name (str): The name of the crew member.
        fleet_cert (str): The fleet certification of the crew member.
        login (str, optional): The login of the crew member. Defaults to None.
        pw (str): The password of the crew member.

    Methods:
        model_post_init(__context: Any) -> None:
            Initializes the login attribute to the SAP value if it is None.

        is_sap_valid(value) -> int:
            Validates the SAP (Staff ID) value.
            Raises a ValueError if the SAP value is not exactly 8 digits long.
            Returns the validated SAP value.

        is_name_valid(value) -> str:
            Validates the name value.
            Raises a ValueError if the name value is empty, contains special characters, or exceeds 255 characters.
            Returns the validated name value.

        is_fleet_valid(value) -> str:
            Validates the fleet certification value.
            Raises a ValueError if the fleet certification value is empty, contains non-alphanumeric characters, or is not exactly 4 characters long.
            Returns the validated fleet certification value.

        is_pw_valid(value) -> str:
            Validates the password value.
            Raises a ValueError if the password value is empty or exceeds 20 characters.
            Returns the validated password value.
    """

    # Data Fields
    sap: int
    name: str
    fleet_cert: str
    login: str | None = None
    pw: str

    # INIT to set Login = SAP
    def model_post_init(self, __context: Any) -> None:
        if self.login is None:
            self.login = str(self.sap)
        return super().model_post_init(__context)

    # Validations
    # SAP Validation
    @field_validator("sap")
    @classmethod
    def is_sap_valid(cls, value):
        sap_len = 8
        sap_str = str(value)
        if len(sap_str) != sap_len:
            raise ValueError(f"SAP (Staff ID) Must be exactly {sap_len} digits long.")
        return value

    # Name Validation
    @field_validator("name")
    @classmethod
    def is_name_valid(cls, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        if not value.replace(" ", "").isalpha():
            raise ValueError(
                "Name should only contain alphabetic characters and spaces."
            )
        if len(value) > 255:
            raise ValueError("Name length should not exceed 255 characters.")
        return value.title()

    # Fleet Certified Validation
    @field_validator("fleet_cert")
    @classmethod
    def is_fleet_valid(cls, value):
        if not value:
            raise ValueError("Fleet cannot be empty.")
        if not value.isalnum():
            raise ValueError("Fleet must only contain 4 Alphanumeric Charaters")
        if len(value) != 4:
            raise ValueError("Provide a valid 4 character Fleet Certification")
        return value.title()

    # Password Validation
    @field_validator("pw")
    @classmethod
    def is_pw_valid(cls, value):
        if not value:
            raise ValueError("Password cannot be empty.")
        if len(value) > 20:
            raise ValueError("Password length should not exceed 20 characters.")
        return value
