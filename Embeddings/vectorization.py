from sentence_transformers import SentenceTransformer
from Database.ReviewsTable import fetch_reviews
import Database.Database_connection as cd
from Logs.Logsconfig import logger

def fetch_data():
    try:
        data = fetch_reviews.fetch_data_from_reviews()
        return data
    except Exception as e:
        return "Error fetching data: " + str(e)

def embed_text_data(data):
    try:
        logger.info("Geberating Embedding for unstructured data")
        # Load a pre-trained Sentence Transformer model
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        # Encode the reviews into embeddings
        positive_embeddings = model.encode(data['Positive_Review'].tolist(), show_progress_bar=True)
        negative_embeddings = model.encode(data['Negative_Review'].tolist(), show_progress_bar=True)

        # Convert numpy arrays to lists for storing in database
        positive_embeddings = positive_embeddings.tolist()
        negative_embeddings = negative_embeddings.tolist()

        logger.info("Embedded unstructured data")
        return positive_embeddings, negative_embeddings
    except Exception as e:
        logger.error(f"Error embedding text data: {e}")
        return None
    

def store_embeddings_in_sql(data):
    try:
        logger.info("Storing the embeddings into Database")
        # Connect to the database
        conn, cursor = cd.connect_database()

        # Define the SQL queries for inserting embeddings
        update_query = """
        UPDATE Reviews
        SET Positive_Embedding = %s, Negative_Embedding = %s
        WHERE Unique_ID = %s;
        """

        # Generate embeddings
        positive_embeddings, negative_embeddings = embed_text_data(data)

        # Iterate through the rows in the DataFrame
        for index, row in data.iterrows():
            unique_id = row['Unique_ID']
            cursor.execute("SELECT COUNT(1) FROM Reviews WHERE Unique_ID = %s", (unique_id,))
            result = cursor.fetchone()

            if result[0] > 0:
                # If the Unique_ID exists, update the embeddings for that row
                cursor.execute(update_query, (
                    positive_embeddings[index], 
                    negative_embeddings[index], 
                    unique_id
                ))
            else:
                logger.error(f"Unique_ID {unique_id} not found in the database. Skipping this entry.")


        # Commit the transaction
        conn.commit()
        logger.info("Embeddings stored successfully.")

        # Close the cursor and connection
        cd.close_connection(conn, cursor)

    except Exception as e:
        logger.error(f"Error storing embeddings: {e}")
