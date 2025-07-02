
import network
import urequests
import ujson
import time

# WiFi credentials
SSID = "YOUR_WIFI_SSID"         # Update with your WiFi SSID
PASSWORD = "YOUR_WIFI_PASSWORD" # Update with your WiFi password

# Server and MongoDB details
SERVER_URL = "http://YOUR_SERVER_IP:5000/mongodb" # Update with your server URL
MONGO_URI = "mongodb://user:pass@host:port/"     # Update with your MongoDB URI

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to WiFi...")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
    print("\nConnected to WiFi, IP:", wlan.ifconfig()[0])

def send_create_request():
    payload = {
        "uri": MONGO_URI,
        "query": {
            "db": "test",
            "collection": "data",
            "operation": "create"
        }
    }
    try:
        response = urequests.post(SERVER_URL, json=payload)
        print("Create Response:", response.text)
        response.close()
    except Exception as e:
        print("Create Failed:", e)

def send_insert_single_request():
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
        response = urequests.post(SERVER_URL, json=payload)
        print("Insert Single Response:", response.text)
        response.close()
    except Exception as e:
        print("Insert Single Failed:", e)

def send_insert_multiple_request():
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
        response = urequests.post(SERVER_URL, json=payload)
        print("Insert Multiple Response:", response.text)
        response.close()
    except Exception as e:
        print("Insert Multiple Failed:", e)

def send_find_request():
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
        response = urequests.post(SERVER_URL, json=payload)
        print("Find Response:", response.text)
        response.close()
    except Exception as e:
        print("Find Failed:", e)

def send_delete_request():
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
        response = urequests.request("DELETE", SERVER_URL, json=payload)
        print("Delete Response:", response.text)
        response.close()
    except Exception as e:
        print("Delete Failed:", e)

def send_update_request():
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
        response = urequests.request("PUT", SERVER_URL, json=payload)
        print("Update Response:", response.text)
        response.close()
    except Exception as e:
        print("Update Failed:", e)

# Main execution
connect_wifi()
while True:
    send_create_request()
    time.sleep(2)
    send_insert_single_request()
    time.sleep(2)
    send_insert_multiple_request()
    time.sleep(2)
    send_find_request()
    time.sleep(2)
    send_update_request()
    time.sleep(2)
    send_delete_request()
    time.sleep(10)
