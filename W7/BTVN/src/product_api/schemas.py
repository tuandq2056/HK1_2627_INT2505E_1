from marshmallow import (
    Schema, ValidationError, fields, pre_load, validate, validates,
    validates_schema)


# ─── output ───
class ProductOut(Schema):
    id = fields.Int()
    sku = fields.Str()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    price_cents = fields.Int()
    qty_in_stock = fields.Int()
    archived = fields.Bool()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


# ─── input tạo mới ───
class ProductIn(Schema):
    sku = fields.Str(required=True, validate=[
        validate.Length(min=3, max=32),
        validate.Regexp(r"^[A-Z0-9-]+$", error="sku chỉ gồm A-Z, 0-9 và '-'"),
    ])
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(
        allow_none=True, validate=validate.Length(max=2000))
    price_cents = fields.Int(
        required=True, strict=True,
        validate=validate.Range(min=0, max=10_000_000))
    qty_in_stock = fields.Int(
        load_default=0, strict=True, validate=validate.Range(min=0))

    @pre_load
    def _normalize(self, data, **kwargs):
        # Chuẩn hoá trước khi validate: bỏ khoảng trắng, sku viết hoa
        if isinstance(data, dict):
            data = dict(data)
            if isinstance(data.get("sku"), str):
                data["sku"] = data["sku"].strip().upper()
            if isinstance(data.get("name"), str):
                data["name"] = data["name"].strip()
        return data

    @validates("name")
    def _name_not_blank(self, value, **kwargs):
        if value.strip() == "":
            raise ValidationError("name không được để trống")


# ─── PATCH: chỉ field có trong body mới đổi ───
class ProductPatch(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=255))
    description = fields.Str(
        allow_none=True, validate=validate.Length(max=2000))
    price_cents = fields.Int(
        strict=True, validate=validate.Range(min=0, max=10_000_000))
    qty_in_stock = fields.Int(strict=True, validate=validate.Range(min=0))

    @validates_schema
    def _not_empty(self, data, **kwargs):
        if not data:
            raise ValidationError("body phải có ít nhất 1 field để cập nhật")


# ─── /reserve ───
class ReserveIn(Schema):
    qty = fields.Int(required=True, strict=True,
                     validate=validate.Range(min=1))


# ─── Order / OrderItem ───
class OrderItemIn(Schema):
    product_id = fields.Int(required=True, strict=True,
                            validate=validate.Range(min=1))
    qty = fields.Int(required=True, strict=True,
                     validate=validate.Range(min=1, max=1000))


class OrderIn(Schema):
    customer = fields.Str(required=True,
                          validate=validate.Length(min=1, max=255))
    items = fields.List(fields.Nested(OrderItemIn), required=True,
                        validate=validate.Length(min=1, max=100))

    @validates_schema
    def _no_duplicate_product(self, data, **kwargs):
        ids = [i["product_id"] for i in data.get("items", [])]
        if len(ids) != len(set(ids)):
            raise ValidationError(
                "mỗi product chỉ xuất hiện 1 lần trong items", "items")


class OrderItemOut(Schema):
    id = fields.Int()
    product_id = fields.Int()
    sku = fields.Function(lambda i: i.product.sku)
    product_name = fields.Function(lambda i: i.product.name)
    qty = fields.Int()
    unit_price_cents = fields.Int()
    line_total_cents = fields.Int()


class OrderOut(Schema):
    id = fields.Int()
    customer = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime()
    items = fields.List(fields.Nested(OrderItemOut))
    total_cents = fields.Int()
