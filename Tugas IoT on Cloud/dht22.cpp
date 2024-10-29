#include "DHT.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <HTTPClient.h>

#define DHTPIN 27           // Pin data terhubung ke pin 27
#define DHTTYPE DHT22       // Tipe sensor DHT22

const char* ssid = "Wokwi-GUEST";        // Nama WiFi
const char* password = "";               // Password WiFi
const char* serverName = "YOUR_SERVER_NAME"; // URL server Flask (HTTP)

// Inisialisasi objek sensor DHT dan LCD
DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);  // Alamat I2C LCD

void setup() {
  Serial.begin(9600);
  dht.begin();
  Wire.begin(19, 18);      // Atur pin SDA dan SCL jika tidak menggunakan pin default
  lcd.begin(16, 2);        // Menginisialisasi LCD 16x2
  lcd.backlight();         // Nyalakan lampu latar LCD
  
  // Menghubungkan ke WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Connected!");
}

void loop() {
  // Baca data dari sensor DHT
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Cek apakah data sensor valid
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Error reading");
    lcd.setCursor(0, 1);
    lcd.print("DHT sensor!");
    delay(5000);
    return;
  }

  // Tampilkan data di Serial Monitor dan LCD
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print("%  ");
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println("°C");

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Humidity: ");
  lcd.print(humidity);
  lcd.print("%");
  
  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
  lcd.print(temperature);
  lcd.print(" C");

  // Mengirim data ke server Flask
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);          // Menghubungkan ke server Flask
    http.addHeader("Content-Type", "application/json"); // Set header

    // Membuat JSON dengan data suhu dan kelembaban
    String postData = "{\"temperature\":" + String(temperature) + ",\"humidity\":" + String(humidity) + "}";
    Serial.print("Sending data: ");
    Serial.println(postData);

    int httpResponseCode = http.POST(postData);
    
    // Menangani respons server
    if (httpResponseCode > 0) {
      Serial.print("HTTP Response Code: ");
      Serial.println(httpResponseCode);
      if (httpResponseCode == 200) {
        String response = http.getString();
        Serial.println("Data sent successfully!");
        Serial.println("Response: " + response);
      } 
      else if (httpResponseCode == 307) {  // 307 Temporary Redirect
        String redirectedURL = http.getLocation();  // Dapatkan URL pengalihan dari header "Location"
        Serial.print("Redirected to: ");
        Serial.println(redirectedURL);

        http.end();  // Akhiri sesi HTTP saat ini

        // Membuat ulang HTTPClient dan mencoba mengirim permintaan ke URL pengalihan
        http.begin(redirectedURL);
        http.addHeader("Content-Type", "application/json");
        httpResponseCode = http.POST(postData);

        if (httpResponseCode == 200) {
          Serial.println("Data sent after redirect!");
          String response = http.getString();
          Serial.println("Response: " + response);
        } else {
          Serial.print("Error after redirect. HTTP Response Code: ");
          Serial.println(httpResponseCode);
        }
      } else {
        Serial.print("Unexpected HTTP response code: ");
        Serial.println(httpResponseCode);
      }
    } else {
      Serial.print("Error sending data to server. HTTP Response Code: ");
      Serial.println(httpResponseCode);
    }
    
    http.end();
  } else {
    Serial.println("WiFi not connected");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("WiFi disconnected");
  }

  delay(5000);  // Delay 5 detik untuk pembacaan berikutnya
}
