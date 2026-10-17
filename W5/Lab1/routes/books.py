import json
from pathlib import Path
from flask import Blueprint, request, jsonify
from jsonschema import validate, ValidationError

from models import db, Book

books_bp = Blueprint("books", __name__, url_prefix="/api/v1/books")

# Load JSON Schema dùng để validate dữ liệu đầu vào (Slide 15)
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "book.json"
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    BOOK_SCHEMA = json.load(f)


@books_bp.get("")
def list_books():
    """Lấy danh sách tất cả sách (format theo API Resource Representation)"""
    books = Book.query.all()
    return jsonify({
        "data": [book.to_dict() for book in books],
        "total": len(books)
    }), 200


@books_bp.post("")
def create_book():
    """
    Tạo sách mới với validation bằng JSON Schema (Mục tiêu 2 của Lab 1 - Slide 15)
    - Nếu body không hợp lệ -> trả về 400 Bad Request kèm lý do
    - Nếu hợp lệ -> lưu DB và trả về 201 Created
    """
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "validation_failed", "message": "Body phải là JSON hợp lệ"}), 400

    # 1. Validate payload theo JSON Schema
    try:
        validate(instance=payload, schema=BOOK_SCHEMA)
    except ValidationError as err:
        return jsonify({
            "error": "validation_failed",
            "message": err.message,
            "field": list(err.path)
        }), 400

    # 2. Kiểm tra trùng ISBN nếu có
    isbn = payload.get("isbn")
    if isbn and Book.query.filter_by(isbn=isbn).first():
        return jsonify({
            "error": "conflict",
            "message": f"Sách với ISBN {isbn} đã tồn tại trong hệ thống"
        }), 409

    # 3. Tạo và lưu Book vào Database
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
    """Lấy chi tiết một cuốn sách theo ID"""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "not_found", "message": f"Không tìm thấy sách với id {book_id}"}), 404

    return jsonify(book.to_dict()), 200


@books_bp.delete("/<int:book_id>")
def delete_book(book_id: int):
    """Xóa một cuốn sách"""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "not_found", "message": f"Không tìm thấy sách với id {book_id}"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f"Đã xóa sách {book_id} thành công"}), 200
