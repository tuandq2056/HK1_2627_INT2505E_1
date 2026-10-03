from flask import Blueprint, jsonify, request, make_response
from db.connection import get_db
from services import order_service
from config import DEFAULT_SIZE

# Khởi tạo Blueprint chứa các API về orders
orders_bp = Blueprint("orders", __name__)

@orders_bp.get("")
def list_orders():
    """Lấy danh sách đơn hàng (có phân trang, filter theo status / customer_name)"""
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))
    except ValueError:
        return jsonify({"error": "page và size phải là số nguyên"}), 400

    filters = {
        "status": request.args.get("status"),
        "customer_name": request.args.get("customer_name")
    }

    db = get_db()
    result = order_service.get_orders_list(db, page, size, filters)
    return jsonify(result), 200

@orders_bp.get("/<int:order_id>")
def get_order(order_id):
    """Lấy chi tiết 1 đơn hàng"""
    db = get_db()
    order = order_service.get_order_detail(db, order_id)
    return jsonify(order), 200

@orders_bp.post("")
def create_order():
    """Tạo đơn hàng mới"""
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400

    db = get_db()
    new_order = order_service.create_order(db, payload)

    resp = make_response(jsonify(new_order), 201)
    resp.headers["Location"] = f"/orders/{new_order['id']}"
    return resp

@orders_bp.put("/<int:order_id>")
def update_order(order_id):
    """Cập nhật đơn hàng"""
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400

    db = get_db()
    updated_order = order_service.update_order(db, order_id, payload)
    return jsonify(updated_order), 200

@orders_bp.delete("/<int:order_id>")
def delete_order(order_id):
    """Xóa đơn hàng"""
    db = get_db()
    order_service.delete_order(db, order_id)
    return "", 204
