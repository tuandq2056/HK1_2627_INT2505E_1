import sqlite3


# ORDERS
#1 READS
def find_order_by_id(db: sqlite3.Connection, order_id: int):
    """
    Tìm đơn hàng theo ID.
    Trả về dictionary chứa thông tin đơn hàng nếu tìm thấy, ngược lại trả về None.
    """
    query = "SELECT * FROM orders WHERE id = ?"
    return db.execute(query, (order_id,)).fetchone()

def _build_where(filters: dict):
    """
    Dịch dict filters ({"status": ..., "customer_name": ...}) thành câu WHERE và list params.
    """
    conditions = []
    params = []
    filters = filters or {}

    if filters.get("status"):
        conditions.append("status = ?")
        params.append(filters["status"])
    if filters.get("customer_name"):
        conditions.append("LOWER(customer_name) LIKE ?")
        params.append(f"%{filters['customer_name'].lower()}%")

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
    return where_clause, params

def find_orders(db: sqlite3.Connection, filters: dict, limit: int, offset: int):
    """
    Tìm đơn hàng theo điều kiện, sắp xếp theo ID.
    Trả về list các dictionary chứa thông tin đơn hàng.
    """
    where_clause, params = _build_where(filters)
    query = f"SELECT * FROM orders {where_clause} ORDER BY id LIMIT ? OFFSET ?"
    return db.execute(query, params + [limit, offset]).fetchall()

def count_orders(db: sqlite3.Connection, filters: dict):
    """
    Đếm số lượng đơn hàng theo điều kiện.
    Trả về số lượng đơn hàng.
    """
    where_clause, params = _build_where(filters)
    query = f"SELECT COUNT(*) as count FROM orders {where_clause}"
    return db.execute(query, params).fetchone()[0]

#2 CREATE
def insert_order(db: sqlite3.Connection, customer_name: str, total_price: float, status: str):
    """
    Thêm đơn hàng mới vào Database.
    Trả về ID của đơn hàng vừa thêm.
    """
    query = "INSERT INTO orders (customer_name, total_price, status) VALUES (?, ?, ?)"
    cursor = db.execute(query, (customer_name, total_price, status))
    db.commit()
    return cursor.lastrowid

#3 UPDATE
def update_order(db: sqlite3.Connection, order_id: int, customer_name: str, total_price: float, status: str):
    """
    Cập nhật thông tin đơn hàng theo ID.
    Trả về số lượng bản ghi bị ảnh hưởng (0 hoặc 1).
    """
    query = "UPDATE orders SET customer_name = ?, total_price = ?, status = ? WHERE id = ?"
    cursor = db.execute(query, (customer_name, total_price, status, order_id))
    db.commit()
    return cursor.rowcount

#4 DELETE
def delete_order(db: sqlite3.Connection, order_id: int):
    """
    Xóa đơn hàng theo ID.
    Trả về số lượng bản ghi bị ảnh hưởng (0 hoặc 1).
    """
    query = "DELETE FROM orders WHERE id = ?"
    cursor = db.execute(query, (order_id,))
    db.commit()
    return cursor.rowcount
