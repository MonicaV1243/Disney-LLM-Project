import PreProcessing.preprocessing_pipeline as preprocess
import Database.database_pipeline as database_pipeline
from pandas import read_csv
from Embeddings.vector_pipeline import vectorization
from Logs.Logsconfig import logger

# Dataset Path
file_path = './data/train.csv'

# Load Dataset
data = read_csv(file_path)
logger.info("Loaded the Dataset")

# Proprocess Data 
data = preprocess.preprocess(data)
logger.info("Proprocessing complete")

# Store data into Database
result = database_pipeline.main(data)
logger.info("Stored Data into the Database")

# Generate and store embeddings
vectorization()
logger.info("Converted Unstructured data into embeddings")




