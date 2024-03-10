from datetime import date
from flight_crew import FlightCrew
from aircraft import Aircraft
from flights import Flight
from backend.connection import db, connection
from models.roster_model import RosterModel


class Roster:
    tablename = "monthly_roster"

    @staticmethod
    def addPairing(pairing: list):
        pair = RosterModel(
            flight_date=pairing[0],
            flight_no=pairing[1],
            msn=pairing[2],
            p1_id=pairing[3],
            p2_id=pairing[4],
        )
        query = f"INSERT INTO {Roster.tablename} (date, flight_no, aircraft_msn, p1_id, p2_id) VALUES (%s,%s,%s,%s,%s)"
        db.execute(query, tuple(pair.model_dump().values()))
        connection.commit()

    @staticmethod
    def deletePairing(flight_no, p1_id: int = False, p2_id: int = False):  # type: ignore
        queryDel = f"DELETE FROM {Roster.tablename} WHERE p1_id={p1_id} AND p2_id={p2_id} AND flight_no={flight_no}"
        db.execute(queryDel)
        connection.commit()

    @staticmethod
    def updatePairing(oldPairing: list, newPairing: list):
        Roster.deletePairing(oldPairing[1], oldPairing[4], oldPairing[5])
        Roster.addPairing(newPairing)

    @staticmethod
    def new_monthly_roster(month: int):
        days_in_months = {
            1: 31,
            2: 28,
            3: 30,
            4: 31,
            5: 30,
            6: 31,
            7: 30,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        } #Dict stores no. of days in each month. Used to create only required no. of pairings  
        
        pairs = []  # Empty list to fill Crew Pairings

        availP1 = FlightCrew.availableP1()  # Returns a list[FlightCrewModel] of all available P1
        availP2 = FlightCrew.availableP2()  # Returns a list[FlightCrewModel] of all available P2
        flights = Flight.allFlights()  # Returns a list[Flight] of all flights in the DB

        dutyTimeP1 = {P1.sap: 0 for P1 in availP1}  # Set duty time 0 of all Crew
        dutyTimeP2 = {P2.sap: 0 for P2 in availP2}  # at the start of a monthly roster cycle

        for day in range(1, days_in_months[month]):
            for flight in flights:
                                
                #Resets all P1 as available when list of availP1 has been exhausted
                if not availP1: 
                    availP1 = FlightCrew.availableP1()
                
                #Resets all P2 as available when list of availP1 has been exhausted
                if not availP2: 
                    availP2 = FlightCrew.availableP2()

                #Returns list of available aircraft of the required type for each flight in loop
                availFleet = Aircraft.avaiableFleet(flight.actype)

                #Create pairing for current flight in loop
                flt_date = date(year=2024, month=month, day=day)
                currentFlightNo = flight.flight_no
                aircraft = availFleet.pop(0)
                p1 = FlightCrew.find_suitable_P1(availP1, dutyTimeP1)
                p2 = FlightCrew.find_suitable_P2(availP2, dutyTimeP2)

                # Delete assigned P1 P2 from available crew lists
                availP1.pop(0)
                availP2.pop(0)

                pairs.append((flt_date, p1, p2, currentFlightNo, aircraft))
        return pairs

# if __name__=='__main__':