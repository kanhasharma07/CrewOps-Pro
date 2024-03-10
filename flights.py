from models.aircraft_model import AircraftModel
from models.flights_model import FlightModel
from backend.connection import db, connection
from datetime import time


class Flight:
    tablename = "flights"

    @staticmethod
    def addFlight(flightData: list):
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
    def viewFlights():
        query = f"SELECT * FROM {Flight.tablename}"
        db.execute(query)
        return db.fetchall()

    @staticmethod
    def deleteFlight(flight_no: int):
        query = f"DELETE FROM {Flight.tablename} WHERE flight_no={flight_no}"
        db.execute(query)
        connection.commit()

    # Returns list[FlightModel] from DB
    @staticmethod
    def allFlights():
        query = f"SELECT * FROM {Flight.tablename}"
        db.execute(query)
        flights = db.fetchall()
        return [
            FlightModel.model_validate(dict(zip(FlightModel.__annotations__, flt)))
            for flt in flights
        ]
