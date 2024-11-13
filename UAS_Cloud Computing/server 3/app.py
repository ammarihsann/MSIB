from flask import Flask, render_template
from flask_socketio import SocketIO
import requests
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Endpoint API untuk mengambil data terbaru
API_URL = 'http://127.0.0.1:5000/api/sensors'

# Fungsi untuk mengambil data terbaru dari endpoint API
def get_latest_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data_list = response.json()

        if data_list:
            latest_data = data_list[-1]
            return {
                'temperature': latest_data['temperature'],
                'humidity': latest_data['humidity'],
                'timestamp': latest_data['timestamp']
            }
        else:
            return {
                'temperature': "No data",
                'humidity': "No data",
                'timestamp': "No data"
            }
    except requests.RequestException as err:
        print("Error:", err)
        return {
            'temperature': "Error",
            'humidity': "Error",
            'timestamp': "Error"
        }

# Route untuk halaman utama
@app.route('/')
def index():
    data = get_latest_data()
    return render_template('index.html', data=data)

# Fungsi untuk mengirim data terbaru secara berkala ke klien melalui WebSocket
def send_data():
    while True:
        data = get_latest_data()
        socketio.emit('update_data', data)
        time.sleep(2)  # Interval untuk pengiriman data

@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(target=send_data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
