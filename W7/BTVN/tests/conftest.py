from contextlib import contextmanager

import pytest
from sqlalchemy import event

from product_api.config import TestConfig
from product_api.extensions import db
from product_api.factory import create_app


@pytest.fixture
def app():
    app = create_app(TestConfig)  # SQLite in-memory, mỗi test một DB mới
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def count_queries(app):
    """Đếm số câu SQL chạy trong khối `with` — dùng để phát hiện N+1.

        with count_queries() as q:
            client.get(...)
        assert q.count <= 3
    """

    class Counter:
        def __init__(self):
            self.count = 0
            self.statements = []

    @contextmanager
    def _count():
        counter = Counter()

        def _on_execute(conn, cursor, statement, params, context, executemany):
            counter.count += 1
            counter.statements.append(statement)

        with app.app_context():
            engine = db.engine
        event.listen(engine, "before_cursor_execute", _on_execute)
        try:
            yield counter
        finally:
            event.remove(engine, "before_cursor_execute", _on_execute)

    return _count


@pytest.fixture
def make_product(client):
    def _make(sku, price_cents=100, qty_in_stock=10, name=None):
        resp = client.post("/api/v1/products", json={
            "sku": sku,
            "name": name or f"Product {sku}",
            "price_cents": price_cents,
            "qty_in_stock": qty_in_stock,
        })
        assert resp.status_code == 201, resp.get_json()
        return resp.get_json()

    return _make
