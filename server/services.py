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
    cursor = connection.cursor() #cursor allows u to iterate records of table and query/fetch

    select_sql = "SELECT avgTimesLeft, lastEnter, lastExit, avgTimeAway FROM roommates WHERE name = %s"
    cursor.execute(select_sql, (name,))
    result = cursor.fetchone() #result equals none if it cant find row, otherwise it equals a tuple that has he values 

    cursor.close()
    connection.close()

    if result:
        return {
            "avgTimesLeft": result[0],
            "lastTimeEntered": result[1],
            "lastTimeExited": result[2],
            "avgTimeAway": result[3]
        }
    else:
        return {"error": "No data found for the specified name"}