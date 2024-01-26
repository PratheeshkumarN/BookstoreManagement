# BookstoreManagement
# Install necessary packages
# pip install flask flask_sqlalchemy flask_marshmallow

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
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

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

Navigate to the project directory:

bash
cd bookstore-management
Create a virtual environment:

bash
python -m venv venv
Activate the virtual environment:

On Windows:

bash
.\venv\Scripts\activate
On Unix or MacOS:

bash
source venv/bin/activate
Install dependencies:

bash
pip install -r requirements.txt
Usage
Run the Flask application:

bash
python bookmanagement.py
The application will run on http://127.0.0.1:5000/.

Endpoints
POST /books: Add a new book.
GET /books: Retrieve all books.
GET /books/<isbn>: Retrieve a specific book by ISBN.
PUT /books/<id>: Update book details.
DELETE /books/<id>: Delete a book.
For detailed API documentation and usage examples, refer to API Documentation.

Testing
To test the API endpoints, you can use tools like Postman or make HTTP requests using a tool like curl.

bash
# Example: Add a new book
curl -X POST -H "Content-Type: application/json" -d '{"title":"Sample Book","author":"Author Name","isbn":"1234567890123","price":19.99,"quantity":10}' http://127.0.0.1:5000/books
Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.
