def test_create_product_returns_201(client):
    resp = client.post("/api/v1/products", json={
        "sku": "ip-15", "name": "iPhone 15", "price_cents": 2_000_000,
    })

    assert resp.status_code == 201
    body = resp.get_json()
    assert body["id"] > 0
    assert body["sku"] == "IP-15"  # sku được chuẩn hoá viết hoa
    assert body["qty_in_stock"] == 0  # mặc định
    assert body["archived"] is False
    assert resp.headers["Location"] == f"/api/v1/products/{body['id']}"


def test_create_product_duplicate_sku_returns_409(client, make_product):
    make_product("SKU-1")
    resp = client.post("/api/v1/products", json={
        "sku": "sku-1", "name": "dup", "price_cents": 1,
    })

    assert resp.status_code == 409
    assert resp.get_json()["error"] == "conflict"


def test_create_product_invalid_body_returns_422(client):
    resp = client.post("/api/v1/products", json={
        "sku": "x", "name": "", "price_cents": -5,
    })

    assert resp.status_code == 422
    detail = resp.get_json()["detail"]
    assert {"sku", "name", "price_cents"} <= detail.keys()


def test_create_product_bad_json_returns_400(client):
    resp = client.post("/api/v1/products", data="{bad json",
                       content_type="application/json")
    assert resp.status_code == 400


def test_list_products_paginates_and_hides_archived(client, make_product):
    ids = [make_product(f"SKU-{i}")["id"] for i in range(5)]
    client.delete(f"/api/v1/products/{ids[0]}")

    resp = client.get("/api/v1/products?page=2&size=2")

    assert resp.status_code == 200
    body = resp.get_json()
    assert body["total"] == 4
    assert body["page"] == 2 and body["size"] == 2
    assert [p["id"] for p in body["items"]] == ids[3:5]


def test_get_missing_product_returns_404(client):
    resp = client.get("/api/v1/products/9999")
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "not_found", "detail": "product 9999 not found"}


def test_reserve_decrements_stock_and_rejects_oversell(client, make_product):
    p = make_product("SKU-R", qty_in_stock=3)

    ok = client.post(f"/api/v1/products/{p['id']}/reserve", json={"qty": 2})
    too_many = client.post(f"/api/v1/products/{p['id']}/reserve", json={"qty": 2})

    assert ok.status_code == 200
    assert ok.get_json()["product"]["qty_in_stock"] == 1
    assert too_many.status_code == 409
    assert too_many.get_json()["error"] == "out_of_stock"
