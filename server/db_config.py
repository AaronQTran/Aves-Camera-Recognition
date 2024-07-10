import mysql.connector

def get_db_connection():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="os$s,TYgCBV}is$h",
        database="aves-db",
        port=5432 
    )

mycursor = mydb.cursor()


sql = "INSERT INTO roommates (name, status, monday, tuesday, wednesday, thursday, friday, saturday, sunday, lastEnter, lastExit, avgTimeAway, avgTimeLeft, timeStamp, totalTimeAway, timeInstances) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
val = [
    ("Andrew", "Inside", 0, 0, 0, 0, 0, 0, 0, "Null", "Null", "Null", 0, "Null", 0, 0),
    ("Kamryn", "Inside", 0, 0, 0, 0, 0, 0, 0, "Null", "Null", "Null", 0, "Null", 0, 0),
    ("Jordan", "Inside", 0, 0, 0, 0, 0, 0, 0, "Null", "Null", "Null", 0, "Null", 0, 0),
    ("Nick", "Inside", 0, 0, 0, 0, 0, 0, 0, "Null", "Null", "Null", 0, "Null", 0, 0)
]

mycursor.executemany(sql, val)
mydb.commit()

print(mycursor.rowcount, "record(s) inserted.")
