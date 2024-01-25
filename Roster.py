from datetime import date
from flight_crew import FlightCrew
from aircraft import Aircraft
from flights import Flight
from backend.connection import db, connection
from models.roster_model import RosterModel

class Roster:
    tablename = 'monthly_roster'
    @staticmethod
    def addPairing(pairing: list):
        pair = RosterModel(
            flight_date=pairing[0],
            flight_no=pairing[1],
            msn=pairing[2],
            p1_id=pairing[3],
            p2_id=pairing[4]
        )
        query = f"INSERT INTO {Roster.tablename} (date, flight_no, aircraft_msn, p1_id, p2_id) VALUES (%s,%s,%s,%s,%s)"
        db.execute(query, tuple(pair.model_dump().values()))
        connection.commit()
        
    @staticmethod
    def deletePairing(flight_no, p1_id: int = False, p2_id: int = False): # type: ignore
        queryDel = f"DELETE FROM {Roster.tablename} WHERE p1_id={p1_id} AND p2_id={p2_id} AND flight_no={flight_no}"
        db.execute(queryDel)
        connection.commit()
        
    @staticmethod
    def updatePairing(oldPairing: list, newPairing: list):
        Roster.deletePairing(oldPairing[1], oldPairing[4], oldPairing[5])
        Roster.addPairing(newPairing)
        
    @staticmethod
    def new_monthly_roster(month: int):
        pairs = []
        
        availP1 = FlightCrew.availableP1()
        availP2 = FlightCrew.availableP2()
        flights = Flight.allFlights()
        
        dutyTimeP1 = {P1.sap : 0 for P1 in availP1} 
        dutyTimeP2 = {P2.sap : 0 for P2 in availP2}
        
        for day in range(1, 32):
            for flight in flights:
                if not availP1:
                    availP1 = FlightCrew.availableP1()
                if not availP2:
                    availP2 = FlightCrew.availableP2()

                availFleet = Aircraft.avaiableFleet(flight.actype)
                
                flt_date = date(year=2024, month=month, day=day)
                currentFlightNo = flight.flight_no
                aircraft = availFleet.pop(0)
                p1 = FlightCrew.find_suitable_P1(availP1, dutyTimeP1)
                p2 = FlightCrew.find_suitable_P2(availP2, dutyTimeP2)
                
                
                availP1.pop(0)
                availP2.pop(0)
                
                pairs.append((flt_date, p1, p2, currentFlightNo, aircraft))
        return pairs   
                
                
            