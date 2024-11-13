#include <WiFi.h>  
#include <PubSubClient.h>
#include <DHTesp.h>

const int DHT_PIN = 27;  
DHTesp dht; 
const char* ssid = "Wokwi-GUEST"; // WiFi SSID 
const char* password = "";
const char* mqtt_server = "test.mosquitto.org"; // Mosquitto server URL

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;

void setup_wifi() { 
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA); 
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) { 
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) { 
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) { 
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void reconnect() { 
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("Connected");
      client.publish("sensor/data", "Welcome");
      client.subscribe("sensor/data"); 
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  pinMode(2, OUTPUT);     
  Serial.begin(115200);
  setup_wifi(); 
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback); 
  dht.setup(DHT_PIN, DHTesp::DHT22);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 2000) { // Publish data every 2 seconds
    lastMsg = now;
    TempAndHumidity data = dht.getTempAndHumidity();

    String jsonPayload = "{\"temperature\":" + String(data.temperature, 2) + 
                         ", \"humidity\":" + String(data.humidity, 1) + "}";

    client.publish("sensor/data", jsonPayload.c_str()); // Publish JSON payload to /ThinkIOT/data

    Serial.print("JSON Payload: ");
    Serial.println(jsonPayload);
  }
}
