import psycopg2
from sentence_transformers import SentenceTransformer
import numpy as np
from Logs.Logsconfig import logger

DB_Params = {
    "dbname": "Hotel_Reviews",
    "user": "postgres",
    "password": "Monica*12",
    "host": "localhost",
    "port": "5432"
}

def connect_database():
    conn = psycopg2.connect(**DB_Params)
    cursor = conn.cursor()
    return conn, cursor

# Load pre-trained DistilBERT model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Query embeddings and fetch matching results from the database
def query_similar_reviews(query):
    try:
        logger.info('Querying similar Reviews')        
        query_embedding = model.encode([query])[0]
        
        # Connect to database
        conn, cursor = connect_database()
        
        # Retrieve all embeddings from the database
        cursor.execute("SELECT Hotel_Name, Positive_Embedding, Negative_Embedding FROM Reviews")
        rows = cursor.fetchall()
        
        # Convert rows into list of embeddings and corresponding hotel names
        hotel_names = []
        positive_embeddings = []
        negative_embeddings = []
        
        for row in rows:
            hotel_names.append(row[0])
            positive_embeddings.append(np.array(row[1]))
            negative_embeddings.append(np.array(row[2]))
        
        # Compute similarity between query embedding and stored embeddings
        similarities = []
        
        for i, pos_embedding in enumerate(positive_embeddings):
            similarity = np.dot(query_embedding, pos_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(pos_embedding))
            similarities.append((hotel_names[i], similarity))
        
        # Sort similarities in descending order
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return the most similar result
        most_similar = similarities[0] if similarities else None
        conn.close()
        
        return most_similar
        
    except Exception as e:
        logger.error(f"Error during querying: {e}")
        return None
