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

def find_books(db: sqlite3.Connection, where_clause: str , params: list,sort_query:str, limit: int, offset: int):
    """
    Tìm sách theo điều kiện.
    Trả về list các dictionary chứa thông tin sách.
    """
    query = f"SELECT * FROM books {where_clause} {sort_query} LIMIT ? OFFSET ?"

    params.extend([limit, offset])
    return db.execute(query, params).fetchall()
    

def count_books(db: sqlite3.Connection, where_clause: str, params: list):
    """
    Đếm số lượng sách theo điều kiện.
    Trả về số lượng sách.
    """
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