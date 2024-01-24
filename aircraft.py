from backend.connection import db, connection
from models.aircraft_model import AircraftModel

class Aircraft:
    tablename = 'aircraft_fleet'
    @staticmethod
    def addAircraft(acdata: list):
        aeroplane = AircraftModel(msn=acdata[0], actype=acdata[1], regn=acdata[2], availability=acdata[3],
                                  engine=acdata[4], engine_hours=acdata[5])
        query = f'INSERT INTO {Aircraft.tablename} (msn, type, regn, availability, engine, engine_hours) VALUES (%s,%s,%s,%s,%s,%s)'
        db.execute(query, tuple(aeroplane.model_dump().values()))
        connection.commit()
        
    @staticmethod
    def viewAircraft():
        query = f"SELECT * FROM {Aircraft.tablename}"
        db.execute(query)
        return db.fetchall()
    
    @staticmethod
    def deleteAircraft(msn: int):
        query = f'DELETE FROM {Aircraft.tablename} WHERE msn={msn}'
        db.execute(query)
        connection.commit()
        
    @staticmethod
    def modifyAircraft(newData:list, msn: int):
        query = F'SELECT * FROM {Aircraft.tablename} WHERE msn={msn}'
        db.execute(query)
        oldData = db.fetchone()
        print(oldData)
        newData = [val2 if val2!='' else val1 for val1, val2 in zip(oldData, newData)] # type: ignore
        print('NewDataModified= ', newData)
        Aircraft.deleteAircraft(msn)
        Aircraft.addAircraft(newData)