import psycopg2 
import Database.Database_connection as db
from Logs.Logsconfig import logger

def create_database():
    try:
        db_params = {
        'user': 'postgres',       
        'password': 'Monica*12',   
        'host': 'localhost',
        'port': '5432'
        }
        connection = psycopg2.connect(**db_params)
        connection.autocommit = True
        cursor = connection.cursor()

        # Check if database exists, and create it if not
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'Hotel_Reviews';")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute('CREATE DATABASE "Hotel_Reviews";')
            logger.info("Database 'Hotel_Reviews' created successfully.")
        else:
            logger.info("Database 'Hotel_Reviews' already exists.")
        cursor.close()
        connection.close() 
    except Exception as e:
        logger.error(f"Error creating database: {e}")

def enable_uuid_extension():
    try:
        # Connect to your PostgreSQL database
        conn, cursor = db.connect_database()

        # Enable the uuid-ossp extension
        cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        logger.info("Extension uuid-ossp enabled successfully.")

        # Check if the extension is installed
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'uuid-ossp';")
        result = cursor.fetchone()
        
        if result:
            logger.info("uuid-ossp extension is installed.")
        else:
            logger.warning("uuid-ossp extension not found.")

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        
def create_tables():
    try:
        logger.info("Creating Tables Hotel and Reviews")
        # Connect to the Hotel_Reviews database
        conn, cursor = db.connect_database()
        enable_uuid_extension()
        # Create Hotel table
        create_hotel_table = """
            CREATE TABLE IF NOT EXISTS Hotel (
                Hotel_Address TEXT,
                Hotel_Name TEXT PRIMARY KEY,
                Average_Score FLOAT,
                Total_Number_of_Reviews INT
            );
        """
        
        # Create Reviews table with foreign key constraint
        create_reviews_table = """
            CREATE TABLE IF NOT EXISTS Reviews (
                Unique_ID UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                Hotel_Name TEXT,
                Reviewer_Nationality TEXT,
                Total_Number_of_Reviews_Reviewer_Has_Given INT,
                Review_Date DATE,
                Negative_Review TEXT,
                Positive_Review TEXT,
                Tags TEXT,
                Positive_Review_NER TEXT,
                Negative_Review_NER TEXT,
                Positive_Embedding FLOAT[],
                Negative_Embedding FLOAT[],
                FOREIGN KEY (Hotel_Name) REFERENCES Hotel(Hotel_Name)
            );
        """

        # Execute SQL queries to create tables
        cursor.execute(create_hotel_table)
        logger.info("Table Hotel created or already exist")
        cursor.execute(create_reviews_table)
        logger.info("Table Reviews created or already exist")

        # Commit changes and close the connection
        conn.commit()
        db.close_connection(conn, cursor)
    except Exception as e:
        logger.error(f"Error creating tables: {e}")

