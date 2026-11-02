# W7 · Lab 1 — Product API CRUD

Flask + SQLAlchemy 2.x + Marshmallow + Flask-Migrate, dùng application factory và blueprint.

## Chạy

```bash
pip install -r requirements.txt
cp .env.example .env            # tuỳ chọn
flask --app wsgi db upgrade     # tạo bảng theo migrations/
flask --app wsgi run
```

## Endpoints

| Method | Path | Mô tả |
|---|---|---|
| GET | `/api/v1/products?page=1&size=20` | Danh sách có phân trang (bỏ qua archived) |
| GET | `/api/v1/products/<id>` | Lấy 1 sản phẩm — 404 nếu không có |
| POST | `/api/v1/products` | Tạo sản phẩm — 409 nếu sku trùng |
| POST | `/api/v1/products/<id>/reserve` | Body `{"qty": 1}` — 409 nếu hết hàng |
| PATCH | `/api/v1/products/<id>` | Cập nhật một phần |
| DELETE | `/api/v1/products/<id>` | Soft delete (`archived=true`) |

Lỗi trả về dạng `{"error": "...", "detail": "..."}` (400/404/409/422).

## Cấu trúc

```
src/product_api/
  factory.py         create_app()
  config.py          Default / Test / Production config (đọc env)
  extensions.py      db, migrate
  errors.py          ApiError + global error handlers
  logging_config.py  log JSON một dòng, có request_id + latency
  schemas.py         ProductOut, ProductIn, ProductPatch, ReserveIn
  models/product.py  Product (SQLAlchemy 2.x typed)
  api/products.py    Blueprint 6 endpoint
migrations/          Alembic revisions
wsgi.py              entry point: app = create_app()
```
