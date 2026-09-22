import sqlite3
import pytest
from repos import book_repo

@pytest.fixture
def db():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    
    connection.execute('''
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            published_year INTEGER,
            etag TEXT
        )
    ''')
    
    # Nạp 3 cuốn sách mồi với dữ liệu khác nhau để test search/filter
    books = [
        ("Clean Code", "Robert C. Martin", 2008, "etag1"),
        ("Clean Architecture", "Robert C. Martin", 2017, "etag2"),
        ("1984", "George Orwell", 1949, "etag3")
    ]
    for b in books:
        connection.execute("INSERT INTO books (title, author, published_year, etag) VALUES (?, ?, ?, ?)", b)
    connection.commit()
    
    yield connection
    connection.close()


# --- TEST READ ---

def test_find_book_by_id_success(db):
    row = book_repo.find_book_by_id(db, 1)
    assert row is not None
    assert row["title"] == "Clean Code"

def test_find_book_by_id_fail(db):
    row = book_repo.find_book_by_id(db, 999)
    assert row is None

def test_find_books_filter_author(db):
    """Test lọc theo tác giả"""
    where_clause = "WHERE LOWER(author) = ?"
    params = ["robert c. martin"]
    rows = book_repo.find_books(db, where_clause, params, "", 10, 0)
    
    assert len(rows) == 2
    assert all(r["author"] == "Robert C. Martin" for r in rows)

def test_find_books_search_title(db):
    """Test tìm kiếm (q) theo tiêu đề"""
    where_clause = "WHERE LOWER(title) LIKE ?"
    params = ["%clean%"]
    rows = book_repo.find_books(db, where_clause, params, "", 10, 0)
    
    assert len(rows) == 2
    titles = [r["title"] for r in rows]
    assert "Clean Code" in titles
    assert "Clean Architecture" in titles

def test_find_books_sorting(db):
    """Test sắp xếp giảm dần theo published_year"""
    sort_query = "ORDER BY published_year DESC"
    rows = book_repo.find_books(db, "", [], sort_query, 10, 0)
    
    assert len(rows) == 3
    assert rows[0]["title"] == "Clean Architecture" # 2017
    assert rows[1]["title"] == "Clean Code" # 2008
    assert rows[2]["title"] == "1984" # 1949

def test_count_books_with_filter(db):
    """Test đếm số lượng sách theo điều kiện (phục vụ tính total_pages)"""
    where_clause = "WHERE LOWER(author) = ?"
    params = ["george orwell"]
    total = book_repo.count_books(db, where_clause, params)
    
    assert total == 1


# --- TEST CREATE ---

def test_insert_book(db):
    new_id = book_repo.insert_book(db, "Book C", "Author C", 2022, "etagC")
    assert new_id == 4  # Vì đã mồi sẵn 3 cuốn rồi
    
    row = db.execute("SELECT * FROM books WHERE id = ?", (new_id,)).fetchone()
    assert row["title"] == "Book C"


# --- TEST UPDATE ---

def test_update_book_success(db):
    affected = book_repo.update_book(db, 1, "Clean Code v2", "Robert C. Martin", 2008, "new_etag")
    assert affected == 1
    
    row = db.execute("SELECT * FROM books WHERE id = 1").fetchone()
    assert row["title"] == "Clean Code v2"
    assert row["etag"] == "new_etag"

def test_update_book_not_exist(db):
    """Test lỗi ngầm của SQLite: Update một id không có thật thì rowcount = 0"""
    affected = book_repo.update_book(db, 999, "Fake Book", "Fake Author", 2024, "etag")
    assert affected == 0


# --- TEST DELETE ---

def test_delete_book_success(db):
    affected = book_repo.delete_book(db, 1)
    assert affected == 1
    
    row = book_repo.find_book_by_id(db, 1)
    assert row is None

def test_delete_book_not_exist(db):
    """Test lỗi ngầm: Xóa một id không có thật thì rowcount = 0"""
    affected = book_repo.delete_book(db, 999)
    assert affected == 0
