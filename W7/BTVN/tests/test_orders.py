from product_api.extensions import db
from product_api.models import Order


def _create_order(client, items, customer="An"):
    return client.post("/api/v1/orders", json={"customer": customer, "items": items})


# ─── POST ───
def test_create_order_with_many_products(client, make_product):
    a = make_product("A-1", price_cents=100, qty_in_stock=5)
    b = make_product("B-1", price_cents=250, qty_in_stock=2)

    resp = _create_order(client, [
        {"product_id": a["id"], "qty": 2},
        {"product_id": b["id"], "qty": 1},
    ])

    assert resp.status_code == 201
    order = resp.get_json()
    assert [i["sku"] for i in order["items"]] == ["A-1", "B-1"]
    assert order["total_cents"] == 2 * 100 + 1 * 250
    # tồn kho đã bị trừ
    assert client.get(f"/api/v1/products/{a['id']}").get_json()["qty_in_stock"] == 3
    assert client.get(f"/api/v1/products/{b['id']}").get_json()["qty_in_stock"] == 1


def test_create_order_out_of_stock_rolls_back_everything(app, client, make_product):
    a = make_product("A-1", qty_in_stock=5)
    b = make_product("B-1", qty_in_stock=1)

    resp = _create_order(client, [
        {"product_id": a["id"], "qty": 2},
        {"product_id": b["id"], "qty": 3},  # không đủ hàng
    ])

    assert resp.status_code == 409
    # Không trừ tồn kho của A, không tạo order nào
    assert client.get(f"/api/v1/products/{a['id']}").get_json()["qty_in_stock"] == 5
    with app.app_context():
        assert db.session.scalar(db.select(db.func.count()).select_from(Order)) == 0


def test_create_order_rejects_duplicate_and_unknown_products(client, make_product):
    a = make_product("A-1")

    dup = _create_order(client, [{"product_id": a["id"], "qty": 1}] * 2)
    unknown = _create_order(client, [{"product_id": 999, "qty": 1}])

    assert dup.status_code == 422
    assert unknown.status_code == 422
    assert unknown.get_json()["error"] == "invalid_product"


# ─── GET + eager loading / N+1 ───
def _seed_orders(client, make_product, n):
    products = [make_product(f"P-{i}", qty_in_stock=100) for i in range(3)]
    for k in range(n):
        resp = _create_order(client, [
            {"product_id": p["id"], "qty": 1} for p in products
        ], customer=f"C{k}")
        assert resp.status_code == 201


def test_get_order_detail(client, make_product):
    _seed_orders(client, make_product, 1)

    resp = client.get("/api/v1/orders/1")

    assert resp.status_code == 200
    body = resp.get_json()
    assert len(body["items"]) == 3
    assert all(i["sku"].startswith("P-") for i in body["items"])
    assert client.get("/api/v1/orders/42").status_code == 404


def test_list_orders_query_count_is_constant(client, make_product, count_queries):
    """Eager loading: số query không tăng theo số order (không N+1)."""
    _seed_orders(client, make_product, 2)
    with count_queries() as small:
        r1 = client.get("/api/v1/orders?size=100")

    for k in range(18):
        resp = _create_order(client, [{"product_id": 1, "qty": 1}], customer=f"X{k}")
        assert resp.status_code == 201
    with count_queries() as large:
        r2 = client.get("/api/v1/orders?size=100")

    assert r1.status_code == r2.status_code == 200
    assert r1.get_json()["total"] == 2
    assert r2.get_json()["total"] == 20
    # count + orders + (items JOIN products) = 3 query, dù 2 hay 20 order
    assert small.count == large.count
    assert large.count <= 3, large.statements


def test_lazy_loading_would_be_n_plus_1(app, client, make_product, count_queries):
    """Đối chứng: không eager load thì số query tăng theo số order → counter bắt được N+1."""
    _seed_orders(client, make_product, 5)

    with app.app_context(), count_queries() as q:
        orders = db.session.execute(db.select(Order)).scalars().all()
        for o in orders:
            for item in o.items:  # lazy load mỗi order
                _ = item.product.sku  # lazy load mỗi product (lần đầu)

    # 1 query orders + 5 query items (+ product) — lớn hơn hẳn bản eager
    assert q.count >= 1 + len(orders)
