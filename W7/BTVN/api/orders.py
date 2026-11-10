from flask import Blueprint, abort, jsonify, request
from sqlalchemy.orm import joinedload, selectinload

from extensions import db

from .models import Order, OrderItem, Product
from .schemas import OrderIn, OrderItemIn, OrderOut

orders_bp = Blueprint("orders", __name__, url_prefix="/api/v1/orders")


def get_order_or_404(id):
    # eager load: items (1-N) dùng selectinload, product (to-one) dùng joinedload
    stmt = db.select(Order).options(
        selectinload(Order.items).joinedload(OrderItem.product)
    ).where(Order.id == id)
    order = db.session.execute(stmt).scalar_one_or_none()
    if order is None:
        abort(404, "order not found")
    return order


def get_product_or_422(id):
    p = db.session.get(Product, id)
    if p is None or p.archived:
        abort(422, f"product {id} not found")
    return p


@orders_bp.get("")
def list_orders():
    page = max(1, request.args.get("page", 1, type=int))
    size = min(100, max(1, request.args.get("size", 20, type=int)))

    # eager load để tránh N+1
    stmt = db.select(Order).options(
        selectinload(Order.items).joinedload(OrderItem.product)
    ).order_by(Order.id).offset((page - 1) * size).limit(size)
    rows = db.session.execute(stmt).scalars().all()
    total = db.session.scalar(db.select(db.func.count()).select_from(Order))

    return jsonify({
        "items": OrderOut(many=True).dump(rows),
        "page": page,
        "size": size,
        "total": total,
    }), 200


@orders_bp.get("/<int:id>")
def get_order(id):
    return OrderOut().dump(get_order_or_404(id)), 200


@orders_bp.post("")
def create_order():
    body = OrderIn().load(request.json)

    ids = [i["product_id"] for i in body["items"]]
    if len(ids) != len(set(ids)):
        abort(422, "product bị trùng trong items")

    order = Order(customer=body["customer"])
    for i in body["items"]:
        p = get_product_or_422(i["product_id"])
        if p.qty_in_stock < i["qty"]:
            db.session.rollback()  # huỷ cả phần đã trừ kho trước đó
            abort(409, f"product {p.id} only {p.qty_in_stock} left")
        p.qty_in_stock -= i["qty"]
        order.items.append(OrderItem(product=p, qty=i["qty"], unit_price_cents=p.price_cents))

    db.session.add(order)
    db.session.commit()
    return OrderOut().dump(order), 201


@orders_bp.post("/<int:id>/items")
def add_order_item(id):
    body = OrderItemIn().load(request.json)
    order = get_order_or_404(id)
    if any(i.product_id == body["product_id"] for i in order.items):
        abort(409, "product đã có trong order")

    p = get_product_or_422(body["product_id"])
    if p.qty_in_stock < body["qty"]:
        abort(409, f"product {p.id} only {p.qty_in_stock} left")
    p.qty_in_stock -= body["qty"]
    order.items.append(OrderItem(product=p, qty=body["qty"], unit_price_cents=p.price_cents))
    db.session.commit()
    return OrderOut().dump(order), 201


@orders_bp.delete("/<int:id>/items/<int:item_id>")
def delete_order_item(id, item_id):
    order = get_order_or_404(id)
    item = db.session.get(OrderItem, item_id)
    if item is None or item.order_id != order.id:
        abort(404, "item not found")

    item.product.qty_in_stock += item.qty  # trả lại kho
    order.items.remove(item)
    db.session.commit()
    return "", 204
