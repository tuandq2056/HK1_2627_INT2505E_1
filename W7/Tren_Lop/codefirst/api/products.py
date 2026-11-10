from flask.views import MethodView
from flask_smorest import Blueprint, abort

from .schemas import ProductSchema, ProductInSchema
from .models import Product
from extensions import db

blp = Blueprint("products", __name__, url_prefix="/products", description="Thao tác với sản phẩm")

@blp.route("")
class ProductList(MethodView):
    @blp.arguments(ProductInSchema)  # validate POST body
    @blp.response(201, ProductSchema)
    def post(self, data):
        """Tạo sản phẩm mới"""
        p = Product(**data)
        db.session.add(p)
        db.session.commit()
        return p

    @blp.response(200, ProductSchema(many=True))
    def get(self):
        """Lấy danh sách tất cả sản phẩm"""
        return db.session.execute(db.select(Product)).scalars().all()


@blp.route("/<int:product_id>")
class ProductItem(MethodView):
    @blp.response(200, ProductSchema)
    def get(self, product_id):
        """Lấy chi tiết một sản phẩm theo ID"""
        product = db.session.get(Product, product_id)
        if not product:
            abort(404, message="Product not found")
        return product

    @blp.response(204)
    def delete(self, product_id):
        """Xóa sản phẩm theo ID"""
        product = db.session.get(Product, product_id)
        if not product:
            abort(404, message="Product not found")

        db.session.delete(product)
        db.session.commit()
        return ""