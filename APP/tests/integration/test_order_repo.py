import sqlite3
import pytest
from repos import order_repo

@pytest.fixture
def db():
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

    # Nạp 3 đơn hàng mồi
    orders = [
        ("Nguyen Van A", 100.0, "pending"),
        ("Tran Thi B", 250.5, "paid"),
        ("Nguyen Van C", 75.0, "pending")
    ]
    for o in orders:
        connection.execute("INSERT INTO orders (customer_name, total_price, status) VALUES (?, ?, ?)", o)
    connection.commit()

    yield connection
    connection.close()


# --- TEST READ ---

def test_find_order_by_id_success(db):
    row = order_repo.find_order_by_id(db, 2)
    assert row["customer_name"] == "Tran Thi B"

def test_find_order_by_id_fail(db):
    assert order_repo.find_order_by_id(db, 999) is None

def test_find_orders_filter_status(db):
    rows = order_repo.find_orders(db, {"status": "pending"}, 10, 0)
    assert len(rows) == 2
    assert all(r["status"] == "pending" for r in rows)

def test_find_orders_filter_customer_name(db):
    rows = order_repo.find_orders(db, {"customer_name": "nguyen"}, 10, 0)
    assert [r["id"] for r in rows] == [1, 3]

def test_find_orders_pagination(db):
    rows = order_repo.find_orders(db, {}, 2, 2)
    assert len(rows) == 1
    assert rows[0]["id"] == 3

def test_count_orders_with_filter(db):
    assert order_repo.count_orders(db, {"status": "paid"}) == 1
    assert order_repo.count_orders(db, None) == 3


# --- TEST CREATE / UPDATE / DELETE ---

def test_insert_order(db):
    new_id = order_repo.insert_order(db, "Le Van D", 10.0, "pending")
    assert new_id == 4
    assert order_repo.find_order_by_id(db, new_id)["customer_name"] == "Le Van D"

def test_update_order_success(db):
    affected = order_repo.update_order(db, 1, "Nguyen Van A", 120.0, "shipped")
    assert affected == 1
    row = order_repo.find_order_by_id(db, 1)
    assert row["status"] == "shipped"
    assert row["total_price"] == 120.0

def test_update_order_not_exist(db):
    assert order_repo.update_order(db, 999, "X", 1.0, "paid") == 0

def test_delete_order_success(db):
    assert order_repo.delete_order(db, 1) == 1
    assert order_repo.find_order_by_id(db, 1) is None

def test_delete_order_not_exist(db):
    assert order_repo.delete_order(db, 999) == 0
