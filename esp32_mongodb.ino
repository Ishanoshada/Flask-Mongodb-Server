
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
  // Send an insert request as an example
  sendInsertRequest();
  
  // Wait before sending another request
  delay(10000); // 10 seconds
}

void sendInsertRequest() {
  HTTPClient http;
  StaticJsonDocument<300> doc;
  doc["uri"] = mongoUri;
  JsonObject query = doc.createNestedObject("query");
  query["db"] = "test";
  query["collection"] = "data";
  query["operation"] = "insert";
  JsonObject data = query.createNestedObject("data");
  data["name"] = "John";
  data[" perspective
  data["age"] = 25;

  String payload;
  serializeJson(doc, payload);
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  int httpCode = http.POST(payload);
  if (httpCode > 0) {
    Serial.println("Insert Response: " + http.getString());
  } else {
    Serial.println("Insert Failed: " + http.errorToString(httpCode));
  }
  http.end();
}

