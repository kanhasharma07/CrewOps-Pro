from backend.connection import db, connection
from models.aircraft_model import AircraftModel


class Aircraft:
    """
    The Aircraft class represents a collection of methods for managing aircraft data in the database.

    Attributes:
    - tablename (str): The name of the table in the database where aircraft data is stored.

    Methods:
    - addAircraft(acdata: list): Adds a new aircraft to the database.
    - viewAircraft(): Retrieves all aircraft data from the database.
    - deleteAircraft(msn: int): Deletes an aircraft from the database based on its MSN (unique identification number).
    - modifyAircraft(newData: list, msn: int): Modifies an existing aircraft in the database based on its MSN.
    - objectify(fleetList: list): Converts a list of aircraft data retrieved from the database into a list of AircraftModel objects.
    - avaiableFleet(actype: str) -> list[AircraftModel]: Retrieves a list of available aircraft of a specific type from the database.

    Note:
    - The addAircraft method expects a list of aircraft data in the following order: MSN, A/C Type, Registration, Availability, Engine, Engine Hours.
    - The viewAircraft method returns a list of all aircraft data in the database.
    - The deleteAircraft method deletes an aircraft from the database based on its MSN.
    - The modifyAircraft method modifies an existing aircraft in the database based on its MSN. It expects a list of new data for the aircraft and the MSN of the aircraft to be modified.
    - The objectify method converts a list of aircraft data retrieved from the database into a list of AircraftModel objects.
    - The avaiableFleet method retrieves a list of available aircraft of a specific type from the database.
    """
    
    tablename = "aircraft_fleet"

    @staticmethod
    def addAircraft(acdata: list) -> None:
        """
        Adds a new aircraft to the database.

        Parameters:
        - acdata (list): A list of aircraft data in the following order: MSN, A/C Type, Registration, Availability, Engine, Engine Hours.

        Returns:
        None

        Note:
        - The method validates the length and types of the `acdata` list before accessing its attributes.
        - The method creates an instance of the AircraftModel class using the validated aircraft data.
        - The method then executes an SQL query to insert the aircraft data into the database.
        - The method commits the changes to the database.

        Example:
        addAircraft([123, 'Boeing', 'ABC123', True, 'CFM56', 5000])
        """
        if len(acdata) != 6 or not all(isinstance(item, (int, str, bool)) for item in acdata):
            raise ValueError("Invalid aircraft data")

        aeroplane = AircraftModel.model_validate(
            {
                "msn": acdata[0],
                "actype": acdata[1],
                "regn": acdata[2],
                "availability": acdata[3],
                "engine": acdata[4],
                "engine_hours": acdata[5],
            }
        )
        query = "INSERT INTO {tablename} (msn, type, regn, availability, engine, engine_hours) VALUES (%s,%s,%s,%s,%s,%s)".format(tablename=Aircraft.tablename)
        db.execute(query, tuple(aeroplane.model_dump().values()))
        connection.commit()

    @staticmethod
    def viewAircraft() -> list:
        """
        Retrieves all aircraft data from the database.

        Returns:
            list: A list of all aircraft data in the database.

        Note:
            - The method executes an SQL query to retrieve all aircraft data from the database.
            - The method returns the fetched data as a list.

        Example:
            viewAircraft()
        """
        query = f"SELECT * FROM {Aircraft.tablename}"
        db.execute(query)
        return db.fetchall()

    @staticmethod
    def deleteAircraft(msn: int) -> None:
        """
        Deletes an aircraft from the database based on its MSN (unique identification number).

        Parameters:
        - msn (int): The MSN of the aircraft to be deleted.

        Returns:
        None

        Note:
        - The method executes an SQL query to delete the aircraft from the database based on its MSN.
        - The method commits the changes to the database.
        """
        query = f"DELETE FROM {Aircraft.tablename} WHERE msn={msn}"
        db.execute(query)
        connection.commit()

    @staticmethod
    def modifyAircraft(newData: list, msn: int) -> None:
        """
        Modifies an existing aircraft in the database based on its MSN.

        Parameters:
        - newData (list): A list of new data for the aircraft.
        - msn (int): The MSN of the aircraft to be modified.

        Returns:
        None

        Note:
        - The method retrieves the old data of the aircraft from the database based on its MSN.
        - The method modifies the new data by replacing empty values with the corresponding old values.
        - The method deletes the old aircraft from the database.
        - The method adds the modified aircraft with the new data to the database.

        Example:
        modifyAircraft(['', 'Boeing 747', 'DEF456', True, 'CFM56', 6000], 123)
        """
        query = f"SELECT * FROM {Aircraft.tablename} WHERE msn={msn}"
        db.execute(query)
        oldData = db.fetchone()
        print(oldData)
        newData = [val2 if val2 != "" else val1 for val1, val2 in zip(oldData, newData)]  # type: ignore
        print("NewDataModified= ", newData)
        Aircraft.deleteAircraft(msn)
        Aircraft.addAircraft(newData)

    # Returns a list[AircraftModel] when provided input of a db.fetchall() list
    @staticmethod
    def objectify(fleetList: list) -> list[AircraftModel]:
        """
        Converts a list of aircraft data retrieved from the database into a list of AircraftModel objects.

        Parameters:
        - fleetList (list): A list of aircraft data retrieved from the database.

        Returns:
        - list[AircraftModel]: A list of AircraftModel objects.

        Note:
        - The method iterates over each aircraft in the fleetList.
        - For each aircraft, it creates a dictionary by zipping the AircraftModel attribute names with the corresponding values from the aircraft data.
        - It then calls the model_validate method of the AircraftModel class, passing the created dictionary as an argument.
        - The model_validate method validates the attributes of the AircraftModel object and returns the validated object.
        - The method collects all the validated AircraftModel objects in a list and returns it.

        Example:
        objectify([
            [123, 'Boeing', 'ABC123', True, 'CFM56', 5000],
            [456, 'Airbus', 'DEF456', False, 'PW1100G', 3000]
        ])
        """
        return [
            AircraftModel.model_validate(
                dict(zip(AircraftModel.__annotations__, aircraft))
            )
            for aircraft in fleetList
        ]

    # Returns list[AircraftModel] of available aircraft.
    @staticmethod
    def avaiableFleet(actype: str) -> list[AircraftModel]:
        """
        Retrieves a list of available aircraft of a specific type from the database.

        Parameters:
        - actype (str): The type of aircraft to retrieve.

        Returns:
        - list[AircraftModel]: A list of AircraftModel objects representing the available aircraft of the specified type.

        Note:
        - The method executes an SQL query to retrieve all available aircraft of the specified type from the database.
        - The method returns the fetched data as a list of AircraftModel objects.
        - The availability of an aircraft is determined by the 'availability' attribute in the database, where 1 represents available and 0 represents unavailable.
        - The method uses the 'model_validate' method of the AircraftModel class to validate and create the AircraftModel objects.
        - The method zips the attribute names of the AircraftModel class with the corresponding values from the fetched data to create a dictionary.
        - The 'model_validate' method validates the attributes of the AircraftModel object and returns the validated object.
        - The method collects all the validated AircraftModel objects in a list and returns it.

        Example:
        avaiableFleet('A350')
        """
        query = f"SELECT * FROM aircraft_fleet WHERE availability=1 AND type='{actype}'"
        db.execute(query)
        availFleet = db.fetchall()
        return [
            AircraftModel.model_validate(
                dict(zip(AircraftModel.__annotations__, aircraft))
            )
            for aircraft in availFleet
        ]
