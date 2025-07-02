# Flask-MongoDB-Server

This project provides a Flask-based web server that acts as a general-purpose interface for MongoDB operations. It allows any client (e.g., microcontrollers like ESP32, web applications, or scripts) to perform MongoDB operations (create, insert, find, delete, update) via HTTP POST, PUT, and DELETE requests. The server is designed to be flexible and can be used with any device or application capable of sending HTTP requests with JSON payloads.

## Features
- **Flask Server**: Exposes a RESTful endpoint (`/mongodb`) to handle MongoDB operations.
- **Supported Operations**:
  - `create` (POST): Create a new database and collection if they don’t exist.
  - `insert` (POST): Add one or more documents to a collection.
  - `find` (POST): Retrieve documents matching a filter.
  - `delete` (DELETE): Delete documents matching a filter.
  - `update` (PUT): Update documents with a specified filter and update operation.
- **Client Flexibility**: Compatible with any client that can send HTTP POST, PUT, or DELETE requests with JSON payloads, including microcontrollers (e.g., ESP32), web apps, or command-line tools.
- **Secure Transmission**: Queries and MongoDB URI are sent in JSON payloads, ensuring safe data transfer when using HTTPS.
- **Example Clients**: Includes an ESP32 sketch, MicroPython examples, and a Python test script.

## Project Structure
- `/index/api.py`: Flask server script for MongoDB operations.
- `esp32_mongodb.ino`: Example ESP32 Arduino sketch for sending queries.
- `esp32_arduino_examples.ino`: Arduino example with functions for all MongoDB operations.
- `esp32_micropython_examples.py`: MicroPython example with functions for all MongoDB operations.
- `test_mongodb_server.py`: Python script to test the server with all operations.
- `requirements.txt`: Python dependencies for the Flask server and test script.
- `README.md`: Project documentation (this file).
- `.gitignore`: Excludes unnecessary files from version control.

## Prerequisites
### Flask Server
- Python 3.8 or higher
- MongoDB instance (e.g., MongoDB Atlas)
- Dependencies listed in `requirements.txt`

### Example ESP32 Client (Optional)
- ESP32 board (e.g., ESP32 DevKit)
- Arduino IDE with ESP32 board support or MicroPython firmware
- Arduino libraries: `WiFi`, `HTTPClient`, `ArduinoJson` (install via Library Manager)
- MicroPython libraries: `urequests` (install via `upip`)

### Test Script (Optional)
- Python 3.8 or higher
- `requests` library (included in `requirements.txt`)

## Setup Instructions
### Flask Server
1. Clone the repository:
   ```bash
   git clone https://github.com/ishanoshada/Flask-Mongodb-Server.git
   cd Flask-Mongodb-Server
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```bash
   python ./index/api.py
   ```
   The server will run on `http://<your-server-ip>:5000`.

### Example ESP32 Client (Optional)
#### Arduino (C/C++)
1. Open `esp32_arduino_examples.ino` or `esp32_mongodb.ino` in the Arduino IDE.
2. Update the following variables:
   - `ssid`: Your WiFi network name.
   - `password`: Your WiFi password.
   - `serverUrl`: The Flask server URL (e.g., `http://<your-server-ip>:5000/mongodb`).
   - `mongoUri`: Your MongoDB URI (e.g., `mongodb://user:pass@host:port/`).
3. Install required libraries in Arduino IDE:
   - Go to **Sketch > Include Library > Manage Libraries**.
   - Install `ArduinoJson` (by Benoit Blanchon).
4. Upload the sketch to your ESP32 board.
5. For `esp32_arduino_examples.ino`, call the desired function (e.g., `sendCreateRequest()`) in `loop()`.

#### MicroPython
1. Install MicroPython on your ESP32 (see `micropython.org`).
2. Install the `urequests` library:
   ```bash
   import upip
   upip.install("micropython-urequests")
   ```
3. Upload `esp32_micropython_examples.py` to your ESP32 using a tool like `ampy` or `rshell`.
4. Update `SSID`, `PASSWORD`, `SERVER_URL`, and `MONGO_URI` in the script.
5. Run the script and call the desired function (e.g., `send_create_request()`) via the MicroPython REPL.

### Test Script
1. Ensure the Flask server is running.
2. Update `test_mongodb_server.py` with your server URL and MongoDB URI:
   - `SERVER_URL`: Set to the Flask server URL (e.g., `http://<your-server-ip>:5000/mongodb`).
   - `MONGO_URI`: Set to your MongoDB URI (e.g., `mongodb://user:pass@host:port/`).
