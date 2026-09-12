from flask import Flask, jsonify, request
from uuid import uuid4
app = Flask(__name__)
books = list()
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

@app.route('/books', methods=['POST'])
def create_book():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Invalid JSON"}), 400
    book = {
        "id": str(uuid4()),
        "title": body.get("title"),
        "author": body.get("author"),
        "published_year": body.get("published_year")
    }
    books.append(book)
    return {"message": "Book created successfully", "book": book}, 201

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)