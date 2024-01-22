from backend.connection import db, connection
from models.flight_crew_model import FlightCrewModel


class FlightCrew:
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
    ):
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
    def deleteCrew(sap):
        db.execute(f"DELETE FROM {FlightCrew.tablename} WHERE staffid={sap}")
        connection.commit()

    @staticmethod
    def viewCrew():
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
    def modifyCrew(sap: int, formData: list):
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
    def updateAvail(sap: int, availBool):
        query = f"UPDATE {FlightCrew.tablename} SET availability={availBool} WHERE staffid={sap}"
        db.execute(query)
        connection.commit()


# if __name__ == "__main__":
# FlightCrew.modifyCrew(80050318)
