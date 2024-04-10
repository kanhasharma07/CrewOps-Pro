import mysql.connector as sql

# Connection
connection = sql.connect(
    host="localhost", user="root", password="crewdbpw", database="crewopsprodb"
)

# Cursor
db = connection.cursor()
