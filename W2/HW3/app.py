from flask import Flask, jsonify, request, make_response, g
import sqlite3
import hashlib

app = Flask(__name__)
DEFAULT_SIZE = 20
MAX_SIZE = 100
DATABASE = "app.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def make_etag(title: str, author: str, published_year: int) -> str:
    """Sinh ETag bằng cách hash nội dung cuốn sách."""
    raw = f"{title}-{author}-{published_year}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()

def init_db():
    with app.app_context():
        db = get_db()
        # Bảng books (có cột etag)
        db.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                published_year INTEGER,
                etag TEXT
            )
        ''')
        # Migration: thêm cột etag nếu chưa có (cho DB cũ)
        try:
            db.execute("ALTER TABLE books ADD COLUMN etag TEXT")
        except sqlite3.OperationalError:
            pass  # Cột đã tồn tại, bỏ qua
        # Cập nhật etag cho các record cũ chưa có
        rows = db.execute("SELECT id, title, author, published_year FROM books WHERE etag IS NULL").fetchall()
        for row in rows:
            etag = make_etag(row["title"], row["author"], row["published_year"])
            db.execute("UPDATE books SET etag = ? WHERE id = ?", (etag, row["id"]))
        # Bảng orders
        db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                total_price REAL NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        db.commit()

@app.get("/books", strict_slashes=False)
def list_books():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))
    except ValueError:
        return jsonify(error="page and size must be int"), 400
    page = max(page, 1)
    size = max(min(size, MAX_SIZE), 1)

    conditions = []
    params = []
    
    a = request.args.get("author")
    if a: 
        conditions.append("LOWER(author) = ?")
        params.append(a.lower())
        
    q = (request.args.get("q") or "").strip().lower()
    if q: 
        conditions.append("(LOWER(title) LIKE ? OR LOWER(author) LIKE ?)")
        params.extend([f"%{q}%", f"%{q}%"])
        
    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    
    db = get_db()
    total = db.execute(f"SELECT COUNT(*) FROM books {where_clause}", params).fetchone()[0]

    query = f"SELECT * FROM books {where_clause}"
    
    sort_by = request.args.get("sort")
    order = request.args.get("order", "asc").lower()
    if sort_by in ["title", "author", "published_year", "id"]:
        direction = "DESC" if order == "desc" else "ASC"
        query += f" ORDER BY {sort_by} {direction}"

    start = (page - 1) * size
    query += " LIMIT ? OFFSET ?"
    params.extend([size, start])
    end = start + size
    
    rows = db.execute(query, params).fetchall()
    items = [dict(row) for row in rows]
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
    row = get_db().execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if not row:
        return jsonify({"error": "not found"}), 404
    
    etag = row["etag"]
    # Conditional request: trả 304 nếu client đã có bản mới nhất
    if request.headers.get("If-None-Match") == etag:
        resp = make_response("", 304)
        resp.headers["ETag"] = etag
        return resp
    
    body = {k: row[k] for k in row.keys() if k != "etag"}
    resp = make_response(jsonify(body), 200)
    resp.headers["ETag"] = etag
    resp.headers["Cache-Control"] = "private, must-revalidate"
    return resp

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
        
    db = get_db()
    etag = make_etag(title, author, published_year)
    cursor = db.execute(
        "INSERT INTO books (title, author, published_year, etag) VALUES (?, ?, ?, ?)",
        (title, author, published_year, etag)
    )
    db.commit()
    new_id = cursor.lastrowid
    
    resp = make_response(jsonify({
        "id": new_id,
        "title": title,
        "author": author,
        "published_year": published_year
    }), 201)
    resp.headers["Location"] = f"/books/{new_id}"
    resp.headers["ETag"] = etag
    return resp

@app.put('/books/<int:book_id>')
def put_book(book_id):
    db = get_db()
    row = db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if not row:
        return jsonify({"error": "not found"}), 404
        
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid JSON"}), 400
        
    title = body.get("title")
    author = body.get("author")
    if not title or not author:
        return jsonify({"error": "title+author required"}), 400
        
    published_year = body.get("published_year", body.get("year", row["published_year"]))
    if type(published_year) is not int or published_year < 1900:
        return jsonify({"error": "year must be a number >= 1900"}), 400
        
    etag = make_etag(title, author, published_year)
    db.execute(
        "UPDATE books SET title = ?, author = ?, published_year = ?, etag = ? WHERE id = ?",
        (title, author, published_year, etag, book_id)
    )
    db.commit()
    
    resp = make_response(jsonify({
        "id": book_id,
        "title": title,
        "author": author,
        "published_year": published_year
    }), 200)
    resp.headers["ETag"] = etag
    return resp

@app.patch('/books/<int:book_id>')
def patch_book(book_id):
    db = get_db()
    row = db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if not row:
        return jsonify({"error": "not found"}), 404
        
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid JSON"}), 400
        
    title = body.get("title", row["title"])
    author = body.get("author", row["author"])
    published_year = body.get("published_year", body.get("year", row["published_year"]))
    
    if type(published_year) is not int or published_year < 1900:
        return jsonify({"error": "year must be a number >= 1900"}), 400
        
    etag = make_etag(title, author, published_year)
    db.execute(
        "UPDATE books SET title = ?, author = ?, published_year = ?, etag = ? WHERE id = ?",
        (title, author, published_year, etag, book_id)
    )
    db.commit()
    
    resp = make_response(jsonify({
        "id": book_id,
        "title": title,
        "author": author,
        "published_year": published_year
    }), 200)
    resp.headers["ETag"] = etag
    return resp

@app.delete('/books/<int:book_id>')
def delete_book(book_id):
    db = get_db()
    row = db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if not row:
        return jsonify({"error": "not found"}), 404
        
    db.execute("DELETE FROM books WHERE id = ?", (book_id,))
    db.commit()
    return "", 204

@app.get('/orders/<int:oid>')
def get_order_by_id(oid):
    row = get_db().execute("SELECT * FROM orders WHERE id = ?", (oid,)).fetchone()
    if row:
        return jsonify(dict(row)), 200
    return jsonify({"error": "not found"}), 404

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=True)