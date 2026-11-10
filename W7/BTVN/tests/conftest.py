import pytest
from sqlalchemy import event

from app import create_app
from extensions import db


@pytest.fixture
def app():
    # mỗi test dùng 1 DB SQLite trong RAM mới
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def queries(app):
    # Ghi lại mọi câu SQL chạy trong test -> dùng để kiểm tra N+1
    sql_list = []

    def on_execute(conn, cursor, statement, params, context, executemany):
        sql_list.append(statement)

    event.listen(db.engine, "before_cursor_execute", on_execute)
    yield sql_list
    event.remove(db.engine, "before_cursor_execute", on_execute)


def create_product(client, sku, price_cents=100, qty_in_stock=10):
    resp = client.post("/api/v1/products", json={
        "sku": sku,
        "name": f"Product {sku}",
        "price_cents": price_cents,
        "qty_in_stock": qty_in_stock,
    })
    assert resp.status_code == 201
    return resp.get_json()


def create_order(client, items, customer="An"):
    return client.post("/api/v1/orders", json={"customer": customer, "items": items})
