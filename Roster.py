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