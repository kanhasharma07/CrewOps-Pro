from backend.connection import db, connection
from models.training_model import TrainingModel


class Training:
    """
    The 'Training' class represents a utility class for managing training data in the database.

    Attributes:
        TABLENAME (str): The name of the table in the database that stores training data.

    Methods:
        addTraining(trgdata: list) -> None: Adds a new training record to the database.
        viewTrainings() -> list: Retrieves a list of all training records from the database.
        deleteTraining(trgid: int) -> None: Deletes a training record from the database.

    Note: This class interacts with the 'TrainingModel' class from the 'models.training_model' module to validate and manipulate training data before storing it in the database.
    """

    TABLENAME = "training"

    @staticmethod
    def addTraining(trgdata: list) -> None:
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
    def viewTrainings() -> list:
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
    def deleteTraining(trgid: int) -> None:
        query = f"DELETE FROM {Training.TABLENAME} WHERE training_id={trgid}"
        db.execute(query)
        connection.commit()
