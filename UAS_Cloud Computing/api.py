from flask import Flask, request, jsonify
from db_config import db_config
import mysql.connector
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
SECRET_KEY = "your_secret_key"

# Fungsi untuk koneksi ke MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Dekorator untuk memeriksa token JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing"}), 403

        try:
            decoded = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
            if decoded['role'] != 'admin':
                return jsonify({"message": "Permission denied"}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 403

        return f(*args, **kwargs)
    return decorated

# Endpoint untuk login dan mendapatkan token JWT
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Contoh validasi sederhana (dapat diganti dengan validasi dari database)
    if username == 'admin' and password == 'adminpassword':
        token = jwt.encode(
            {
                'username': username,
                'role': 'admin',
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            SECRET_KEY,
            algorithm='HS256'
        )
        return jsonify({'token': token})

    return jsonify({"message": "Invalid credentials"}), 401

# Endpoint GET untuk mengambil semua data sensor (tidak memerlukan token)
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

# Endpoint POST untuk menambahkan data sensor baru (hanya untuk admin)
@app.route('/api/sensors', methods=['POST'])
@token_required
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

# Endpoint PUT untuk memperbarui data sensor berdasarkan ID (hanya untuk admin)
@app.route('/api/sensors/<int:id>', methods=['PUT'])
@token_required
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

if __name__ == '__main__':
    app.run(debug=True)
