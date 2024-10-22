from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 'YOUR_API_KEY'

# Endpoint vm1 menggunakan metode POST
@app.route('/ongkir', methods=['POST'])
def hitung_ongkir():
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')
    weight = data.get('weight')

    # Memastikan semua parameter ada
    if not all([origin, destination, weight]):
        return jsonify({"error": "Please provide origin, destination, and weight"}), 400

    headers = {
        'key': API_KEY
    }

    # Memanggil API RajaOngkir
    response = requests.post(
        'https://api.rajaongkir.com/starter/cost',
        headers=headers,
        data={
            'origin': origin,
            'destination': destination,
            'weight': weight,
            'courier': 'jne'  # Anda dapat mengganti kurir sesuai kebutuhan
        }
    )

    return jsonify(response.json())

# Endpoint vm2 menggunakan metode GET
@app.route('/status', methods=['GET'])
def get_status():
    # Menyediakan status atau informasi lain
    return jsonify({"status": "API is running"})

# Endpoint vm3 menggunakan metode GET
@app.route('/info', methods=['GET'])
def get_info():
    # Menyediakan informasi lebih lanjut
    return jsonify({"info": "This is a sample API to calculate shipping costs."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
