from models.ame_crew_model import AMECrewModel
from backend.connection import connection, db


class AMECrew:

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


if __name__ == "__main__":
    pass
    # AMECrew.addCrew(80050322, 'kanha sharma', 'b737', 'heeyaw')
    # AMECrew.deleteCrew(80050322)
