from pydantic import BaseModel, field_validator
from datetime import date


class TrainingModel(BaseModel):
    """
    The 'TrainingModel' class represents a model for training data. It inherits from the 'BaseModel' class provided by the 'pydantic' library.

    Attributes:
        training_id (int): The ID of the training.
        training_name (str): The name of the training.
        training_desc (str): The description of the training.
        trainer_id (int): The ID of the trainer.
        trainee_id (int): The ID of the trainee.
        training_date (date): The date of the training.
        location (str): The location of the training.
        duration (str): The duration of the training.

    Validations:
        - Trainer ID Validation: This validation ensures that the trainer ID is exactly 8 digits long.
        - Trainee ID Validation: This validation ensures that the trainee ID is exactly 8 digits long.
        - Training Date Validation: This validation ensures that the training date is not in the past.
        - DEP Validations: This validation ensures that the location (station IATA code) is not empty and consists of 3 alphabetical characters.

    Note: The validations are implemented as class methods using the 'field_validator' decorator provided by the 'pydantic' library.
    """
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
        sap_len = 8
        sap_str = str(value)
        if len(sap_str) != sap_len:
            raise ValueError(
                f"Trainer SAP (Staff ID) Must be exactly {sap_len} digits long."
            )
        return value

    # Trainee ID Validation
    @field_validator("trainee_id")
    @classmethod
    def is_trainee_valid(cls, value):
        sap_len = 8
        sap_str = str(value)
        if len(sap_str) != sap_len:
            raise ValueError(
                f"Trainee SAP (Staff ID) Must be exactly {sap_len} digits long."
            )
        return value

    # Training Date Validation
    @field_validator("training_date")
    @classmethod
    def is_trainingdate_valid(cls, value):
        today = date.today()
        if value < today:
            raise ValueError("Training Date date cannot be in the past.")
        return value

    # DEP Validations
    @field_validator("location")
    @classmethod
    def is_iata_valid(cls, value):
        if not value:
            raise ValueError("Station IATA Code cannot be empty.")
        if not value.isalpha() or len(value) != 3:
            raise ValueError(
                "Station IATA Code should only contain 3 alphabetical characters."
            )
        return value.upper()
