from backend.connection import db, connection
from models.training_model import TrainingModel


class Training:

    TABLENAME = "training"

    @staticmethod
    def addTraining(trgdata: list):
        training = TrainingModel(
            training_id=trgdata[0],
            training_name=trgdata[1],
            training_desc=trgdata[2],
            trainer_id=trgdata[3],
            trainee_id=trgdata[4],
            training_date=trgdata[5],
            location=trgdata[6],
            duration=str(trgdata[7][0]) + ":" + str(trgdata[7][1]),
        )
        query = f"INSERT INTO {Training.TABLENAME} (training_id, training_name, training_desc, trainer, trainee, date, location, duration) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        db.execute(query, tuple(training.model_dump().values()))
        connection.commit()

    @staticmethod
    def viewTrainings():
        query = f"""SELECT
                t.training_name,
                t.training_desc,
                CONCAT("Capt ", fc1.fname, " ", fc1.lname) AS Trainer,
                CONCAT("Capt ", fc2.fname, " ", fc2.lname) as Trainee,
                t.location,
                DATE_FORMAT(t.date, '%d-%m-%Y') AS date,
                t.duration,
                t.training_id
            FROM
                flight_crew fc1
                JOIN training t ON t.trainer = fc1.staffid
                JOIN flight_crew fc2 ON t.trainee = fc2.staffid"""
        db.execute(query)
        return db.fetchall()

    @staticmethod
    def deleteTraining(trgid: int):
        query = f"DELETE FROM {Training.TABLENAME} WHERE training_id={trgid}"
        db.execute(query)
        connection.commit()
