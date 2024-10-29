from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Variabel untuk menyimpan data terakhir
sensor_data = {
    "temperature": None,
    "humidity": None
}

# Endpoint untuk menerima data suhu dan kelembaban
@app.route('/sensor', methods=['POST'])
def receive_sensor_data():
    global sensor_data
    data = request.get_json()
    
    # Menyimpan data suhu dan kelembaban
    sensor_data['temperature'] = data.get('temperature')
    sensor_data['humidity'] = data.get('humidity')
    
    print(f"Received data - Temperature: {sensor_data['temperature']}°C, Humidity: {sensor_data['humidity']}%")
    return jsonify({"status": "success", "data": sensor_data}), 200


# Endpoint untuk mendapatkan data terakhir
@app.route('/data', methods=['GET'])
def get_sensor_data():
    return jsonify(sensor_data), 200

# Endpoint untuk menyajikan index.html dari direktori utama
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
