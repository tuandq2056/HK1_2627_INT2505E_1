from flask import Flask, jsonify, request, make_response
from uuid import uuid4

app = Flask(__name__)
DEFAULT_SIZE = 20
MAX_SIZE = 100

books = [
    {
        "id": i, 
        "title": f"Clean Code Phần {i}" if i % 2 != 0 else f"Clean Architecture Phần {i}", 
        "author": "Robert C. Martin" if i % 2 != 0 else "Orwell", 
        "published_year": 2000 + i
    } 
    for i in range(1, 26)
]
@app.get("/books", strict_slashes =False)
def list_books():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))
    except ValueError:
        return jsonify(error="page and size must be int"), 400
    page = max(page, 1)
    size = max(min(size, MAX_SIZE), 1)


    items = books
    a = request.args.get("author")
    if a: 
        items = [b for b in items if b["author"].lower() == a.lower()]
    q = (request.args.get("q") or "").strip().lower()
    if q: 
        items = [b for b in items if q in b["title"].lower() or q in b["author"].lower()]
        
    sort_by = request.args.get("sort")
    order = request.args.get("order", "asc").lower()
    if sort_by in ["title", "author", "published_year", "id"]:
        reverse = (order == "desc")
        items.sort(key=lambda x: x.get(sort_by), reverse=reverse)

    total = len(items)
    start = (page - 1) * size
    end = start + size
    items = items[start:end]
    last = (total + size - 1) // size if size > 0 else 1
    
    def build_url(p): 
        url = f"/books?page={p}&size={size}"
        if a: url += f"&author={a}"
        if q: url += f"&q={q}"
        if sort_by: url += f"&sort={sort_by}"
        if request.args.get("order"): url += f"&order={request.args.get('order')}"
        return url
        
    links = {
        "self": {"href": build_url(page)},
        "first": {"href": build_url(1)},
        "last": {"href": build_url(max(last, 1))}
    }
    if page > 1: 
        links["prev"] = {"href": build_url(page - 1)}
    if end < total: 
        links["next"] = {"href": build_url(page + 1)}
    
    body = {
        "data": items,
        "pagination": {"page": page, "size": size, "total": total, "total_pages": max(last, 1)},
        "_links": links
    }
    
    resp = make_response(jsonify(body), 200)
    resp.headers["Cache-Control"] = "public, max-age=30"
    return resp

@app.get('/books/<int:book_id>')
def get_book_by_id(book_id):
    for book in books:
        if book["id"] == book_id:
            return jsonify(book), 200
    return jsonify({"error": "not found"}), 404

@app.post('/books')
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

@app.put('/books/<int:book_id>')
def put_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "not found"}), 404
        
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid JSON"}), 400
        
    title = body.get("title")
    author = body.get("author")
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

@app.patch('/books/<int:book_id>')
def patch_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "not found"}), 404
        
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid JSON"}), 400
        
    title = body.get("title")
    author = body.get("author")
    if title is not None:
        book["title"] = title
    if author is not None :
        book["author"] = author
    if "published_year" in body or "year" in body:
        y = body.get("year", body.get("published_year"))
        if type(y) is not int or y < 1900:
            return jsonify({"error": "year must be a number >= 1900"}), 400
        book["published_year"] = y
    
    return jsonify(book), 200

@app.delete('/books/<int:book_id>')
def delete_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "not found"}), 404
    books.remove(book)
    return "", 204


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)