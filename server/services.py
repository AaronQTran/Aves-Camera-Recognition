import json
import threading
import mysql.connector
from db_config import get_db_connection
json_lock = threading.Lock()

def update_roommate_status(name, new_status):
    connection = get_db_connection()
    cursor = connection.cursor()

    update_sql = "UPDATE roommates SET status = %s WHERE name = %s"
    cursor.execute(update_sql, (new_status, name))
    connection.commit()

    cursor.close()
    connection.close()

    return {"status": "success", "message": f"Updated {name} to {new_status}"}

def get_statistics(name):
    connection = get_db_connection()
    cursor = connection.cursor()

    select_sql = """
    SELECT status, monday, tuesday, wednesday, thursday, friday, saturday, sunday, avgTimesLeft, lastEnter, lastExit, avgTimeAway,  timeStamp, totalTimeAway, timeInstances
    FROM roommates
    WHERE name = %s
    """
    cursor.execute(select_sql, (name,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return {
            "status": result[0],
            "monday": result[1],
            "tuesday": result[2],
            "wednesday": result[3],
            "thursday": result[4],
            "friday": result[5],
            "saturday": result[6],
            "sunday": result[7],
            "avgTimesLeft": result[8],
            "lastEnter": result[9],
            "lastExit": result[10],
            "avgTimeAway": result[11],
            "timeStamp" : result[12],
            "totalTimeAway" : result[13],
            "timeInstances" : result[14]
        }
    else:
        return {"error": "No data found for the specified name"}
