import sqlite3
import pytest
from app import app

@pytest.fixture
def client(monkeypatch):
    """Dùng DB ảo :memory: thay cho app.db thật (giống test_books_api.py)."""
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            total_price REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    connection.commit()

    monkeypatch.setattr('routes.orders.get_db', lambda: connection)

    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

    connection.close()


def test_order_api_full_flow(client):
    # CREATE
    resp = client.post("/orders", json={"customer_name": "Nguyen Van A", "total_price": 199.99})
    assert resp.status_code == 201
    assert resp.headers["Location"] == "/orders/1"
    assert resp.get_json()["status"] == "pending"

    # READ
    resp = client.get("/orders/1")
    assert resp.status_code == 200
    assert resp.get_json()["customer_name"] == "Nguyen Van A"

    # LIST + FILTER
    client.post("/orders", json={"customer_name": "Tran Thi B", "total_price": 50, "status": "paid"})
    resp = client.get("/orders?status=paid")
    body = resp.get_json()
    assert body["pagination"]["total"] == 1
    assert body["data"][0]["customer_name"] == "Tran Thi B"

    # UPDATE
    resp = client.put("/orders/1", json={"status": "shipped"})
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "shipped"
    assert client.get("/orders/1").get_json()["status"] == "shipped"

    # DELETE
    assert client.delete("/orders/1").status_code == 204
    assert client.get("/orders/1").status_code == 404

def test_create_order_invalid(client):
    resp = client.post("/orders", json={"customer_name": "A", "total_price": -5})
    assert resp.status_code == 400

def test_update_order_not_found(client):
    resp = client.put("/orders/999", json={"status": "paid"})
    assert resp.status_code == 404
