from flask import Blueprint, jsonify, request, make_response
from db.connection import get_db
from services import book_service
from config import DEFAULT_SIZE

# Khởi tạo Blueprint (như một mini-app chứa các API về books)
books_bp = Blueprint("books", __name__)

@books_bp.get("")
def list_books():
    """Lấy danh sách sách (hỗ trợ cả cursor pagination và offset pagination)"""
    cursor = request.args.get("cursor")
    page_param = request.args.get("page")

    try:
        size = int(request.args.get("size") or request.args.get("limit") or DEFAULT_SIZE)
        page = int(page_param) if page_param is not None else 1
    except ValueError:
        return jsonify({"error": "page và size phải là số nguyên"}), 400

    filters = {
        "author": request.args.get("author"),
        "published_year": request.args.get("published_year"),
        "q": request.args.get("q")
    }

    sort_param = request.args.get("sort")
    order = request.args.get("order", "asc")
    if sort_param and sort_param.startswith("-"):
        sort_by = sort_param[1:]
        order = "desc"
    else:
        sort_by = sort_param or "id"

    fields_param = request.args.get("fields") or request.args.get("fields[books]")
    fields = [f.strip() for f in fields_param.split(",") if f.strip()] if fields_param else None

    db = get_db()

    # 2. Xử lý phân trang
    if cursor is not None:
        result = book_service.get_books_cursor(
            db, limit=size, cursor=cursor, filters=filters,
            sort_by=sort_by, order=order, fields=fields
        )
    else:
        result = book_service.get_books_list(
            db, page=page, size=size, filters=filters,
            sort_by=sort_by, order=order, fields=fields
        )

    resp = make_response(jsonify(result), 200)
    resp.headers["Cache-Control"] = "public, max-age=30"
    return resp

@books_bp.get("/<int:book_id>")
def get_book(book_id):
    """Lấy chi tiết 1 cuốn sách, có hỗ trợ Conditional Request (ETag) và Sparse Fieldsets"""
    db = get_db()
    book_dict, etag = book_service.get_book_detail(db, book_id)

    # Check ETag (If-None-Match)
    if request.headers.get("If-None-Match") == etag:
        resp = make_response("", 304)
        resp.headers["ETag"] = etag
        return resp

    fields_param = request.args.get("fields") or request.args.get("fields[books]")
    if fields_param:
        fields = [f.strip() for f in fields_param.split(",") if f.strip()]
        book_dict = {k: book_dict[k] for k in fields if k in book_dict}

    resp = make_response(jsonify(book_dict), 200)
    resp.headers["ETag"] = etag
    resp.headers["Cache-Control"] = "private, must-revalidate"
    return resp

@books_bp.post("")
def create_book():
    """Tạo sách mới"""
    # 1. NHẬN HTTP
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400
        
    # 2. GỌI SERVICE
    db = get_db()
    # TRUYỀN VÀO: db, payload (dict)
    # NHẬN RA: new_book (dict), etag (string)
    # (Nếu thiếu title/author, Service sẽ throw ValidationError, errorhandler sẽ tự bắt)
    new_book, etag = book_service.create_book(db, payload)
    
    # 3. TRẢ HTTP
    resp = make_response(jsonify(new_book), 201)
    resp.headers["Location"] = f"/books/{new_book['id']}"
    resp.headers["ETag"] = etag
    return resp

@books_bp.put("/<int:book_id>")
def update_book(book_id):
    """Cập nhật sách (Yêu cầu gửi If-Match)"""
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400
        
    if_match_etag = request.headers.get("If-Match")
    if not if_match_etag:
        return jsonify({"error": "Thiếu Header If-Match"}), 428 # Precondition Required
        
    db = get_db()
    # TRUYỀN VÀO: db, book_id, payload, if_match_etag
    updated_book, new_etag = book_service.update_book(db, book_id, payload, if_match_etag)
    
    resp = make_response(jsonify(updated_book), 200)
    resp.headers["ETag"] = new_etag
    return resp

@books_bp.delete("/<int:book_id>")
def delete_book(book_id):
    """Xóa sách"""
    db = get_db()
    book_service.delete_book(db, book_id)
    return "", 204
