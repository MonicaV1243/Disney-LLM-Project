import Database.Database_connection as db
import pandas as pd
from Logs.Logsconfig import logger

def fetch_data_from_reviews():
    try:
        logger.info("Fetching Data from Table Reviews")
        # Connect to the database
        conn, cursor = db.connect_database()

        # SQL query to fetch data
        query = """SELECT * FROM Reviews;"""
        cursor.execute(query)

        # Fetch all rows
        data = cursor.fetchall()
        columns = [ 'Unique_ID', 'Hotel_Name', 'Reviewer_Nationality', 'Total_Number_of_Reviews_Reviewer_Has_Given', 'Review_Date', 
                    'Negative_Review', 'Positive_Review', 'Tags',
                    'Positive_Review_NER', 'Negative_Review_NER', 'Positive_Embedding', 'Negative_Embedding'
                    ]

        # Convert data to DataFrame
        data = pd.DataFrame(data, columns=columns)

        # Close the cursor and connection
        db.close_connection(conn, cursor)

        return data
    except Exception as e:
        logger.error(f"Error fetching data from Reviews Table: {e}")
        return None
