# LLM Data Engineer Pre-Assignment

```
This assignment entails to design and implement a scalable data pipeline that:
1. Ingest and preprocess a mixed dataset for efficient storage and retrieval in a relational database.
2. Perform vectorization of unstructured data and store the resulting embeddings in a vector storage solution.
3. Enable query-based retrieval and implement Retriever-Augmented Generation (RAG) for summarization and response generation.
```

## Pipeline Setup Instructions
### Step 1: Clone the Repository
Clone the repository to your local machine to get started.
```
git clone https://github.com/your-repo/hotel-reviews-pipeline.git
cd hotel-reviews-pipeline
```
### Step 2: Install and Set Up PostgreSQL
```
Install PostgreSQL on your system to serve as the relational database for storing structured data.
Follow the detailed steps provided in the guide below:
[How to Download, Install, and Locally Set Up PostgreSQL](https://talesofdancingcurls.medium.com/how-to-download-install-and-locally-set-up-postgresql-63f9ff4769aa)
```
### Step 3: Install the Python dependencies:
Ensure you have Python 3.11 or higher installed on your system. Then, install the required dependencies:
```
pip install -r requirements.txt
```
### Step 4: Run the Project
Execute the pipeline to preprocess the dataset, store it in the database, perform vectorization, and handle embeddings:
```
python pipeline.py
```

## Running the RAG Use Case
### Step 1: Start the Application
Run the Flask application to expose the API for querying the stored embeddings and executing the RAG use case:
```
python app.py
```
The Flask server will start, and the API will be available at http://127.0.0.1:5000/.

### Step 2: Test the API
Use the API_Test.py script to interact with the Flask API and test its functionality:
```
python API_Test.py
```
This script contains sample queries to validate:
1. Retrieval of embeddings based on similarity to the input prompt.
2. Execution of RAG workflows, such as generating summaries or responses from the retrieved data.
