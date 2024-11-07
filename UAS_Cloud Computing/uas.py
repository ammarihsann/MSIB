from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Konfigurasi MySQL
db_config = {
    'user': 'root',            # Ganti dengan username MySQL Anda
    'password': '',             # Ganti dengan password MySQL Anda
    'host': 'localhost',
    'database': 'ammar_db'
}

# Fungsi untuk koneksi ke MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Endpoint GET untuk mengambil semua data sensor
@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM sensor_data")
    rows = cursor.fetchall()

    # Format hasil sebagai list of dictionaries
    data = []
    for row in rows:
        data.append({
            'id': row[0],
            'temperature': row[1],
            'humidity': row[2],
            'timestamp': row[3]
        })

    cursor.close()
    db.close()

    return jsonify(data)

# Endpoint POST untuk menambahkan data sensor baru
@app.route('/api/sensors', methods=['POST'])
def add_sensor():
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')

    db = get_db_connection()
    cursor = db.cursor()

    # Query untuk menambahkan data baru
    query = "INSERT INTO sensor_data (temperature, humidity) VALUES (%s, %s)"
    cursor.execute(query, (temperature, humidity))
    db.commit()

    cursor.close()
    db.close()

    return jsonify({"message": "Data added successfully"}), 201

# Endpoint PUT untuk memperbarui data sensor berdasarkan ID
@app.route('/api/sensors/<int:id>', methods=['PUT'])
def update_sensor(id):
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')

    db = get_db_connection()
    cursor = db.cursor()

    # Query untuk memperbarui data berdasarkan ID
    query = "UPDATE sensor_data SET temperature = %s, humidity = %s WHERE id = %s"
    cursor.execute(query, (temperature, humidity, id))
    db.commit()

    cursor.close()
    db.close()

    return jsonify({"message": "Data updated successfully"})

# Jalankan aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True)
