import time
from pydantic import BaseModel, field_validator
from datetime import date, time

class TrainingModel(BaseModel):
    
    # Data Fields
    training_id: int
    training_name: str
    training_desc: str
    trainer_id: int
    trainee_id: int
    training_date: date
    location: str
    duration: str
    
    # Validations
    # Trainer ID Validation
    @field_validator("trainer_id")
    @classmethod
    def is_trainer_valid(cls, value):
        """
        Check if the Trainer SAP (Staff ID) value is valid.

        Parameters:
        - sap_value (int): The Trainer SAP (Staff ID) value to be validated. Auto-passed.

        Raises:
        - ValueError: If the Trainer SAP (Staff ID) value is not exactly 8 digits long.

        Returns:
        - int: The validated Trainer SAP (Staff ID) value.

        """
        sap_len = 8
        sap_str = str(value)
        if len(sap_str) != sap_len:
            raise ValueError(f"Trainer SAP (Staff ID) Must be exactly {sap_len} digits long.")
        return value
    
    # Trainee ID Validation
    @field_validator("trainee_id")
    @classmethod
    def is_trainee_valid(cls, value):
        """
        Check if the Trainee SAP (Staff ID) value is valid.

        Parameters:
        - sap_value (int): The Trainee SAP (Staff ID) value to be validated. Auto-passed.

        Raises:
        - ValueError: If the Trainee SAP (Staff ID) value is not exactly 8 digits long.

        Returns:
        - int: The validated Trainee SAP (Staff ID) value.

        """
        sap_len = 8
        sap_str = str(value)
        if len(sap_str) != sap_len:
            raise ValueError(f"Trainee SAP (Staff ID) Must be exactly {sap_len} digits long.")
        return value
    
    # Training Date Validation
    @field_validator("training_date")
    @classmethod
    def is_trainingdate_valid(cls, value):
        """
        Check if the Training Date value is valid.

        Parameters:
        - value (date): The Training Date value to be validated. Auto-passed.

        Raises:
        - ValueError: If the Training Date value is in the past.

        Returns:
        - date: The validated Training Date value.

        """
        today = date.today()
        if value < today:
            raise ValueError("Training Date date cannot be in the past.")
        return value
    
    # DEP Validations
    @field_validator('location')
    @classmethod
    def is_iata_valid(cls, value):
        """
        Check if the station IATA Code Value is valid.

        Parameters:
        - value (str): The training location value to be validated. Auto-passed.

        Raises:
        - ValueError: If the IATA Code value is not exactly 3 alphabetical characters.

        Returns:
        - str: The validated base ops value.

        """
        if not value:
            raise ValueError("Station IATA Code cannot be empty.")
        if not value.isalpha() or len(value) != 3:
            raise ValueError("Station IATA Code should only contain 3 alphabetical characters.")
        return value.upper()