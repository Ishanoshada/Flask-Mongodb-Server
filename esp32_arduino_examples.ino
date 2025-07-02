
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";        // Update with your WiFi SSID
const char* password = "YOUR_WIFI_PASSWORD"; // Update with your WiFi password

// Server and MongoDB details
const char* serverUrl = "http://YOUR_SERVER_IP:5000/mongodb"; // Update with your server URL
const char* mongoUri = "mongodb://user:pass@host:port/";      // Update with your MongoDB URI

void setup() {
  Serial.begin(115200);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
}

void loop() {
  // Call each operation sequentially for testing
  sendCreateRequest();
  delay(2000);
  sendInsertSingleRequest();
  delay(2000);
  sendInsertMultipleRequest();
  delay(2000);
  sendFindRequest();
  delay(2000);
  sendUpdateRequest();
  delay(2000);
  sendDeleteRequest();
  delay(10000); // Wait 10 seconds before repeating
}

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
