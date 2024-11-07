from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Konfigurasi MySQL
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'ammar_db'
}

# Fungsi untuk mengambil data terbaru dari sensor DHT
def get_latest_data():
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Query untuk mengambil data terbaru
        query = "SELECT temperature, humidity, timestamp FROM sensor_data ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(query)

        # Ambil data terbaru
        row = cursor.fetchone()
        if row:
            data = {
                'temperature': row[0],
                'humidity': row[1],
                'timestamp': row[2]
            }
        else:
            data = {
                'temperature': "No data",
                'humidity': "No data",
                'timestamp': "No data"
            }

        return data
    except mysql.connector.Error as err:
        print("Error:", err)
        return {
            'temperature': "Error",
            'humidity': "Error",
            'timestamp': "Error"
        }
    finally:
        cursor.close()
        db.close()

# Route untuk halaman utama
@app.route('/')
def index():
    data = get_latest_data()  # Ambil data terbaru dari MySQL
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
