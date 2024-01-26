from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(120), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Define Book schema
class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author', 'isbn', 'price', 'quantity')

book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Create a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(**data)
    db.session.add(new_book)
    db.session.commit()
    return book_schema.jsonify(new_book)

# Retrieve all books
@app.route('/books', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    return books_schema.jsonify(all_books)

# Retrieve a specific book by ISBN
@app.route('/books/<isbn>', methods=['GET'])
def get_book(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    return book_schema.jsonify(book)

# Update book details
@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    data = request.json

    book.title = data['title']
    book.author = data['author']
    book.isbn = data['isbn']
    book.price = data['price']
    book.quantity = data['quantity']

    db.session.commit()
    return book_schema.jsonify(book)

# Delete a book
@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return book_schema.jsonify(book)

if _name_ == '_main_':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
