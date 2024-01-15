from datetime import date
from backend.connection import db, connection
from models.flight_crew_model import FlightCrewModel


class FlightCrew:
    
    @staticmethod
    def addCrew(sap, fname, lname, desig, mob, atpl, license, medical, baseops, avail, pw, login = None):
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
            pw=pw)
        
        table_name = 'flight_crew'
        query = f"""INSERT INTO {table_name}
        (staffid, fname, lname, designation, contact, atpl, license_no, medical_validity, base_ops, availability, login, pw)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        data= tuple(pilot.model_dump().values())
        db.execute(query, data)
        connection.commit()
    
    @staticmethod    
    def deleteCrew(sap):
        db.execute(f"DELETE FROM flight_crew WHERE staffid = {sap}")
        connection.commit()
        
    
        
        
        
  
  
        
# from datetime import date
# kanha = FlightCrew()
# kanha.addFlightCrew(80050318, "kanha", "sharma", "boss", 9451438366, False, 19854, date(2024, 6, 8), 'bom', True, "helloji")