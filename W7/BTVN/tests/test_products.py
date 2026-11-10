from tests.conftest import create_product


def test_create_product(client):
    resp = client.post("/api/v1/products", json={
        "sku": "ip-15", "name": "iPhone 15", "price_cents": 2000000,
    })

    assert resp.status_code == 201
    body = resp.get_json()
    assert body["sku"] == "ip-15"
    assert body["qty_in_stock"] == 0
    assert body["archived"] is False


def test_create_product_duplicate_sku(client):
    create_product(client, "SKU-1")
    resp = client.post("/api/v1/products", json={
        "sku": "SKU-1", "name": "dup", "price_cents": 1,
    })

    assert resp.status_code == 409
    assert resp.get_json()["error"] == "conflict"


def test_create_product_invalid_body(client):
    resp = client.post("/api/v1/products", json={
        "sku": "x", "name": "", "price_cents": -5,
    })

    assert resp.status_code == 422
    assert set(resp.get_json()["detail"]) == {"sku", "name", "price_cents"}


def test_create_product_bad_json(client):
    resp = client.post("/api/v1/products", data="{bad json",
                       content_type="application/json")
    assert resp.status_code == 400


def test_list_products_paginate_and_hide_deleted(client):
    ids = [create_product(client, f"SKU-{i}")["id"] for i in range(5)]
    client.delete(f"/api/v1/products/{ids[0]}")

    body = client.get("/api/v1/products?page=2&size=2").get_json()

    assert body["total"] == 4
    assert [p["id"] for p in body["items"]] == ids[3:5]


def test_get_missing_product(client):
    resp = client.get("/api/v1/products/9999")
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "not_found"


def test_update_product(client):
    p = create_product(client, "SKU-U")

    resp = client.patch(f"/api/v1/products/{p['id']}", json={"price_cents": 500})

    assert resp.status_code == 200
    assert resp.get_json()["price_cents"] == 500


def test_reserve(client):
    p = create_product(client, "SKU-R", qty_in_stock=3)

    ok = client.post(f"/api/v1/products/{p['id']}/reserve", json={"qty": 2})
    too_many = client.post(f"/api/v1/products/{p['id']}/reserve", json={"qty": 2})

    assert ok.status_code == 200
    assert ok.get_json()["qty_in_stock"] == 1
    assert too_many.status_code == 409
