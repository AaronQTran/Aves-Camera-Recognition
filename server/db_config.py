import mysql.connector
from google.cloud.sql.connector import connector

def get_db_connection():
    conn = connector.connect(
        "<INSTANCE_CONNECTION_NAME>",
        "pymysql",
        user="<DB_USER>",
        password="<DB_PASSWORD>",
        db="attendance"
    )
    return conn
