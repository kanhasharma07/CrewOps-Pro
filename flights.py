from models.flights_model import FlightModel
from backend.connection import db, connection


class Flight:
    """
    The Flight class represents a utility class for managing flight data in the database.

    Attributes:
        tablename (str): The name of the table in the database where flight data is stored.

    Methods:
        addFlight(flightData: list) -> None: Adds a new flight to the database.
        viewFlights() -> list: Retrieves all flights from the database.
        deleteFlight(flight_no: int) -> None: Deletes a flight from the database.
        allFlights() -> list[FlightModel]: Retrieves all flights from the database as a list of FlightModel objects.

    """

    tablename = "flights"

    @staticmethod
    def addFlight(flightData: list) -> None:
        flt = FlightModel(
            flight_no=flightData[0],
            dep=flightData[1],
            arr=flightData[2],
            etd=str(flightData[3][0]) + ":" + str(flightData[3][1]),
            eta=str(flightData[4][0]) + ":" + str(flightData[4][1]),
            actype=flightData[5],
            duration=str(flightData[6][0]) + ":" + str(flightData[6][1]),
        )
        query = f"INSERT INTO {Flight.tablename} (flight_no, departure, arrival, aircraft_type, dep_time, arr_time, duration) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        data = tuple(flt.model_dump().values())
        db.execute(query, data)
        connection.commit()

    @staticmethod
    def viewFlights() -> list:
        query = f"SELECT * FROM {Flight.tablename}"
        db.execute(query)
        return db.fetchall()

    @staticmethod
    def deleteFlight(flight_no: int) -> None:
        query = f"DELETE FROM {Flight.tablename} WHERE flight_no={flight_no}"
        db.execute(query)
        connection.commit()

    # Returns list[FlightModel] from DB
    @staticmethod
    def allFlights() -> list[FlightModel]:
        """
        Returns a list of FlightModel objects representing all flights in the database.

        Returns:
            list[FlightModel]: A list of FlightModel objects representing all flights in the database.

        """
        query = f"SELECT * FROM {Flight.tablename}"
        db.execute(query)
        flights = db.fetchall()
        return [
            FlightModel.model_validate(dict(zip(FlightModel.__annotations__, flt)))
            for flt in flights
        ]
