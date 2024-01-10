from pydantic import BaseModel, field_validator

class FlightCrew(BaseModel):
    
    #Data Fields
    sap: int
    fname: str
    lname: str
    desig: str
    mob: int
    atpl_holder: bool
    licence: int
    medical_validity: int
    base_ops: str
    availability: bool
    login: str
    pw: str
    
    
    #Validations
    #StaffID Validation
    @field_validator("sap")
    @classmethod
    def is_sap_valid(cls, sap_value):
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
        sap_str = str(sap_value)
        if len(sap_str) != sap_len:
            raise ValueError(f"SAP (Staff ID) Must be exactly {sap_len} digits long.")
        return sap_value
    
    
    #Mobile Number Validation
    @field_validator("mob")
    @classmethod
    def is_mob_valid(cls, mob_value):
        """
        Check if the mobile number value is valid.

        Parameters:
        - mob_value (int): The mobile number value to be validated. Auto-passed.

        Raises:
        - ValueError: If the mobile number value is not exactly 10 digits long.

        Returns:
        - int: The validated mobile number value.

        """
        mob_len = 10
        mob_str = str(mob_value)
        if len(mob_str) != mob_len:
            raise ValueError(f"Mobile number Must be exactly {mob_len} digits long.")
        return mob_value
    
    
    #First Name Validation
    @field_validator("fname")
    @classmethod
    def is_fname_valid(cls, fname_value):
        """
        Check if the first name value is valid.

        Parameters:
        - fname_value (str): The first name value to be validated. Auto-passed.

        Raises:
        - ValueError: If the first name value is empty or contains any special characters.

        Returns:
        - str: The validated first name value.

        """
        if not fname_value:
            raise ValueError("First name cannot be empty.")
        if not fname_value.isalpha():
            raise ValueError("First name should only contain alphabetic characters.")
        return fname_value.title()
    #Last Name Validation
    @field_validator("lname")
    @classmethod
    def is_lname_valid(cls, lname_value):
        """
        Check if the last name value is valid.

        Parameters:
        - lname_value (str): The last name value to be validated. Auto-passed.

        Raises:
        - ValueError: If the last name value is empty or contains any special characters.

        Returns:
        - str: The validated last name value.

        """
        if not lname_value:
            raise ValueError("Last name cannot be empty.")
        if not lname_value.isalpha():
            raise ValueError("Last name should only contain alphabetic characters.")
        return lname_value.title()
    
    #continue validations