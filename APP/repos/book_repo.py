import sqlite3


# BOOKS
#1 READS
def find_book_by_id(db: sqlite3.Connection, book_id: int):
    """
    Tìm sách theo ID.
    Trả về dictionary chứa thông tin sách nếu tìm thấy, ngược lại trả về None.
    """
    query = "SELECT * FROM books WHERE id = ?"
    return db.execute(query, (book_id,)).fetchone()

# Các cột được phép sắp xếp (whitelist để chống SQL Injection qua ORDER BY)
SORTABLE_COLUMNS = {"id", "title", "author", "published_year"}

def _build_where(filters: dict):
    """
    Dịch dict filters ({"author": ..., "q": ...}) thành câu WHERE và list params.
    Toàn bộ SQL chỉ nằm ở tầng Repo, tầng Service không cần biết đến SQL.
    """
    conditions = []
    params = []
    filters = filters or {}

    if filters.get("author"):
        conditions.append("LOWER(author) = ?")
        params.append(filters["author"].lower())
    if filters.get("published_year"):
        conditions.append("published_year = ?")
        params.append(int(filters["published_year"]))
    if filters.get("q"):
        q = f"%{filters['q'].lower()}%"
        conditions.append("(LOWER(title) LIKE ? OR LOWER(author) LIKE ?)")
        params.extend([q, q])

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
    return where_clause, params

def _build_order_by(sort_by: str, order: str):
    """Sinh câu ORDER BY an toàn. Cột không hợp lệ sẽ bị bỏ qua."""
    if sort_by not in SORTABLE_COLUMNS:
        return ""
    direction = "DESC" if (order or "").lower() == "desc" else "ASC"
    return f"ORDER BY {sort_by} {direction}"

def find_books(db: sqlite3.Connection, filters: dict, limit: int, offset: int, sort_by: str = None, order: str = "asc"):
    """
    Tìm sách theo điều kiện (Offset pagination).
    Trả về list các dictionary chứa thông tin sách.
    """
    where_clause, params = _build_where(filters)
    sort_query = _build_order_by(sort_by, order)
    query = f"SELECT * FROM books {where_clause} {sort_query} LIMIT ? OFFSET ?"
    return db.execute(query, params + [limit, offset]).fetchall()

def find_books_cursor(db: sqlite3.Connection, filters: dict, limit: int, cursor_id: int = None, sort_by: str = "id", order: str = "asc"):
    """
    Tìm sách dùng Keyset/Cursor pagination (lấy limit + 1 để biết has_more).
    """
    where_clause, params = _build_where(filters)
    direction = "DESC" if (order or "").lower() == "desc" else "ASC"
    op = "<" if direction == "DESC" else ">"

    cursor_params = []
    if cursor_id is not None:
        cursor_cond = f"id {op} ?"
        cursor_params = [cursor_id]
        where_clause = f"{where_clause} AND {cursor_cond}" if where_clause else f"WHERE {cursor_cond}"

    sort_query = _build_order_by(sort_by, order)
    if not sort_query:
        sort_query = f"ORDER BY id {direction}"
    elif sort_by != "id":
        sort_query = f"{sort_query}, id {direction}"

    query = f"SELECT * FROM books {where_clause} {sort_query} LIMIT ?"
    return db.execute(query, params + cursor_params + [limit + 1]).fetchall()
    

def count_books(db: sqlite3.Connection, filters: dict):
    """
    Đếm số lượng sách theo điều kiện.
    Trả về số lượng sách.
    """
    where_clause, params = _build_where(filters)
    query = f"SELECT COUNT(*) as count FROM books {where_clause}"
    return db.execute(query, params).fetchone()[0]

#2 CREATE
def insert_book(db: sqlite3.Connection, title: str, author: str, published_year: int, etag: str):
    """
    Thêm sách mới vào Database.
    Trả về ID của sách vừa thêm.
    """
    query = "INSERT INTO books (title, author, published_year, etag) VALUES (?, ?, ?, ?)"
    cursor = db.execute(query, (title, author, published_year, etag))
    db.commit()
    return cursor.lastrowid

#3 UPDATE
def update_book(db: sqlite3.Connection, book_id: int, title: str, author: str, published_year: int, etag: str):
    """
    Cập nhật thông tin sách theo ID.
    Trả về số lượng bản ghi bị ảnh hưởng (0 hoặc 1).
    """
    query = "UPDATE books SET title = ?, author = ?, published_year = ?, etag = ? WHERE id = ?"
    cursor = db.execute(query, (title, author, published_year, etag, book_id))
    db.commit()
    return cursor.rowcount

#4 DElETE
def delete_book(db: sqlite3.Connection, book_id: int):
    """
    Xóa sách theo ID.
    Trả về số lượng bản ghi bị ảnh hưởng (0 hoặc 1).
    """
    query = "DELETE FROM books WHERE id = ?"
    cursor = db.execute(query, (book_id,))
    db.commit()
    return cursor.rowcount