3. Run the test script:
   ```bash
   python test_mongodb_server.py
   ```

## Constructing Requests
The server accepts HTTP POST, PUT, and DELETE requests at `/mongodb` with a JSON payload containing `uri` and `query`. The `query` field specifies the MongoDB operation and its parameters. The JSON payload does not require URL-encoding since it is sent in the request body, but the MongoDB URI should be properly formatted.

### Request Structure
- **Endpoint**: `http://<your-server-ip>:5000/mongodb`
- **Headers**: `Content-Type: application/json`
- **Body**: JSON object with:
  - `uri`: MongoDB connection string (e.g., `mongodb://user:pass@host:port/`).
  - `query`: Object containing `db`, `collection`, `operation`, and operation-specific fields (e.g., `data` for insert, `filter` for find/delete, `filter` and `update` for update).

## Example Requests
The following examples show the JSON payloads for each operation and their expected responses. Use these payloads in the request body for POST, PUT, or DELETE requests to `/mongodb`.

### Create (POST)
- **JSON Payload**:
  ```json
  {
    "uri": "mongodb://user:pass@host:port/",
    "query": {
      "db": "test",
      "collection": "data",
      "operation": "create"
    }
  }
  ```
- **Response**:
  ```json
  {"message": "Collection data created in database test"}
  ```
  or, if the collection already exists:
  ```json
  {"message": "Collection data already exists in database test"}
  ```
- **cURL Command**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"uri":"mongodb://user:pass@host:port/","query":{"db":"test","collection":"data","operation":"create"}}' http://<server-ip>:5000/mongodb
  ```

### Insert (Single Document, POST)
- **JSON Payload**:
  ```json
  {
    "uri": "mongodb://user:pass@host:port/",
    "query": {
      "db": "test",
      "collection": "data",
      "operation": "insert",
      "data": {"name": "John", "age": 25}
    }
  }
  ```
- **Response**:
  ```json
  {"inserted_id": "507f1f77bcf86cd799439011"}
  ```
- **cURL Command**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"uri":"mongodb://user:pass@host:port/","query":{"db":"test","collection":"data","operation":"insert","data":{"name":"John","age":25}}}' http:/
/<server-ip>:5000/mongodb
  ```

### Insert (Multiple Documents, POST)
- **JSON Payload**:
  ```json
  {
    "uri": "mongodb://user:pass@host:port/",
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
  ```
- **Response**:
  ```json
  {"inserted_ids": ["507f1f77bcf86cd799439011", "507f1f77bcf86cd799439012"]}
  ```
- **cURL Command**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"uri escult="mongodb://user:pass@host:port/","query":{"db":"test","collection":"data","operation":"insert","data":[{"name":"John","age":25},{"name":"Jane","age":30}]}}' http://<server-ip>:5000/mongodb
  ```

### Find (POST)
- **JSON Payload**:
  ```json
  {
    "uri": "mongodb://user:pass@host:port/",
    "query": {
      "db": "test",
      "collection": "data",
      "operation": "find",
      "filter": {"name": "John"}
    }
  }
  ```
- **Response**:
  ```json
  {"results": [{"_id": "507f1f77bcf86cd799439011", "name": "John", "age": 25}]}
  ```
- **cURL Command**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"uri":"mongodb://user:pass@host:port/","query":{"db":"test","collection":"data","operation":"find","filter":{"name":"John"}}}' http://<server-ip>:5000/mongodb
  ```

### Delete (DELETE)
- **JSON Payload**:
  ```json
  {
    "uri": "mongodb://user:pass@host:port/",
    "query": {
      "db": "test",
      "collection": "data",
      "operation": "delete",
      "filter": {"name": "John"}
    }
  }
  ```
- **Response**:
  ```json
  {"deleted_count": 2}
  ```
- **cURL Command**:
  ```bash
  curl -X DELETE -H "Content-Type: application/json" -d '{"uri":"mongodb://user:pass@host:port/","query":{"db":"test","collection":"data","operation":"delete","filter":{"name":"John"}}}' http://<server-ip>:5000/mongodb
  ```

### Update (PUT)
- **JSON Payload**:
  ```json
  {
    "uri": "mongodb://user:pass@host:port/",
    "query": {
      "db": "test",
      "collection": "data",
      "operation": "update",
      "filter": {"name": "John"},
      "update": {"$set": {"age": 30}}
    }
  }
  ```
- **Response**:
  ```json
  {"matched_count": 2, "modified_count": 2}
  ```
