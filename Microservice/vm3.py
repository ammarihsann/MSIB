from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL untuk VM1 dan VM2
VM1_URL_STATUS = 'http://127.0.0.1:5001/status'  # URL untuk status VM1
VM1_URL = 'http://127.0.0.1:5001/ongkir'          # URL untuk ongkir di VM1
VM2_URL = 'http://127.0.0.1:5002/produk'           # URL untuk produk di VM2

@app.route('/ongkir', methods=['POST'])
def get_ongkir():
    """
    Endpoint untuk menghitung ongkos kirim.
    Diterima dalam format JSON dengan data asal, tujuan, dan berat.
    """
    data = request.json  # Mengambil data JSON dari permintaan
    response = requests.post(VM1_URL, json=data)  # Mengirimkan permintaan ke VM1
    return jsonify(response.json())  # Mengembalikan respons dari VM1

@app.route('/produk', methods=['GET'])
def get_produk():
    """
    Endpoint untuk mendapatkan daftar produk dari VM2.
    """
    response = requests.get(VM2_URL)  # Mengambil data produk dari VM2
    return jsonify(response.json())  # Mengembalikan daftar produk

@app.route('/status', methods=['GET'])
def get_status():
    """
    Endpoint untuk mendapatkan status dari VM1.
    """
    response = requests.get(VM1_URL_STATUS)  # Mengambil status dari VM1
    return jsonify(response.json())  # Mengembalikan status dari VM1

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)  # Menjalankan aplikasi Flask
