import Database.Database_connection as db
from Logs.Logsconfig import logger

def insert_into_hotel_table(data):
    try:
        logger.info("Inserting data from Table Hotel")
        # Connect to the database
        conn, cursor = db.connect_database()

        data = data.to_dict(orient="records")

        # SQL query for Hotel table insertion
        hotel_query = """
        INSERT INTO Hotel (
            Hotel_Address, Hotel_Name, Average_Score, Total_Number_of_Reviews
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (Hotel_Name) DO NOTHING;
        """

        # Iterate through each row in the dataset
        for row in data:
            cursor.execute(
                hotel_query,
                (
                    row['Hotel_Address'], row['Hotel_Name'], row['Average_Score'], row['Total_Number_of_Reviews']
                )
            )

        # Commit the transaction
        conn.commit()
        logger.info("All rows inserted into Hotel table successfully.")

        # Close the cursor and connection
        db.close_connection(conn, cursor)

    except Exception as e:
        logger.error(f"Error inserting data: {e}")
