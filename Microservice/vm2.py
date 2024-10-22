from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration to connect to MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/produkdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_produk = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    stok = db.Column(db.Integer, nullable=False)

@app.route('/produk', methods=['GET'])
def get_produk():
    products = Product.query.all()
    output = []
    for product in products:
        product_data = {
            'id': product.id,
            'nama_produk': product.nama_produk,
            'harga': product.harga,
            'stok': product.stok
        }
        output.append(product_data)

    return jsonify(output)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables within application context
    app.run(host='0.0.0.0', port=5002)
