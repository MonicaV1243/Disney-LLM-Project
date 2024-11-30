from flask import Flask, request, jsonify
from psycopg2 import connect

from generate_summary import generate_summary
from similar_query_reviews import query_similar_reviews
from Logs.Logsconfig import logger
# Initialize Flask app
app = Flask(__name__)

# Database connection function
def connect_database():
    conn = connect(
        dbname="hotel_reviews",
        user="your_user",
        password="your_password",
        host="localhost",
        port="5432"
    )
    return conn

@app.route('/generate_summary', methods=['POST'])
def generate_summary_from_query():
    data = request.get_json()
    query = data.get('query', '')
    
    # Retrieve similar reviews
    result = query_similar_reviews(query)
    
    if result:
        hotel_name = result[0]
        
        # Generate summary based on similar reviews 
        summary = generate_summary([hotel_name]) 
        
        return jsonify({'hotel': hotel_name, 'summary': summary}), 200
    else:
        logger.error({'error': 'No similar reviews found'})
        return jsonify({'error': 'No similar reviews found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
