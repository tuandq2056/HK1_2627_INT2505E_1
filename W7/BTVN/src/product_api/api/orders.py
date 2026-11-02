from flask import Blueprint, request
from sqlalchemy import func
from sqlalchemy.orm import joinedload, selectinload

from ..errors import ApiError, Conflict, NotFound
from ..extensions import db
from ..models import Order, OrderItem, Product
from ..schemas import OrderIn, OrderItemIn, OrderOut
from ..services.inventory import release_stock, reserve_stock

orders_bp = Blueprint("orders", __name__, url_prefix="/api/v1/orders")

order_out = OrderOut()

# Eager load: items (1-N) dùng selectinload, product (to-one) dùng joinedload
# → số query cố định, không phụ thuộc số order (tránh N+1)
WITH_ITEMS = selectinload(Order.items).joinedload(OrderItem.product)


def _int_arg(name, default, lo, hi):
    try:
        value = int(request.args.get(name, default))
    except (TypeError, ValueError):
        value = default
    return min(hi, max(lo, value))


def _get_order_or_404(order_id):
    order = db.session.execute(
        db.select(Order).options(WITH_ITEMS).where(Order.id == order_id)
    ).scalar_one_or_none()
    if order is None:
        raise NotFound(f"order {order_id} not found")
    return order


def _load_products(ids):
    """Lấy các product còn bán trong 1 query; 422 nếu thiếu product nào."""
    rows = db.session.execute(
        db.select(Product).where(Product.id.in_(ids), Product.archived.is_(False))
    ).scalars().all()
    found = {p.id: p for p in rows}
    missing = sorted(set(ids) - found.keys())
    if missing:
        raise ApiError(f"product not found: {missing}",
                       code="invalid_product", status=422)
    return found


# GET /api/v1/orders?page=1&size=20
@orders_bp.get("")
def list_orders():
    page = _int_arg("page", 1, 1, 10**6)
    size = _int_arg("size", 20, 1, 100)
    rows = db.session.execute(
        db.select(Order).options(WITH_ITEMS)
        .order_by(Order.id).offset((page - 1) * size).limit(size)
    ).scalars().all()
    total = db.session.scalar(db.select(func.count()).select_from(Order))
    return {
        "items": order_out.dump(rows, many=True),
        "page": page,
        "size": size,
        "total": total,
    }, 200


# GET /api/v1/orders/<id>
@orders_bp.get("/<int:id>")
def get_order(id):
    return order_out.dump(_get_order_or_404(id)), 200


# POST /api/v1/orders
# body: {"customer": "An", "items": [{"product_id": 1, "qty": 2}, ...]}
@orders_bp.post("")
def create_order():
    body = OrderIn().load(request.get_json())
    products = _load_products([i["product_id"] for i in body["items"]])

    order = Order(customer=body["customer"])
    for item in body["items"]:
        p = products[item["product_id"]]
        reserve_stock(p, item["qty"])  # lỗi → rollback toàn bộ order
        order.items.append(OrderItem(
            product=p, qty=item["qty"], unit_price_cents=p.price_cents))
    db.session.add(order)
    db.session.commit()

    order = _get_order_or_404(order.id)
    return order_out.dump(order), 201, {"Location": f"/api/v1/orders/{order.id}"}


# POST /api/v1/orders/<id>/items  body: {"product_id": 2, "qty": 1}
@orders_bp.post("/<int:id>/items")
def add_order_item(id):
    body = OrderItemIn().load(request.get_json())
    order = _get_order_or_404(id)
    if any(i.product_id == body["product_id"] for i in order.items):
        raise Conflict(f"product {body['product_id']} already in order {id}")

    p = _load_products([body["product_id"]])[body["product_id"]]
    reserve_stock(p, body["qty"])
    order.items.append(OrderItem(
        product=p, qty=body["qty"], unit_price_cents=p.price_cents))
    db.session.commit()
    return order_out.dump(_get_order_or_404(id)), 201


# DELETE /api/v1/orders/<id>/items/<item_id> — trả lại tồn kho
@orders_bp.delete("/<int:id>/items/<int:item_id>")
def delete_order_item(id, item_id):
    order = _get_order_or_404(id)
    item = next((i for i in order.items if i.id == item_id), None)
    if item is None:
        raise NotFound(f"item {item_id} not found in order {id}")
    release_stock(item.product_id, item.qty)
    order.items.remove(item)  # delete-orphan → xoá dòng order_items
    db.session.commit()
    return "", 204
