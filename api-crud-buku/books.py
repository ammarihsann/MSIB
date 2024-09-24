from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfigurasi database MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/buku'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model Buku untuk ORM
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    penulis = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'penulis': self.penulis
        }

# Model Users untuk ORM
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username
        }

# Mendapatkan semua buku (GET)
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify({'books': [book.to_dict() for book in books]})

# Mendapatkan buku berdasarkan id (GET)
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        abort(404)
    return jsonify({'book': book.to_dict()})

# Menambahkan buku baru (POST)
@app.route('/books', methods=['POST'])
def create_book():
    if not request.json or not 'title' in request.json or not 'penulis' in request.json:
        abort(400)
    new_book = Book(
        title=request.json['title'],
        penulis=request.json['penulis']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'book': new_book.to_dict()}), 201

# Mendapatkan semua pengguna (GET)
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'users': [user.to_dict() for user in users]})

# Mendapatkan pengguna berdasarkan id (GET)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    return jsonify({'user': user.to_dict()})

# Menambahkan pengguna baru (POST)
@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or not 'email' in request.json or not 'username' in request.json:
        abort(400)
    new_user = User(
        email=request.json['email'],
        username=request.json['username']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'user': new_user.to_dict()}), 201

if __name__ == '__main__':
    # Membuat tabel jika belum ada
    with app.app_context():
        db.create_all()

    app.run(debug=True)
