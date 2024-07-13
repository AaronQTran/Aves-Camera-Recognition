import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        mydb = mysql.connector.connect(
            host="104.196.28.242",
            #host="127.0.0.1",
            user="root",
            password="os$s,TYgCBV}is$h",
            database="aves-db",
            port=5432
        )
        if mydb.is_connected():
            return mydb
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

mydb = get_db_connection()

if mydb:
    try:
        mycursor = mydb.cursor()
        
        # Truncate the table
        truncate_sql = "TRUNCATE TABLE roommates"
        mycursor.execute(truncate_sql)
        
        # Insert new data
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
    except Error as e:
        print(f"Error executing SQL: {e}")
    finally:
        mycursor.close()
        mydb.close()
else:
    print("Failed to connect to the database.")
