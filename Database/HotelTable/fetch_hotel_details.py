import Database.Database_connection as db
import pandas as pd
from Logs.Logsconfig import logger

def fetch_data_from_hotel():
    try:
        logger.info("Fetching data from Table Hotel")
        # Connect to the database
        conn, cursor = db.connect_database()

        # SQL query to fetch data
        query = """SELECT * FROM Hotel;"""
        cursor.execute(query)

        # Fetch all rows
        data = cursor.fetchall()
        columns = [ 'Hotel_Address', 'Hotel_Name', 'Average_Score', 'Total_Number_of_Reviews']

        # Convert data to DataFrame
        data = pd.DataFrame(data, columns=columns)

        # Close the cursor and connection
        db.close_connection(conn, cursor)

        return data
    except Exception as e:
        logger.error(f"Error fetching data from Hotel Table: {e}")
        return None
