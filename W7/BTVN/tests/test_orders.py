from api.models import Order
from extensions import db
from tests.conftest import create_order, create_product


def get_stock(client, product_id):
    return client.get(f"/api/v1/products/{product_id}").get_json()["qty_in_stock"]


def test_create_order_with_many_products(client):
    a = create_product(client, "A-1", price_cents=100, qty_in_stock=5)
    b = create_product(client, "B-1", price_cents=250, qty_in_stock=2)

    resp = create_order(client, [
        {"product_id": a["id"], "qty": 2},
        {"product_id": b["id"], "qty": 1},
    ])

    assert resp.status_code == 201
    order = resp.get_json()
    assert [i["sku"] for i in order["items"]] == ["A-1", "B-1"]
    assert get_stock(client, a["id"]) == 3
    assert get_stock(client, b["id"]) == 1


def test_create_order_out_of_stock_rollback(client):
    a = create_product(client, "A-1", qty_in_stock=5)
    b = create_product(client, "B-1", qty_in_stock=1)

    resp = create_order(client, [
        {"product_id": a["id"], "qty": 2},
        {"product_id": b["id"], "qty": 3},  # không đủ hàng
    ])

    assert resp.status_code == 409
    assert get_stock(client, a["id"]) == 5  # A không bị trừ kho
    assert db.session.scalar(db.select(db.func.count()).select_from(Order)) == 0


def test_create_order_duplicate_or_unknown_product(client):
    a = create_product(client, "A-1")

    dup = create_order(client, [{"product_id": a["id"], "qty": 1}] * 2)
    unknown = create_order(client, [{"product_id": 999, "qty": 1}])

    assert dup.status_code == 422
    assert unknown.status_code == 422


def test_add_and_delete_item(client):
    a = create_product(client, "A-1", qty_in_stock=5)
    b = create_product(client, "B-1", qty_in_stock=5)
    order = create_order(client, [{"product_id": a["id"], "qty": 1}]).get_json()

    added = client.post(f"/api/v1/orders/{order['id']}/items",
                        json={"product_id": b["id"], "qty": 2})
    again = client.post(f"/api/v1/orders/{order['id']}/items",
                        json={"product_id": b["id"], "qty": 1})

    assert added.status_code == 201
    assert len(added.get_json()["items"]) == 2
    assert again.status_code == 409
    assert get_stock(client, b["id"]) == 3

    item_id = added.get_json()["items"][1]["id"]
    resp = client.delete(f"/api/v1/orders/{order['id']}/items/{item_id}")

    assert resp.status_code == 204
    assert get_stock(client, b["id"]) == 5  # trả lại kho


def test_get_order(client):
    a = create_product(client, "A-1")
    create_order(client, [{"product_id": a["id"], "qty": 1}])

    assert client.get("/api/v1/orders/1").status_code == 200
    assert client.get("/api/v1/orders/42").status_code == 404


def test_list_orders_no_n_plus_1(client, queries):
    """Eager loading: 2 order hay 20 order thì số query vẫn như nhau."""
    products = [create_product(client, f"P-{i}", qty_in_stock=100) for i in range(3)]
    items = [{"product_id": p["id"], "qty": 1} for p in products]

    for _ in range(2):
        create_order(client, items)
    queries.clear()
    client.get("/api/v1/orders?size=100")
    count_small = len(queries)

    for _ in range(18):
        create_order(client, items)
    queries.clear()
    resp = client.get("/api/v1/orders?size=100")
    count_large = len(queries)

    assert resp.get_json()["total"] == 20
    assert count_small == count_large
    assert count_large <= 3  # count + orders + items/products
