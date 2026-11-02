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

## BT3 — Docker

```bash
docker compose up -d --build      # Postgres 16 + API (gunicorn) ở http://localhost:5000
docker compose logs -f api
docker compose down               # thêm -v để xoá luôn dữ liệu Postgres
```

- `Dockerfile` multi-stage: stage builder cài package vào `/opt/venv`, stage runtime chỉ copy venv + `wsgi.py` + `migrations/`, chạy bằng user `app` (không root).
- `docker-entrypoint.sh`: chạy `flask db upgrade` rồi `exec gunicorn` → máy mới chỉ cần `docker compose up`, không phải tạo bảng tay.
- `docker-compose.yml`: API chờ DB `service_healthy` (`pg_isready`) mới khởi động; cấu hình qua biến môi trường (`DB_URL`, `SECRET_KEY`, `LOG_LEVEL`, `API_PORT` để đổi port nếu 5000 bị chiếm).
- `.gitattributes` giữ LF cho file `.sh` để clone trên Windows vẫn chạy được.

## BT4 — Health check (`src/product_api/api/health.py`)

| Endpoint | Loại | Kiểm tra | Kết quả |
|---|---|---|---|
| `GET /healthz` | Liveness | Không chạm DB | `200 {"status": "ok"}` khi process còn chạy |
| `GET /ready` | Readiness | `SELECT 1` tới DB | `200` nếu DB ok, `503 {"status": "degraded"}` nếu DB lỗi |

Tách riêng để DB chết thì orchestrator chỉ ngừng gửi traffic (readiness fail), không restart API vô ích (liveness vẫn ok).
`Dockerfile` có `HEALTHCHECK` gọi `/healthz` → `docker ps` hiện trạng thái `healthy`.

Kiểm tra: `docker compose stop db` → `/healthz` vẫn 200, `/ready` trả 503; `docker compose start db` → `/ready` về 200.
