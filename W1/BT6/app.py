from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)

# Dùng ID kiểu số nguyên để giống hệt bài test
books = [
    {"id": 1, "title": "Dế Mèn Phiêu Lưu Ký", "author": "Tô Hoài", "published_year": 1941},
    {"id": 2, "title": "Lập Trình Python Cơ Bản", "author": "Guido van Rossum", "published_year": 2020},
    {"id": 3, "title": "Flask Web Development", "author": "Miguel Grinberg", "published_year": 2018},
    {"id": 4, "title": "Học Python Nâng Cao", "author": "Luciano Ramalho", "published_year": 2022},
    {"id": 5, "title": "Tắt Đèn", "author": "Ngô Tất Tố", "published_year": 1939}
]

@app.route('/books', methods=['GET'])
def list_books():
    limit = int(request.args.get("limit", 20))
    offset = int(request.args.get("offset", 0))
    q = request.args.get("q", "").strip().lower()
    sort = request.args.get("sort")
    
    items = books
    if q:
        items = [b for b in books if q in b["title"].lower()]
        
    if sort == "title":
        items = sorted(items, key=lambda x: x["title"])
        
    items = items[offset : offset + limit]

    return jsonify(items), 200

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    for book in books:
        if book["id"] == book_id:
            return jsonify(book), 200
    return jsonify({"error": "not found"}), 404

@app.route('/books', methods=['POST'])
def create_book():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid JSON"}), 400
        
    title = body.get("title")
    author = body.get("author")
    if not title or not author:
        return jsonify({"error": "title+author required"}), 400
        
    published_year = body.get("published_year", body.get("year"))
    if published_year is None or type(published_year) is not int or published_year < 1900:
        return jsonify({"error": "year must be a number >= 1900"}), 400
        
    new_id = 1 if not books else max(b["id"] for b in books) + 1
    book = {
        "id": new_id,
        "title": title,
        "author": author,
        "published_year": published_year
    }
    books.append(book)
    return jsonify(book), 201, {'Location': f'/books/{new_id}'}

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "not found"}), 404
        
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid JSON"}), 400
        
    title = body.get("title", book["title"])
    author = body.get("author", book["author"])
    if not title or not author:
        return jsonify({"error": "title+author required"}), 400
    
    book["title"] = title
    book["author"] = author
        
    if "published_year" in body or "year" in body:
        y = body.get("year", body.get("published_year"))
        if type(y) is not int or y < 1900:
            return jsonify({"error": "year must be a number >= 1900"}), 400
        book["published_year"] = y
    
    return jsonify(book), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "not found"}), 404
    books.remove(book)
    return "", 204

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)