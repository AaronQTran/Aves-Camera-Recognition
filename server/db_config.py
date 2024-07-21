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
            port=3306
        )
        if mydb.is_connected():
            return mydb
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def initialize_database():
    mydb = get_db_connection()
    if mydb:
        try:
            mycursor = mydb.cursor()
            
            # Drop the table
            drop_sql = "DROP TABLE IF EXISTS roommates"
            mycursor.execute(drop_sql)

            # Create the table
            create_sql = """
            CREATE TABLE roommates (
                name VARCHAR(255),
                status VARCHAR(255),
                monday INT,
                tuesday INT,
                wednesday INT,
                thursday INT,
                friday INT,
                saturday INT,
                sunday INT,
                lastEnter VARCHAR(255),
                lastExit VARCHAR(255),
                avgTimeAway VARCHAR(255),
                avgTimesLeft INT,
                timeStamp VARCHAR(255),
                totalTimeAway DOUBLE,
                check1 INT,
                check2 INT,
                timeStart DOUBLE,
                timeEnd DOUBLE,
                timeInstances INT
            )
            """
            mycursor.execute(create_sql)
            
            # Insert new data
            sql = "INSERT INTO roommates (name, status, monday, tuesday, wednesday, thursday, friday, saturday, sunday, lastEnter, lastExit, avgTimeAway, avgTimesLeft, timeStamp, totalTimeAway, check1, check2, timeStart, timeEnd, timeInstances) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, %s, %s)"
            val = [
                ("Andrew", "Inside", 0, 0, 0, 0, 0, 0, 0, "test", "test", "test", 0, "0", 0, 0, 0, 0, 0, 0),
                ("Kamryn", "Inside", 5, 2, 6, 2, 9, 2, 1, "Null", "Null", "Null", 0, "0", 0, 0, 0, 0, 0, 0),
                ("Jordan", "Inside", 0, 0, 0, 0, 0, 0, 0, "Null", "Null", "Null", 0, "0", 0, 0, 0, 0, 0, 0),
                ("Nick", "Inside", 0, 0, 0, 0, 0, 0, 0, "Null", "Null", "Null", 0, "0", 0, 0, 0, 0, 0, 0)
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

if __name__ == "__main__":
    initialize_database()
