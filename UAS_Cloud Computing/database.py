import json
import mysql.connector
import paho.mqtt.client as mqtt

# Konfigurasi MySQL
db_config = {
    'user': 'root',            # Ganti dengan username MySQL Anda
    'password': '',     # Ganti dengan password MySQL Anda
    'host': 'localhost',
    'database': 'ammar_db'
}

# Konfigurasi MQTT
mqtt_broker = "test.mosquitto.org"  # Alamat broker MQTT
mqtt_port = 1883
mqtt_topic = "sensor/data"

# Fungsi untuk menyimpan data ke MySQL
def save_to_mysql(temperature, humidity):
    try:
        # Koneksi ke MySQL
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Query untuk menyimpan data
        query = "INSERT INTO sensor_data (temperature, humidity) VALUES (%s, %s)"
        cursor.execute(query, (temperature, humidity))
        db.commit()

        print("Data saved to MySQL:", temperature, humidity)
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        db.close()

# Callback ketika terhubung ke broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker!" if rc == 0 else "Failed to connect, return code %d\n", rc)
    client.subscribe(mqtt_topic)

# Callback ketika pesan diterima
def on_message(client, userdata, msg):
    print("Message received from MQTT:", msg.payload.decode())
    try:
        # Parsing JSON data
        data = json.loads(msg.payload.decode())
        temperature = data["temperature"]
        humidity = data["humidity"]

        # Simpan data ke MySQL
        save_to_mysql(temperature, humidity)
    except json.JSONDecodeError:
        print("Failed to decode JSON")

# Inisialisasi client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Menghubungkan ke broker MQTT
client.connect(mqtt_broker, mqtt_port, 60)

# Jalankan client MQTT
client.loop_forever()
