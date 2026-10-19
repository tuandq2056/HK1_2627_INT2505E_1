import base64
import json
from pathlib import Path
from flask import Blueprint, request, jsonify
from jsonschema import validate, ValidationError
from sqlalchemy import select, tuple_

from models import db, Book

books_bp = Blueprint("books", __name__, url_prefix="/api/v1/books")

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "book.json"
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    BOOK_SCHEMA = json.load(f)

SORT_COLS = {
    "id": Book.id,
    "price": Book.price_vnd,
    "price_vnd": Book.price_vnd,
    "title": Book.title,
}


def encode_cursor(sort_value, book_id: int) -> str:
    """Encode sort value and book id into a URL-safe base64 string."""
    payload = json.dumps({"v": sort_value, "i": book_id})
    return base64.urlsafe_b64encode(payload.encode("utf-8")).decode("utf-8").rstrip("=")


def decode_cursor(token: str) -> tuple:
    """Decode a URL-safe base64 string back into sort value and book id."""
    padding = "=" * (-len(token) % 4)
    payload = json.loads(base64.urlsafe_b64decode((token + padding).encode("utf-8")))
    return payload["v"], payload["i"]


@books_bp.get("")
def list_books():
    """
    Retrieve a paginated list of books using cursor-based pagination.
    Supports ?limit, ?sort (e.g. 'id', '-id', 'price', '-price'), and ?cursor.
    """
    limit = min(request.args.get("limit", 10, type=int), 100)
    cursor = request.args.get("cursor")
    raw_sort = request.args.get("sort", "id")

    desc = raw_sort.startswith("-")
    sort_key = raw_sort.lstrip("-")
    col = SORT_COLS.get(sort_key, Book.id)

    order_by_clause = [
        col.desc() if desc else col.asc(),
        Book.id.desc() if desc else Book.id.asc(),
    ]
    query = select(Book).order_by(*order_by_clause)

    if cursor:
        try:
            last_val, last_id = decode_cursor(cursor)
            op = "<" if desc else ">"
            condition = tuple_(col, Book.id).op(op)((last_val, last_id))
            query = query.filter(condition)
        except Exception:
            return jsonify({"error": "invalid_cursor", "message": "The provided cursor is invalid"}), 400

    rows = db.session.scalars(query.limit(limit + 1)).all()
    has_more = len(rows) > limit
    items = rows[:limit]

    next_cursor = None
    if items and has_more:
        last_item = items[-1]
        next_cursor = encode_cursor(getattr(last_item, col.key), last_item.id)

    return jsonify({
        "data": [book.to_dict() for book in items],
        "page": {
            "next_cursor": next_cursor,
            "has_more": has_more,
            "limit": limit,
        }
    }), 200


@books_bp.post("")
def create_book():
    """Create a new book with JSON Schema validation."""
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "validation_failed", "message": "Body phải là JSON hợp lệ"}), 400

    try:
        validate(instance=payload, schema=BOOK_SCHEMA)
    except ValidationError as err:
        return jsonify({
            "error": "validation_failed",
            "message": err.message,
            "field": list(err.path),
        }), 400

    isbn = payload.get("isbn")
    if isbn and Book.query.filter_by(isbn=isbn).first():
        return jsonify({
            "error": "conflict",
            "message": f"Sách với ISBN {isbn} đã tồn tại trong hệ thống",
        }), 409

    book = Book(
        title=payload["title"],
        isbn=payload.get("isbn"),
        price_vnd=payload.get("price_vnd", 0),
        stock=payload.get("stock", 0),
    )
    db.session.add(book)
    db.session.commit()

    return jsonify(book.to_dict()), 201


@books_bp.get("/<int:book_id>")
def get_book(book_id: int):
    """Retrieve book details by ID."""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "not_found", "message": f"Không tìm thấy sách với id {book_id}"}), 404

    return jsonify(book.to_dict()), 200


@books_bp.delete("/<int:book_id>")
def delete_book(book_id: int):
    """Delete a book by ID."""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "not_found", "message": f"Không tìm thấy sách với id {book_id}"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f"Đã xóa sách {book_id} thành công"}), 200
