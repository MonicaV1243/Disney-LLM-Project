import psycopg2
from config import DB_Params
from Logs.Logsconfig import logger

def connect_database():
    try:
        conn = psycopg2.connect(**DB_Params)
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        logger.error("Error connecting to the database" + str(e))

def close_connection(conn, cursor):
    # Close the cursor and connection
    cursor.close()
    conn.close()
