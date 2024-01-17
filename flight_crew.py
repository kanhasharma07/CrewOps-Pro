from datetime import date
import json
from backend.connection import db, connection
from models.flight_crew_model import FlightCrewModel


class FlightCrew:
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

        table_name = "flight_crew"
        query = f"""INSERT INTO {table_name}
        (staffid, fname, lname, designation, contact, atpl, license_no, medical_validity, base_ops, availability, login, pw)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        data = tuple(pilot.model_dump().values())
        db.execute(query, data)
        connection.commit()

    @staticmethod
    def deleteCrew(sap):
        db.execute(f"DELETE FROM flight_crew WHERE staffid = {sap}")
        connection.commit()

    @staticmethod
    def viewCrew():
        table_name = "flight_crew"
        query = f"SELECT * FROM {table_name}"
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
    def updateAvail(sap: int, availBool):
        table_name = "flight_crew"
        query = f"UPDATE {table_name} SET availability={availBool} WHERE staffid={sap}"
        db.execute(query)
        connection.commit()


# if __name__ == "__main__":
