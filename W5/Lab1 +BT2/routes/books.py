import base64
import json
from pathlib import Path
from flask import Blueprint, request, jsonify
from jsonschema import validate, ValidationError
from sqlalchemy import select, func, and_, or_

from models import db, Book

books_bp = Blueprint("books", __name__, url_prefix="/api/v1/books")

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "book.json"
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    BOOK_SCHEMA = json.load(f)

ALLOWED_SORT_FIELDS = {
    "id": ("id", Book.id),
    "price": ("price_vnd", Book.price_vnd),
    "price_vnd": ("price_vnd", Book.price_vnd),
    "title": ("title", Book.title),
    "genre": ("genre", Book.genre),
    "stock": ("stock", Book.stock),
}


def parse_multi_sort(raw_sort: str):
    """
    Parse a comma-separated sort string into structured sort definitions.
    Returns a list of tuples: (attribute_name, column_expression, is_descending).
    """
    sort_defs = []
    has_id = False

    for part in raw_sort.split(","):
        trimmed = part.strip()
        if not trimmed:
            continue
        is_desc = trimmed.startswith("-")
        field_name = trimmed.lstrip("-")

        if field_name not in ALLOWED_SORT_FIELDS:
            raise ValueError(f"Unsupported sort field: {field_name}")

        attr_name, col_expr = ALLOWED_SORT_FIELDS[field_name]
        sort_defs.append((attr_name, col_expr, is_desc))
        if field_name == "id":
            has_id = True

    if not has_id:
        sort_defs.append(("id", Book.id, False))

    return sort_defs


def encode_cursor(sort_string: str, values: list, book_id: int) -> str:
    """Encode multi-key sort state and book id into a URL-safe base64 string."""
    payload = json.dumps({"s": sort_string, "v": values, "i": book_id})
    return base64.urlsafe_b64encode(payload.encode("utf-8")).decode("utf-8").rstrip("=")


def decode_cursor(token: str) -> dict:
    """Decode a URL-safe base64 string into a dictionary containing sort state."""
    padding = "=" * (-len(token) % 4)
    return json.loads(base64.urlsafe_b64decode((token + padding).encode("utf-8")))


def build_cursor_condition(sort_defs: list, values: list, book_id: int):
    """
    Construct SQL condition for multi-key seek pagination.
    Generates lexicographical order conditions for any combination of asc/desc keys.
    """
    or_clauses = []
    prefix_equalities = []

    for idx, (attr_name, col_expr, is_desc) in enumerate(sort_defs):
        val = book_id if attr_name == "id" else values[idx]
        seek_op = col_expr < val if is_desc else col_expr > val

        if prefix_equalities:
            or_clauses.append(and_(*prefix_equalities, seek_op))
        else:
            or_clauses.append(seek_op)

        prefix_equalities.append(col_expr == val)

    return or_(*or_clauses)


@books_bp.get("")
def list_books():
    """
    Retrieve books with support for:
      - Pagination strategy: ?strategy=offset | cursor (default: cursor when cursor param is passed, else offset)
      - Filter: ?genre=...
      - Multi-key sort: ?sort=-price,title (comma-separated, prefix '-' for descending)
      - Limit: ?limit=... (1 to 100)
    """
    strategy = request.args.get("strategy")
    cursor = request.args.get("cursor")

    if not strategy:
        strategy = "cursor" if cursor else "offset"

    if strategy not in ("offset", "cursor"):
        return jsonify({
            "error": "invalid_strategy",
            "message": "Strategy must be 'offset' or 'cursor'",
        }), 400

    limit = request.args.get("limit", 10, type=int)
    if limit is None or limit < 1:
        return jsonify({"error": "invalid_limit", "message": "Limit must be a positive integer"}), 400
    limit = min(limit, 100)

    genre = request.args.get("genre")
    raw_sort = request.args.get("sort", "-id" if strategy == "cursor" else "id")

    try:
        sort_defs = parse_multi_sort(raw_sort)
    except ValueError as err:
        return jsonify({"error": "bad_sort", "message": str(err)}), 400

    order_clauses = [col.desc() if is_desc else col.asc() for _, col, is_desc in sort_defs]
    query = select(Book).order_by(*order_clauses)

    if genre:
        query = query.filter(Book.genre == genre)

    if strategy == "offset":
        offset = request.args.get("offset", 0, type=int)
        if offset is None or offset < 0:
            return jsonify({"error": "invalid_offset", "message": "Offset must be non-negative"}), 400

        count_query = select(func.count(Book.id))
        if genre:
            count_query = count_query.filter(Book.genre == genre)
        total = db.session.scalar(count_query) or 0

        rows = db.session.scalars(query.offset(offset).limit(limit)).all()

        return jsonify({
            "data": [book.to_dict() for book in rows],
            "pagination": {
                "strategy": "offset",
                "offset": offset,
                "limit": limit,
                "total": total,
                "has_next": (offset + limit) < total,
            }
        }), 200

    if cursor:
        try:
            token_data = decode_cursor(cursor)
        except Exception:
            return jsonify({"error": "invalid_cursor", "message": "Cursor token is invalid"}), 400

        if token_data.get("s") != raw_sort:
            return jsonify({
                "error": "sort_changed",
                "message": "Sort parameter has changed since the cursor was generated",
            }), 400

        condition = build_cursor_condition(sort_defs, token_data["v"], token_data["i"])
        query = query.filter(condition)

    rows = db.session.scalars(query.limit(limit + 1)).all()
    has_more = len(rows) > limit
    items = rows[:limit]

    next_cursor = None
    if items and has_more:
        last_item = items[-1]
        values = [getattr(last_item, attr_name) for attr_name, _, _ in sort_defs if attr_name != "id"]
        next_cursor = encode_cursor(raw_sort, values, last_item.id)

    return jsonify({
        "data": [book.to_dict() for book in items],
        "pagination": {
            "strategy": "cursor",
            "limit": limit,
            "next_cursor": next_cursor,
            "has_more": has_more,
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
        genre=payload.get("genre", "tech"),
        price_vnd=payload.get("price_vnd", 0),
        stock=payload.get("stock", 0),
    )
    db.session.add(book)
    db.session.commit()

    return jsonify(book.to_dict()), 201


@books_bp.get("/<int:book_id>")
def get_book(book_id: int):
    """Retrieve book details by ID."""
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"error": "not_found", "message": f"Không tìm thấy sách với id {book_id}"}), 404

    return jsonify(book.to_dict()), 200


@books_bp.delete("/<int:book_id>")
def delete_book(book_id: int):
    """Delete a book by ID."""
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"error": "not_found", "message": f"Không tìm thấy sách với id {book_id}"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f"Đã xóa sách {book_id} thành công"}), 200
