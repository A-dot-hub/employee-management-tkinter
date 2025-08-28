import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="9321675524@j",
        database="employee_management"
    )
