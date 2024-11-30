from datetime import datetime
import Database.Database_connection as db
from Logs.Logsconfig import logger

def preprocess_date(date_str):
    try:
        return datetime.strptime(date_str, "%m%d%Y").strftime("%Y-%m-%d")
    except ValueError:
        # If the date format is invalid, return None or handle the error accordingly
        logger.error(f"Invalid date format: {date_str}")
        return None

def review_table(data):
    try:
        logger.info("Inserting data into Table Reviews")
        # Connect to the database
        conn, cursor = db.connect_database()
        data = data.to_dict(orient="records")

        # SQL query for Reviews table insertion
        review_query = """
        INSERT INTO Reviews (
            Hotel_Name, Reviewer_Nationality, Total_Number_of_Reviews_Reviewer_Has_Given,
            Review_Date, Negative_Review, Positive_Review, Tags,
            Positive_Review_NER, Negative_Review_NER
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Iterate through DataFrame rows as named tuples
        for row in data:
            review_date = preprocess_date(row['Review_Date'])

            # Insert each row into the database
            cursor.execute(
                review_query,
                (
                    row['Hotel_Name'], row['Reviewer_Nationality'], row['Total_Number_of_Reviews_Reviewer_Has_Given'],
                    review_date, row['Negative_Review'], row['Positive_Review'], row['Tags'],
                    row['Positive_Review_NER'], row['Negative_Review_NER']
                )
            )

        # Commit the transaction
        conn.commit()
        logger.info("All rows inserted into Reviews table successfully.")

        # Close the cursor and connection
        db.close_connection(conn, cursor)

    except Exception as e:
        logger.error(f"Error inserting data: {e}")
