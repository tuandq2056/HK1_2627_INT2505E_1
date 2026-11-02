from flask import Blueprint, request
from sqlalchemy import func, update
from sqlalchemy.exc import IntegrityError

from ..errors import Conflict, NotFound, OutOfStock
from ..extensions import db
from ..models import Product
from ..schemas import ProductIn, ProductOut, ProductPatch, ReserveIn

products_bp = Blueprint("products", __name__, url_prefix="/api/v1/products")

product_out = ProductOut()


def _json_body():
    # Content-type sai hoặc JSON hỏng → werkzeug ném 400/415
    return request.get_json()


def _int_arg(name, default, lo, hi):
    raw = request.args.get(name, default)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        value = default
    return min(hi, max(lo, value))


def get_active_or_404(product_id):
    p = db.session.get(Product, product_id)
    if p is None or p.archived:
        raise NotFound(f"product {product_id} not found")
    return p


# GET /api/v1/products?page=1&size=20
@products_bp.get("")
def list_products():
    page = _int_arg("page", 1, 1, 10**6)
    size = _int_arg("size", 20, 1, 100)

    base = db.select(Product).where(Product.archived.is_(False))
    rows = db.session.execute(
        base.order_by(Product.id).offset((page - 1) * size).limit(size)
    ).scalars().all()
    total = db.session.scalar(
        db.select(func.count()).select_from(Product)
        .where(Product.archived.is_(False)))

    return {
        "items": product_out.dump(rows, many=True),
        "page": page,
        "size": size,
        "total": total,
    }, 200


# GET /api/v1/products/<id>
@products_bp.get("/<int:id>")
def get_product(id):
    return product_out.dump(get_active_or_404(id)), 200


# POST /api/v1/products
@products_bp.post("")
def create_product():
    body = ProductIn().load(_json_body())
    p = Product(**body)
    db.session.add(p)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Conflict(f"sku {body['sku']} already exists")
    return product_out.dump(p), 201, {"Location": f"/api/v1/products/{p.id}"}


# POST /api/v1/products/<id>/reserve  body: {"qty": 1}
@products_bp.post("/<int:id>/reserve")
def reserve_product(id):
    body = ReserveIn().load(_json_body())
    qty = body["qty"]
    p = get_active_or_404(id)

    # UPDATE có điều kiện — atomic, tránh 2 request cùng lúc làm tồn kho < 0
    result = db.session.execute(
        update(Product)
        .where(Product.id == id, Product.qty_in_stock >= qty)
        .values(qty_in_stock=Product.qty_in_stock - qty)
        .execution_options(synchronize_session=False)
    )
    if result.rowcount == 0:
        db.session.rollback()
        db.session.refresh(p)
        raise OutOfStock(f"only {p.qty_in_stock} left, requested {qty}")

    db.session.commit()
    db.session.refresh(p)
    return {"reserved": qty, "product": product_out.dump(p)}, 200


# PATCH /api/v1/products/<id>
@products_bp.patch("/<int:id>")
def patch_product(id):
    body = ProductPatch().load(_json_body(), partial=True)
    p = get_active_or_404(id)
    for k, v in body.items():
        setattr(p, k, v)
    db.session.commit()
    return product_out.dump(p), 200


# DELETE /api/v1/products/<id> — soft delete
@products_bp.delete("/<int:id>")
def delete_product(id):
    p = get_active_or_404(id)
    p.archived = True
    db.session.commit()
    return "", 204
