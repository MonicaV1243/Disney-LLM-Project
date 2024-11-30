from Database.ReviewsTable import insert_into_reviews
from Database.HotelTable import insert_into_hotel
import Database.CreateDatabase as cd
from Logs.Logsconfig import logger

def main(data):
    try:
        # Create a database and the necessary tables
        cd.create_database()
        cd.create_tables()

        # Insert rows into Hotel Table
        hotel_data = data.drop_duplicates(subset=['Hotel_Name'])
        insert_into_hotel.insert_into_hotel_table(hotel_data)

        # Insert rows into Reviews Table
        insert_into_reviews.review_table(data)
    
    except Exception as e:
        logger.error("Action Failed :" + str(e))
        return None