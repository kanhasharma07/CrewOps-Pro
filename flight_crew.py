import enum
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

    @staticmethod
    def isAvailabie(sap: int):
        query = f"UPDATE {FlightCrew.tablename} SET availability=True WHERE staffid={sap}"
        db.execute(query)
        connection.commit()
    
    @staticmethod
    def isCrewed(sap: int):
        query = f"UPDATE {FlightCrew.tablename} SET availability=False WHERE staffid={sap}"
        db.execute(query)
        connection.commit()
    
    # Returns a list of FlightCrewModel instances from an input of db.fetchall()
    @staticmethod
    def objectify(crew: list) -> list[FlightCrewModel]:
        return [
            FlightCrewModel.model_validate(
                dict(zip(FlightCrewModel.__annotations__, crewman))
            )
            for crewman in crew
        ]

    # Returns a list[FlightCrewModel] of Available P1
    @staticmethod
    def availableP1() -> list[FlightCrewModel]:
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
    def find_suitable_P1(availP1: list, dutyTimeP1: dict):
        while dutyTimeP1[availP1[0].sap]>=8:
            availP1.pop(0)
        return availP1[0]
        
    @staticmethod
    # Returns the list of next available P2 whose Duty Time has not exceeded 8 hrs
    def find_suitable_P2(availP2: list, dutyTimeP2: dict):
        while dutyTimeP2[availP2[0].sap]>=8:
            availP2.pop(0)
        return availP2[0]

# if __name__ == "__main__":

