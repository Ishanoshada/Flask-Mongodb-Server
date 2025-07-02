import requests
import json

# Configuration
SERVER_URL = "http://localhost:5000/mongodb"  # Update with your server URL
MONGO_URI = "mongodb://user:pass@host:port/"  # Update with your MongoDB URI

def send_create_request():
    """Send a POST request to create a collection."""
    payload = {
        "uri": MONGO_URI,
        "query": {
            "db": "test",
            "collection": "data",
            "operation": "create"
        }
    }
    try:
        response = requests.post(SERVER_URL, json=payload)
        print("Create Response:", response.status_code, response.json())
    except Exception as e:
        print("Create Failed:", str(e))

def send_insert_single_request():
    """Send a POST request to insert a single document."""
    payload = {
        "uri": MONGO_URI,
        "query": {
            "db": "test",
            "collection": "data",
            "operation": "insert",
            "data": {"name": "John", "age": 25}
        }
    }
    try:
        response = requests.post(SERVER_URL, json=payload)
        print("Insert Single Response:", response.status_code, response.json())
    except Exception as e:
        print("Insert Single Failed:", str(e))

def send_insert_multiple_request():
    """Send a POST request to insert multiple documents."""
    payload = {
        "uri": MONGO_URI,
        "query": {
            "db": "test",
            "collection": "data",
            "operation": "insert",
            "data": [
                {"name": "John", "age": 25},
                {"name": "Jane", "age": 30}
            ]
        }
    }
    try:
        response = requests.post(SERVER_URL, json=payload)
        print("Insert Multiple Response:", response.status_code, response.json())
    except Exception as e:
        print("Insert Multiple Failed:", str(e))

def send_find_request():
    """Send a POST request to find documents."""
    payload = {
        "uri": MONGO_URI,
        "query": {
            "db": "test",
            "collection": "data",
            "operation": "find",
            "filter": {"name": "John"}
        }
    }
    try:
        response = requests.post(SERVER_URL, json=payload)
        print("Find Response:", response.status_code, response.json())
    except Exception as e:
        print("Find Failed:", str(e))

def send_delete_request():
    """Send a DELETE request to delete documents."""
    payload = {
        "uri": MONGO_URI,
        "query": {
            "db": "test",
            "collection": "data",
            "operation": "delete",
            "filter": {"name": "John"}
        }
    }
    try:
        response = requests.delete(SERVER_URL, json=payload)
        print("Delete Response:", response.status_code, response.json())
    except Exception as e:
        print("Delete Failed:", str(e))

def send_update_request():
    """Send a PUT request to update documents."""
    payload = {
        "uri": MONGO_URI,
        "query": {
            "db": "test",
            "collection": "data",
            "operation": "update",
            "filter": {"name": "John"},
            "update": {"$set": {"age": 30}}
        }
    }
    try:
        response = requests.put(SERVER_URL, json=payload)
        print("Update Response:", response.status_code, response.json())
    except Exception as e:
        print("Update Failed:", str(e))

if __name__ == "__main__":
    print("Testing MongoDB Server Operations")
    print("-" * 40)
    
    send_create_request()
    print("-" * 40)
    
    send_insert_single_request()
    print("-" * 40)
    
    send_insert_multiple_request()
    print("-" * 40)
    
    send_find_request()
    print("-" * 40)
    
    send_update_request()
    print("-" * 40)
    
    send_delete_request()
