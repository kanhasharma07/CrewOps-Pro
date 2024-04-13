from models.ame_crew_model import AMECrewModel
from backend.connection import connection, db


class AMECrew:
    """
    AMECrew class represents a class for managing AME Crew members.

    Methods:
        addCrew(crewData: list) -> None:
            Adds a new crew member to the database.
            Parameters:
                crewData (list): A list containing the crew member's data in the following order: [sap, name, fleet_cert, pw].
        
        deleteCrew(sap: int) -> None:
            Deletes a crew member from the database.
            Parameters:
                sap (int): The SAP (Staff ID) of the crew member to be deleted.
        
        viewCrew() -> List[Tuple]:
            Retrieves all crew members from the database.
            Returns:
                List[Tuple]: A list of tuples, where each tuple represents a crew member's data.
        
        modifyCrew(newData: list, sap: int) -> None:
            Modifies the data of a crew member in the database.
            Parameters:
                newData (list): A list containing the updated data of the crew member in the following order: [sap, name, fleet_cert, pw].
                sap (int): The SAP (Staff ID) of the crew member to be modified.
    """
    tablename = "ame_crew"

    @staticmethod
    def addCrew(crewData: list):
        ame = AMECrewModel(
            sap=crewData[0],
            name=crewData[1],
            fleet_cert=crewData[2],
            pw=crewData[3],
            login=None,
        )

        query = f"INSERT INTO {AMECrew.tablename} (staffid, name, fleet_certified, login, pw) VALUES (%s,%s,%s,%s,%s)"
        values = tuple(ame.model_dump().values())
        db.execute(query, values)
        connection.commit()

    @staticmethod
    def deleteCrew(sap):
        db.execute(f"DELETE FROM {AMECrew.tablename} WHERE staffid={sap}")
        connection.commit()

    @staticmethod
    def viewCrew():
        query = f"SELECT * FROM {AMECrew.tablename}"
        db.execute(query)
        return db.fetchall()

    @staticmethod
    def modifyCrew(newData: list, sap: int):
        query = f"SELECT * FROM {AMECrew.tablename} WHERE staffid={sap}"
        db.execute(query)
        oldData = db.fetchone()
        newData = [val2 if val2 != "" else val1 for val1, val2 in zip(oldData, newData)]  # type: ignore
        modelDict = dict(zip(AMECrewModel.__annotations__.keys(), newData))
        ame = AMECrewModel.model_validate(modelDict)
        db.execute(f"DELETE FROM {AMECrew.tablename} WHERE staffid={sap}")
        queryNew = f"INSERT INTO {AMECrew.tablename} (staffid, name, fleet_certified, login, pw) VALUES (%s,%s,%s,%s,%s)"
        data = tuple(ame.model_dump().values())
        db.execute(queryNew, data)
        connection.commit()

