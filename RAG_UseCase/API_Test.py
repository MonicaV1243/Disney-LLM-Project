import requests

def test_generate_summary():
    # Define the query for testing
    query_payload = {
        "query": "Review the hotel arena."
    }

    try:
        # Send a POST request to the /generate_summary endpoint
        response = requests.post("http://127.0.0.1:5000/generate_summary", json=query_payload)
        
        # Check the response status
        if response.status_code == 200:
            print("Response from server:")
            print(response.json())
        else:
            print(f"API call failed with status code: {response.status_code}")
            print("Response text:")
            print(response.text)

    except Exception as e:
        print(f"Error while testing the API: {e}")

if __name__ == "__main__":
    test_generate_summary()