- **cURL Command**:
  ```bash
  curl -X PUT -H "Content-Type: application/json" -d '{"uri":"mongodb://user:pass@host:port/","query":{"db":"test","collection":"data","operation":"update","filter":{"name":"John"},"update":{"$set":{"age":30}}}}' http://<server-ip>:5000/mongodb
  ```

## Example Clients
The project includes example clients to demonstrate how to interact with the Flask server’s `/mongodb` endpoint. Below are code snippets for an ESP32 using Arduino (C/C++) and MicroPython, covering all supported operations (`create`, `insert`, `find`, `delete`, `update`). Full example code is provided in `esp32_arduino_examples.ino` and `esp32_micropython_examples.py`.

### Arduino (C/C++) Client for ESP32
The following snippets (from `esp32_arduino_examples.ino`) use the `WiFi`, `HTTPClient`, and `ArduinoJson` libraries to send HTTP POST, PUT, and DELETE requests for each operation. Update `ssid`, `password`, `serverUrl`, and `mongoUri` before use.

#### Create (POST)
```cpp
void sendCreateRequest() {
  HTTPClient http;
  StaticJsonDocument<300> doc;
  doc["uri"] = mongoUri;
  JsonObject query = doc.createNestedObject("query");
  query["db"] = "test";
  query["collection"] = "data";
  query["operation"] = "create";

  String payload;
  serializeJson(doc, payload);
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  int httpCode = http.POST(payload);
  if (httpCode > 0) {
    Serial.println("Create Response: " + http.getString());
  } else {
    Serial.println("Create Failed: " + http.errorToString(httpCode));
  }
  http.end();
}
```

#### Insert (Single Document, POST)
```cpp
void sendInsertSingleRequest() {
  HTTPClient http;
  StaticJsonDocument<300> doc;
  doc["uri"] = mongoUri;
  JsonObject query = doc.createNestedObject("query");
  query["db"] = "test";
  query["collection"] = "data";
  query["operation"] = "insert";
  JsonObject data = query.createNestedObject("data");
  data["name"] = "John";
  data["age"] = 25;

  String payload;
  serializeJson(doc, payload);
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  int httpCode = http.POST(payload);
  if (httpCode > 0) {
    Serial.println("Insert Single Response: " + http.getString());
  } else {
    Serial.println("Insert Single Failed: " + http.errorToString(httpCode));
  }
  http.end();
}
```

#### Insert (Multiple Documents, POST)
```cpp
void sendInsertMultipleRequest() {
  HTTPClient http;
  StaticJsonDocument<300> doc;
  doc["uri"] = mongoUri;
  JsonObject query = doc.createNestedObject("query");
  query["db"] = "test";
  query["collection"] = "data";
  query["operation"] = "insert";
  JsonArray data = query.createNestedArray("data");
  JsonObject doc1 = data.createNestedObject();
  doc1["name"] = "John";
  doc1["age"] = 25;
  JsonObject doc2 = data.createNestedObject();
  doc2["name"] = "Jane";
  doc2["age"] = 30;

  String payload;
  serializeJson(doc, payload);
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  int httpCode = http.POST(payload);
  if (httpCode > 0) {
    Serial.println("Insert Multiple Response: " + http.getString());
  } else {
    Serial.println("Insert Multiple Failed: " + http.errorToString(httpCode));
  }
  http.end();
}
```

#### Find (POST)
```cpp
void sendFindRequest() {
  HTTPClient http;
  StaticJsonDocument<300> doc;
  doc["uri"] = mongoUri;
  JsonObject query = doc.createNestedObject("query");
  query["db"] = "test";
  query["collection"] = "data";
  query["operation"] = "find";
  JsonObject filter = query.createNestedObject("filter");
  filter["name"] = "John";

  String payload;
  serializeJson(doc, payload);
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  int httpCode = http.POST(payload);
  if (httpCode > 0) {
    Serial.println("Find Response: " + http.getString());
  } else {
    Serial.println("Find Failed: " + http.errorToString(httpCode));
  }
  http.end();
}
```

#### Delete (DELETE)
```cpp
void sendDeleteRequest() {
  HTTPClient http;
  StaticJsonDocument<300> doc;
  doc["uri"] = mongoUri;
  JsonObject query = doc.createNestedObject("query");
  query["db"] = "test";
  query["collection"] = "data";
  query["operation"] = "delete";
  JsonObject filter = query.createNestedObject("filter");
  filter["name"] = "John";

  String payload;
  serializeJson(doc, payload);
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  int httpCode = http.sendRequest("DELETE", payload);
  if (httpCode > 0) {
    Serial.println("Delete Response: " + http.getString());
  } else {
    Serial.println("Delete Failed: " + http.errorToString(httpCode));
  }
  http.end();
}
```

