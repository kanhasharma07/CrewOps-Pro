from datetime import date
from backend.connection import db, connection
from models.flight_crew_model import FlightCrewModel


class FlightCrew:
    
    @staticmethod
    def addFlightCrew(sap, fname, lname, desig, mob, atpl, license, medical, baseops, avail, pw, login = None):
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
        
        query = f"""INSERT INTO flight_crew
        (staffid, fname, lname, designation, contact, atpl, license_no, medical_validity, base_ops, availability, login, pw)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        data= tuple(pilot.model_dump().values())
        db.execute(query, data)
        connection.commit()
        
        
        
        
        
  
  
        
# from datetime import date
# kanha = FlightCrew()
# kanha.addFlightCrew(80050318, "kanha", "sharma", "boss", 9451438366, False, 19854, date(2024, 6, 8), 'bom', True, "helloji")