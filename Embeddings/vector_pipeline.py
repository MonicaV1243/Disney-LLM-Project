import Embeddings.vectorization as vector
from Logs.Logsconfig import logger
def vectorization():
    try:
        # Fetch Data from Reviews Table
        data = vector.fetch_data()

        # Generate and store embeddings in FAISS
        vector.store_embeddings_in_sql(data)
    except Exception as e:
        logger.error("Error Occurred :" + str(e))
        return None
