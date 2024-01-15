from models.ame_crew_model import AMECrewModel
from backend.connection import connection, db

class AMECrew:
    
    @staticmethod
    def addCrew(sap: int,
                name: str,
                fleet: str, 
                pw: str, 
                login = None):
        
        ame = AMECrewModel(sap=sap, name=name, fleet_cert=fleet, pw=pw, login=login)
        
        tablename = 'ame_crew'
        query = f'INSERT INTO {tablename} (staffid, name, fleet_certified, login, pw) VALUES (%s,%s,%s,%s,%s)'
        values = tuple(ame.model_dump().values())
        db.execute(query, values)
        connection.commit()
        
        
    @staticmethod    
    def deleteCrew(sap):
        tablename = 'ame_crew'
        db.execute(f"DELETE FROM {tablename} WHERE staffid = {sap}")
        connection.commit()
        


if __name__=='__main__':
    pass
    # AMECrew.addCrew(80050322, 'kanha sharma', 'b737', 'heeyaw')
    # AMECrew.deleteCrew(80050322)