#### Update (PUT)
```cpp
void sendUpdateRequest() {
  HTTPClient http;
  StaticJsonDocument<300> doc;
  doc["uri"] = mongoUri;
  JsonObject query = doc.createNestedObject("query");
  query["db"] = "test";
  query["collection"] = "data";
  query["operation"] = "update";
  JsonObject filter = query.createNestedObject("filter");
  filter["name"] = "John";
  JsonObject update = query.createNestedObject("update");
  JsonObject setData = update.createNestedObject("$set");
  setData["age"] = 30;

  String payload;
  serializeJson(doc, payload);
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  int httpCode = http.PUT(payload);
  if (httpCode > 0) {
    Serial.println("Update Response: " + http.getString());
  } else {
    Serial.println("Update Failed: " + http.errorToString(httpCode));
  }
  http.end();
}
```

**Setup**:
1. Install libraries in Arduino IDE: `WiFi`, `HTTPClient`, `ArduinoJson` (via Library Manager).
2. Open `esp32_arduino_examples.ino` and update `ssid`, `password`, `serverUrl`, and `mongoUri`.
3. Call the desired function (e.g., `sendCreateRequest()`) in `loop()` or `setup()`.
4. Upload to your ESP32 board.
5. Monitor Serial output (115200 baud) for responses.

### MicroPython Client for ESP32
The following snippets (from `esp32_micropython_examples.py`) use the `urequests` library to send HTTP POST, PUT, and DELETE requests for each operation. Update `SSID`, `PASSWORD`, `SERVER_URL`, and `MONGO_URI` before use.

#### Create (POST)
```python
def send_create_request():
    import urequests
    import ujson
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
```

#### Insert (Single Document, POST)
```python
def send_insert_single_request():
    import urequests
    import ujson
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
```

#### Insert (Multiple Documents, POST)
```python
def send_insert_multiple_request():
    import urequests
    import ujson
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
```

#### Find (POST)
```python
def send_find_request():
    import urequests
    import ujson
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
```

#### Delete (DELETE)
```python
def send_delete_request():
    import urequests
    import ujson
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
```

#### Update (PUT)
```python
def send_update_request():
    import urequests
    import ujson
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
```

**Setup**:
1. Install MicroPython on your ESP32 (see `micropython.org`).
2. Install the `urequests` library:
   ```bash
   import upip
   upip.install("micropython-urequests")
   ```
3. Upload `esp32_micropython_examples.py` to your ESP32 using `ampy`, `rshell`, or Thonny.
4. Update `SSID`, `PASSWORD`, `SERVER_URL`, and `MONGO_URI`.
5. Call the desired function (e.g., `send_create_request()`) via the MicroPython REPL.
6. Monitor console output for responses.

### Python Test Script
The project includes `test_mongodb_server.py`, which tests all operations (`create`, `insert`, `find`, `delete`, `update`) using the `requests` library. See the **Test Script** section for setup and execution instructions.

## Security Notes
- **MongoDB URI**: Contains sensitive credentials. Use HTTPS or a secure network to protect it. Consider storing the URI in a `.env` file (excluded via `.gitignore`) and loading it in your scripts.
- **Network**: Ensure the Flask server’s IP is whitelisted in your MongoDB instance (e.g., MongoDB Atlas).
- **Query Size**: For complex queries, adjust the `StaticJsonDocument` size in Arduino sketches (default is 300 bytes) or equivalent in other clients.

## Troubleshooting
- **Flask Server**:
  - Verify the MongoDB URI and ensure the server is reachable.
  - Check terminal output for errors when running `/index/api.py`.
- **ESP32 Client (Arduino)**:
  - Confirm WiFi credentials and server URL are correct.
  - Monitor Serial output (115200 baud) for error messages.
  - Ensure the `ArduinoJson` library is installed.
- **ESP32 Client (MicroPython)**:
  - Verify WiFi credentials, server URL, and `urequests` installation.
  - Check console output for errors.
  - Ensure the ESP32 has sufficient memory for complex queries.
- **Test Script**:
  - Ensure the `requests` library is installed (`pip install requests`).
  - Verify the server URL and MongoDB URI in `test_mongodb_server.py`.
  - Check for network connectivity or firewall issues if requests fail.
- **Other Clients**: Ensure the JSON payload is correctly formatted and the MongoDB URI is accessible.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue on GitHub.

## Author
- GitHub: [ishanoshada](https://github.com/ishanoshada)


**Repository Views** ![Views](https://profile-counter.glitch.me/flask-server-mongodb/count.svg)
