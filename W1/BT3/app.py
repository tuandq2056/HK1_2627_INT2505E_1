from flask import Flask, jsonify, request
from uuid import uuid4
app = Flask(__name__)
from uuid import uuid4

books = [
    {
        "id": str(uuid4()),
        "title": "Dế Mèn Phiêu Lưu Ký",
        "author": "Tô Hoài",
        "published_year": 1941
    },
    {
        "id": str(uuid4()),
        "title": "Lập Trình Python Cơ Bản",
        "author": "Guido van Rossum",
        "published_year": 2020
    },
    {
        "id": str(uuid4()),
        "title": "Flask Web Development",
        "author": "Miguel Grinberg",
        "published_year": 2018
    },
    {
        "id": str(uuid4()),
        "title": "Học Python Nâng Cao",
        "author": "Luciano Ramalho",
        "published_year": 2022
    },
    {
        "id": str(uuid4()),
        "title": "Tắt Đèn",
        "author": "Ngô Tất Tố",
        "published_year": 1939
    }
]


@app.route('/books', methods=['GET'])
def list_books():
    limit = int(request.args.get("limit", 20))
    offset = int(request.args.get("offset", 0))
    q = request.args.get("q", "").strip().lower()
    items = [b for b in books if q in b["title"].lower()]
    items = items[offset : offset + limit]

    return jsonify({"items": items}), 200

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

@app.route('/books/<string:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    for book in books:
        if book["id"] == book_id:
            return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

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