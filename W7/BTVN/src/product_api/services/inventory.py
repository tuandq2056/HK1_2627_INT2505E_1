"""Logic tồn kho dùng chung cho products và orders. Không commit — caller quyết định."""
from sqlalchemy import update

from ..errors import OutOfStock
from ..extensions import db
from ..models import Product


def reserve_stock(product, qty):
    # UPDATE có điều kiện — atomic, tránh 2 request cùng lúc làm tồn kho < 0
    result = db.session.execute(
        update(Product)
        .where(Product.id == product.id, Product.qty_in_stock >= qty)
        .values(qty_in_stock=Product.qty_in_stock - qty)
        .execution_options(synchronize_session=False)
    )
    if result.rowcount == 0:
        db.session.rollback()
        db.session.refresh(product)
        raise OutOfStock(
            f"product {product.id}: only {product.qty_in_stock} left, requested {qty}")


def release_stock(product_id, qty):
    db.session.execute(
        update(Product)
        .where(Product.id == product_id)
        .values(qty_in_stock=Product.qty_in_stock + qty)
        .execution_options(synchronize_session=False)
    )
