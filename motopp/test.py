import mysql.connector
import os

print("connecting to db....")
if 'ogindes' in os.environ.get("PWD"):
    host = "localhost"
    password = "Quocom@123"
else:
    host = "mysql"
    password = ""

conn = mysql.connector.connect(user='root', host=host, database='motopp', port=3306, password=password)
print(conn)
print("db connected")

cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
conn.close()

print(users)
