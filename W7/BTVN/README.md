# W7 · Bài tập về nhà — Backend Service

Phát triển tiếp từ [Lab 1](../Lab1) (BT1 — Product API CRUD).

## Chạy local

```bash
pip install -r requirements.txt
flask --app wsgi db upgrade
flask --app wsgi run
```

## BT2 — Order / OrderItem (`/api/v1/orders`)

Order ⟷ Product là quan hệ N-N qua bảng `order_items` (mỗi dòng có `qty` và giá chụp lúc đặt `unit_price_cents`),
nên một order chứa được nhiều product. Blueprint riêng: `src/product_api/api/orders.py`.

| Method | Path | Mô tả |
|---|---|---|
| GET | `/api/v1/orders?page=1&size=20` | Danh sách order kèm items (eager loading) |
| GET | `/api/v1/orders/<id>` | Chi tiết 1 order — 404 nếu không có |
| POST | `/api/v1/orders` | Tạo order, trừ tồn kho; hết hàng → 409 và rollback cả order |
| POST | `/api/v1/orders/<id>/items` | Thêm 1 product vào order — 409 nếu đã có |
| DELETE | `/api/v1/orders/<id>/items/<item_id>` | Xoá item, trả lại tồn kho |

```json
POST /api/v1/orders
{"customer": "An", "items": [{"product_id": 1, "qty": 2}, {"product_id": 2, "qty": 1}]}
```

Eager loading: `selectinload(Order.items).joinedload(OrderItem.product)` — số query cố định, không bị N+1.
