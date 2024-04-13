from datetime import date
from flight_crew import FlightCrew
from aircraft import Aircraft
from flights import Flight
from backend.connection import db, connection
from models.roster_model import RosterModel


class Roster:
    """
    The 'Roster' class represents a utility class for managing flight crew pairings in a monthly roster.

    Attributes:
        tablename (str): The name of the table in the database where the monthly roster data is stored.

    Methods:
        addPairing(pairing: list) -> None:
            Adds a new pairing to the monthly roster in the database.

        deletePairing(flight_no, p1_id: int = False, p2_id: int = False) -> None:
            Deletes a pairing from the monthly roster in the database.

        updatePairing(oldPairing: list, newPairing: list) -> None:
            Updates a pairing in the monthly roster in the database.

        new_monthly_roster(month: int) -> list:
            Generates a new monthly roster for the specified month.

        addRoster(month: int) -> None:
            Adds the generated monthly roster to the database.

        viewYourRoster(sap: int) -> list:
            Retrieves the monthly roster data for a specific flight crew member.
    """

    tablename = "monthly_roster"

    @staticmethod
    def addPairing(pairing: list) -> None:
        """
        Adds a new pairing to the monthly roster in the database.

        Parameters:
            pairing (list): A list containing the following elements in order:
                - flight_date (date): The date of the flight.
                - flight_no (int): The flight number.
                - msn (int): The MSN (Manufacturer Serial Number) of the aircraft.
                - p1_id (int): The SAP (Staff ID) of the first crew member.
                - p2_id (int): The SAP (Staff ID) of the second crew member.

        Returns:
            None

        Raises:
            None

        Example:
            addPairing([date(2022, 1, 1), 123, 56789, 12345678, 87654321])
        """
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
    def deletePairing(flight_no, p1_id: int = False, p2_id: int = False) -> None:
        queryDel = f"DELETE FROM {Roster.tablename} WHERE p1_id={p1_id} AND p2_id={p2_id} AND flight_no={flight_no}"
        db.execute(queryDel)
        connection.commit()

    @staticmethod
    def updatePairing(oldPairing: list, newPairing: list) -> None:
        Roster.deletePairing(oldPairing[1], oldPairing[4], oldPairing[5])
        Roster.addPairing(newPairing)

    @staticmethod
    def new_monthly_roster(month: int) -> list:
        """
        Generates a new monthly roster for the specified month.

        Parameters:
            month (int): The month for which the roster is generated.

        Returns:
            list: A list of crew pairings for each day of the month. Each pairing is represented as a tuple with the following elements in order:
                - flight_date (date): The date of the flight.
                - flight_no (int): The flight number.
                - aircraft (Aircraft): The aircraft assigned to the flight.
                - p1 (FlightCrewModel): The first crew member assigned to the flight.
                - p2 (FlightCrewModel): The second crew member assigned to the flight.

        Logic Flow:
        1. Create a dictionary 'days_in_months' that stores the number of days in each month.
        2. Initialize an empty list 'pairs' to store the crew pairings.
        3. Retrieve a list of all available P1 crew members using the 'availableP1' method of the 'FlightCrew' class.
        4. Retrieve a list of all available P2 crew members using the 'availableP2' method of the 'FlightCrew' class.
        5. Retrieve a list of all flights from the database using the 'allFlights' method of the 'Flight' class.
        6. Create two dictionaries 'dutyTimeP1' and 'dutyTimeP2' to store the duty time of each crew member. Initialize the duty time of all crew members to 0.
        7. Iterate over the range of days in the specified month.
        8. Iterate over each flight in the list of flights.
        9. Check if the list of available P1 crew members is empty. If it is, retrieve a new list of available P1 crew members.
        10. Check if the list of available P2 crew members is empty. If it is, retrieve a new list of available P2 crew members.
        11. Retrieve a list of available aircraft of the required type for the current flight using the 'availableFleet' method of the 'Aircraft' class.
        12. Create a pairing for the current flight by assigning the flight date, flight number, aircraft, and suitable P1 and P2 crew members.
        13. Remove the assigned P1 and P2 crew members from the lists of available crew members.
        14. Append the pairing to the 'pairs' list.
        15. Return the 'pairs' list containing all the crew pairings for each day of the month.
        """
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
        }  # Dict stores no. of days in each month. Used to create only required no. of pairings

        pairs = []  # Empty list to fill Crew Pairings

        availP1 = (
            FlightCrew.availableP1()
        )  # Returns a list[FlightCrewModel] of all available P1
        availP2 = (
            FlightCrew.availableP2()
        )  # Returns a list[FlightCrewModel] of all available P2
        flights = Flight.allFlights()  # Returns a list[Flight] of all flights in the DB

        dutyTimeP1 = {P1.sap: 0 for P1 in availP1}  # Set duty time 0 of all Crew
        dutyTimeP2 = {
            P2.sap: 0 for P2 in availP2
        }  # at the start of a monthly roster cycle

        for day in range(1, days_in_months[month]):
            for flight in flights:

                # Resets all P1 as available when list of availP1 has been exhausted
                if not availP1:
                    availP1 = FlightCrew.availableP1()

                # Resets all P2 as available when list of availP1 has been exhausted
                if not availP2:
                    availP2 = FlightCrew.availableP2()

                # Returns list of available aircraft of the required type for each flight in loop
                availFleet = Aircraft.avaiableFleet(flight.actype)

                # Create pairing for current flight in loop
                flt_date = date(year=2024, month=month, day=day)
                currentFlightNo = flight.flight_no
                aircraft = availFleet.pop(0)
                p1 = FlightCrew.find_suitable_P1(availP1, dutyTimeP1)
                p2 = FlightCrew.find_suitable_P2(availP2, dutyTimeP2)

                # Delete assigned P1 P2 from available crew lists
                availP1.pop(0)
                availP2.pop(0)

                pairs.append((flt_date, currentFlightNo, aircraft, p1, p2))
        return pairs

    @staticmethod
    def addRoster(month: int) -> None:
        """
        Adds the generated monthly roster to the database.

        Parameters:
            month (int): The month for which the roster is generated.

        Returns:
            None

        Raises:
            None

        Example:
            addRoster(1)
        """
        db.execute(f"DELETE FROM {Roster.tablename}")
        crewPairObj = Roster.new_monthly_roster(month=month)
        crewPair = [
            (crew[0], crew[1], crew[2].msn, crew[3].sap, crew[4].sap)
            for crew in crewPairObj
        ]
        query = f"INSERT INTO {Roster.tablename} (date, flight_no, aircraft_msn, p1_id, p2_id) VALUES (%s,%s,%s,%s,%s)"
        db.executemany(query, crewPair)
        connection.commit()

    # Returns list of Roster Data, each flight as a tuple in the list
    @staticmethod
    def viewYourRoster(sap: int) -> list:
        """
        Retrieves the monthly roster data for a specific flight crew member.

        Parameters:
            sap (int): The SAP (Staff ID) of the flight crew member.

        Returns:
            list: A list of tuples representing the monthly roster data for the specified flight crew member. Each tuple contains the following elements in order:
                - date (str): The date of the flight in the format 'dd-mm-yyyy'.
                - flight_no (int): The flight number.
                - PIC (str): The name of the Pilot in Command.
                - Co-Pilot (str): The name of the Co-Pilot.
                - route (str): The route of the flight in the format 'departure - arrival'.
                - timing (str): The timing of the flight in the format 'departure time - arrival time'.
                - regn (str): The registration number of the aircraft in the format 'VT-<registration number>'.

        Example:
            viewYourRoster(12345678)
        """
        query = f"""SELECT
                DATE_FORMAT(monthly_roster.date, '%d-%m-%Y'),
                flights.flight_no,
                CONCAT("Capt ", fc1.fname, ' ', fc1.lname) AS PIC,
                CONCAT("Capt ", fc2.fname, ' ', fc2.lname) AS "Co-Pilot",
                CONCAT(flights.departure, " - ", flights.arrival) AS route,
                CONCAT(TIME_FORMAT(flights.dep_time, '%H:%i'), " - ", TIME_FORMAT(flights.arr_time, '%H:%i')) AS timing,
                CONCAT("VT-", aircraft_fleet.regn) AS regn
            FROM
                flight_crew AS fc1
                JOIN monthly_roster ON fc1.staffid = monthly_roster.p1_id
                JOIN flights ON monthly_roster.flight_no = flights.flight_no
                JOIN aircraft_fleet ON monthly_roster.aircraft_msn = aircraft_fleet.msn
                JOIN flight_crew AS fc2 ON monthly_roster.p2_id = fc2.staffid
            WHERE
                fc1.staffid = {sap}
                OR fc2.staffid = {sap};"""
        db.execute(query)
        return db.fetchall()
