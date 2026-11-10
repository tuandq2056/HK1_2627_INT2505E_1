
# pyrefly: ignore[missing-import]
from marshmallow import Schema, fields


class ProductInSchema(Schema):
  name = fields.String(required=True)
  price = fields.Float(required=True)


class ProductSchema(ProductInSchema):
  id = fields.Integer(dump_only=True)