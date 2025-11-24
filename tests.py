import requests
import json

# Define the base URL of your API
BASE_URL = "http://127.0.0.1:5000"

def test_get_endpoint():
    """
    Tests a GET request to a specific endpoint.
    """
    endpoint = "/get_products"
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"GET {url} - Status Code: {response.status_code}")
        print(f"Response JSON: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error during GET request: {e}")

def test_post_endpoint():
    """
    Tests a POST request to a specific endpoint with data.
    """
    endpoint = "/create_product"
    url = f"{BASE_URL}{endpoint}"
    payload = {"name": "Z", "description": "This is a test item"}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print(f"POST {url} - Status Code: {response.status_code}")
        print(f"Response JSON: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 201 # Assuming 201 Created for a successful POST
        # Add more assertions based on your expected response data
        print(response.json())
        assert "id" in response.json()["item"]
        assert response.json()["item"]["name"] == "Z"
    except requests.exceptions.RequestException as e:
        print(f"Error during POST request: {e}")

if __name__ == "__main__":
    print("Running API tests...")
    test_get_endpoint()
    print("\n")
    test_post_endpoint()
    print("\nAPI tests completed.")
