import mysql.connector

database = mysql.connector.connect(
    host ='localhost',
    user = 'root',
    password = 'P@$$w2rd',
)
# Cursor Object
cursorObject = database.cursor()
# Create Database
cursorObject.execute("CREATE DATABASE bank")

print("Database Successfully Created")