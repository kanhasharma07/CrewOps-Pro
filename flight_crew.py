import enum
from backend.connection import db, connection
from models.flight_crew_model import FlightCrewModel


class FlightCrew:
    """
    FlightCrew class represents a utility class for managing flight crew members.

    Methods:
        addCrew(sap, fname, lname, desig, mob, atpl, license, medical, baseops, avail, pw, login=None) -> None:
            Adds a new flight crew member to the database.

        deleteCrew(sap) -> None:
            Deletes a flight crew member from the database.

        viewCrew() -> List[List[Union[int, str, bool]]]:
            Retrieves a list of flight crew members from the database.

        modifyCrew(sap: int, formData: List[str]) -> None:
            Modifies the details of a flight crew member in the database.

        updateAvail(sap: int, availBool: bool) -> None:
            Updates the availability status of a flight crew member in the database.

        isAvailable(sap: int) -> None:
            Sets the availability status of a flight crew member to True in the database.

        isCrewed(sap: int) -> None:
            Sets the availability status of a flight crew member to False in the database.

        objectify(crew: List[List[Union[int, str, bool]]]) -> List[FlightCrewModel]:
            Converts a list of flight crew member data into a list of FlightCrewModel instances.

        availableP1() -> List[FlightCrewModel]:
            Retrieves a list of available P1 flight crew members from the database.

        availableP2() -> List[FlightCrewModel]:
            Retrieves a list of available P2 flight crew members from the database.

        find_suitable_P1(availP1: List[FlightCrewModel], dutyTimeP1: Dict[int, int]) -> FlightCrewModel:
            Finds the next available P1 flight crew member whose duty time has not exceeded 8 hours.

        find_suitable_P2(availP2: List[FlightCrewModel], dutyTimeP2: Dict[int, int]) -> FlightCrewModel:
            Finds the next available P2 flight crew member whose duty time has not exceeded 8 hours.
    """

    tablename = "flight_crew"

    @staticmethod
    def addCrew(
        sap,
        fname,
        lname,
        desig,
        mob,
        atpl,
        license,
        medical,
        baseops,
        avail,
        pw,
        login=None,
    ) -> None:
        # Creating operational Flight Crew Instance
        pilot = FlightCrewModel(
            sap=sap,
            fname=fname,
            lname=lname,
            desig=desig,
            mob=mob,
            atpl_holder=atpl,
            licence=license,
            medical_validity=medical,
            base_ops=baseops,
            availability=avail,
            login=login,
            pw=pw,
        )

        query = f"""INSERT INTO {FlightCrew.tablename}
        (staffid, fname, lname, designation, contact, atpl, license_no, medical_validity, base_ops, availability, login, pw)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        data = tuple(pilot.model_dump().values())
        db.execute(query, data)
        connection.commit()

    @staticmethod
    def deleteCrew(sap) -> None:
        db.execute(f"DELETE FROM {FlightCrew.tablename} WHERE staffid={sap}")
        connection.commit()

    @staticmethod
    def viewCrew() -> list:
        query = f"SELECT * FROM {FlightCrew.tablename}"
        db.execute(query)
        crewViewList = db.fetchall()

        def replaceNonBoolean(seq):
            modifiedList = [list(item) for item in seq]
            for i, val in enumerate(modifiedList):
                modifiedList[i][5] = False if val[5] == 0 else True
                modifiedList[i][9] = False if val[9] == 0 else True
            return modifiedList

        return replaceNonBoolean(crewViewList)

    @staticmethod
    def modifyCrew(sap: int, formData: list) -> None:
        query = f"SELECT * FROM {FlightCrew.tablename} WHERE staffid={sap}"
        db.execute(query)
        oldData = db.fetchone()
        newData = [val2 if val2 != "" else val1 for val1, val2 in zip(oldData, formData)]  # type: ignore
        modelDict = dict(zip(list(FlightCrewModel.__annotations__.keys()), newData))
        pilot = FlightCrewModel.model_validate(modelDict)
        db.execute(f"DELETE FROM {FlightCrew.tablename} WHERE staffid={sap}")
        newQuery = f"""INSERT INTO {FlightCrew.tablename}
        (staffid, fname, lname, designation, contact, atpl, license_no, medical_validity, base_ops, availability, login, pw)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        data = tuple(pilot.model_dump().values())
        db.execute(newQuery, data)
        connection.commit()

    @staticmethod
    def updateAvail(sap: int, availBool) -> None:
        query = f"UPDATE {FlightCrew.tablename} SET availability={availBool} WHERE staffid={sap}"
        db.execute(query)
        connection.commit()

    @staticmethod
    def isAvailabie(sap: int) -> None:
        """
        Updates the availability status of a flight crew member in the database.

        Parameters:
            sap (int): The staff ID of the flight crew member.

        Returns:
            None

        Raises:
            None
        """
        query = (
            f"UPDATE {FlightCrew.tablename} SET availability=True WHERE staffid={sap}"
        )
        db.execute(query)
        connection.commit()

    @staticmethod
    def isCrewed(sap: int) -> None:
        """
        Updates the availability status of a flight crew member to false in the database.

        Parameters:
            sap (int): The staff ID of the flight crew member.

        Returns:
            None

        Raises:
            None
        """
        query = (
            f"UPDATE {FlightCrew.tablename} SET availability=False WHERE staffid={sap}"
        )
        db.execute(query)
        connection.commit()

    # Returns a list of FlightCrewModel instances from an input of db.fetchall()
    @staticmethod
    def objectify(crew: list) -> list[FlightCrewModel]:
        """
        Converts a list of flight crew member data into a list of FlightCrewModel instances.

        Parameters:
            crew (list): A list of flight crew member data.

        Returns:
            list[FlightCrewModel]: A list of FlightCrewModel instances.

        Raises:
            None
        """
        return [
            FlightCrewModel.model_validate(
                dict(zip(FlightCrewModel.__annotations__, crewman))
            )
            for crewman in crew
        ]

    # Returns a list[FlightCrewModel] of Available P1
    @staticmethod
    def availableP1() -> list[FlightCrewModel]:
        """
        Retrieves a list of available P1 flight crew members from the database.

        Returns:
            list[FlightCrewModel]: A list of FlightCrewModel instances representing the available P1 flight crew members.

        Raises:
            None
        """
        query = f"SELECT * FROM {FlightCrew.tablename} WHERE designation IN ('Commander','Sr Commander','LTC', 'TRI','DE') AND availability=1"
        db.execute(query)
        crew = db.fetchall()
        return [
            FlightCrewModel.model_validate(
                dict(zip(FlightCrewModel.__annotations__, crewman))
            )
            for crewman in crew
        ]

    # Returns a list[FlightCrewModel] of Available P2
    @staticmethod
    def availableP2() -> list[FlightCrewModel]:
        """
        Retrieves a list of available P2 flight crew members from the database.

        Returns:
            list[FlightCrewModel]: A list of FlightCrewModel instances representing the available P2 flight crew members.

        Raises:
            None
        """
        query = f"SELECT * FROM {FlightCrew.tablename} WHERE designation IN ('JFO','FO','SFO') AND availability=1"
        db.execute(query)
        crew = db.fetchall()
        return [
            FlightCrewModel.model_validate(
                dict(zip(FlightCrewModel.__annotations__, crewman))
            )
            for crewman in crew
        ]

    @staticmethod
    # Returns the list of next available P1 whose Duty Time has not exceeded 8 hrs
    def find_suitable_P1(
        availP1: list[FlightCrewModel], dutyTimeP1: dict
    ) -> FlightCrewModel:
        """
        Returns the next available P1 flight crew member whose duty time has not exceeded 8 hours.

        Parameters:
            availP1 (list[FlightCrewModel]): A list of available P1 flight crew members.
            dutyTimeP1 (dict): A dictionary mapping SAP (Staff ID) to duty time in hours.

        Returns:
            FlightCrewModel: The next available P1 flight crew member whose duty time has not exceeded 8 hours.

        Raises:
            None
        """
        while dutyTimeP1[availP1[0].sap] >= 8:
            availP1.pop(0)
        return availP1[0]

    @staticmethod
    # Returns the list of next available P2 whose Duty Time has not exceeded 8 hrs
    def find_suitable_P2(
        availP2: list[FlightCrewModel], dutyTimeP2: dict
    ) -> FlightCrewModel:
        """
        Returns the next available P2 flight crew member whose duty time has not exceeded 8 hours.

        Parameters:
            availP2 (list[FlightCrewModel]): A list of available P2 flight crew members.
            dutyTimeP2 (dict): A dictionary mapping SAP (Staff ID) to duty time in hours.

        Returns:
            FlightCrewModel: The next available P2 flight crew member whose duty time has not exceeded 8 hours.

        Raises:
            None
        """
        while dutyTimeP2[availP2[0].sap] >= 8:
            availP2.pop(0)
        return availP2[0]
