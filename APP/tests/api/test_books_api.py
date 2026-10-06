import sqlite3
import pytest
from app import app

@pytest.fixture
def client(monkeypatch):
    """
    Fixture này sẽ thay thế (monkeypatch) hàm get_db() thật trong app.
    Thay vì kết nối vào file app.db thật trên đĩa, nó sẽ ép hệ thống dùng DB ảo :memory:.
    Điều này giúp API test chạy rất nhanh và không làm bẩn DB thật của bạn.
    """
    # 1. Khởi tạo DB ảo và tạo cấu trúc bảng (schema)
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
    connection.commit()

    # 2. Ép hàm get_db() trong file routes/books.py phải trả về DB ảo này
    monkeypatch.setattr('routes.books.get_db', lambda: connection)

    # 3. Trả về Test Client để giả lập gọi HTTP
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
        
    connection.close()


def test_book_api_full_flow(client):
    """
    Đây là bài Kiểm thử Tích hợp (Integration/E2E).
    Nó sẽ giả lập hành vi của 1 người dùng chạy xuyên suốt từ A-Z.
    """
    
    # BƯỚC 1: CREATE (Tạo sách mới)
    payload = {"title": "Harry Potter", "author": "J.K. Rowling", "published_year": 1997}
    resp1 = client.post("/books", json=payload)
    
    assert resp1.status_code == 201
    assert resp1.headers["Location"] == "/books/1"
    etag = resp1.headers["ETag"] # Lưu ETag lại để lát nữa test PUT
    
    
    # BƯỚC 2: READ (Lấy chi tiết cuốn sách vừa tạo)
    resp2 = client.get("/books/1")
    assert resp2.status_code == 200
    assert resp2.json["title"] == "Harry Potter"
    assert resp2.headers["ETag"] == etag
    
    
    # BƯỚC 3: CONDITIONAL READ (Test 304 Not Modified)
    resp3 = client.get("/books/1", headers={"If-None-Match": etag})
    assert resp3.status_code == 304 # 304 Nghĩa là data chưa đổi, lấy trong cache đi
    assert resp3.data == b"" # Body phải trống rỗng
    
    
    # BƯỚC 4: UPDATE (Đổi năm xuất bản)
    update_payload = {"title": "Harry Potter", "author": "J.K. Rowling", "published_year": 2000}
    # Cố tình quên gửi If-Match -> Phải bị chửi 428
    resp4_fail = client.put("/books/1", json=update_payload)
    assert resp4_fail.status_code == 428
    
    # Gửi đúng ETag cũ
    resp4_success = client.put("/books/1", json=update_payload, headers={"If-Match": etag})
    assert resp4_success.status_code == 200
    new_etag = resp4_success.headers["ETag"]
    assert new_etag != etag # ETag phải được đổi sau khi update
    assert resp4_success.json["published_year"] == 2000
    
    
    # BƯỚC 5: READ LIST (Lấy danh sách sách)
    resp5 = client.get("/books?page=1&size=5")
    assert resp5.status_code == 200
    assert resp5.json["pagination"]["total"] == 1
    assert len(resp5.json["data"]) == 1
    assert "self" in resp5.json["_links"]
    
    
    # BƯỚC 6: DELETE (Xóa sách)
    resp6 = client.delete("/books/1")
    assert resp6.status_code == 204
    
    # Gọi lại thử xem còn không -> Phải báo 404
    resp7 = client.get("/books/1")
    assert resp7.status_code == 404


def test_books_cursor_pagination(client):
    """Test Cursor-based pagination: cursor, next_cursor, has_more, limit."""
    # Tạo 5 cuốn sách
    for i in range(1, 6):
        client.post("/books", json={"title": f"Book {i}", "author": "Author A", "published_year": 2000 + i})

    # Page 1: limit 2
    r1 = client.get("/books?limit=2")
    assert r1.status_code == 200
    b1 = r1.get_json()
    assert len(b1["data"]) == 2
    assert b1["pagination"]["has_more"] is True
    assert b1["pagination"]["next_cursor"] is not None
    assert b1["data"][0]["title"] == "Book 1"
    assert b1["data"][1]["title"] == "Book 2"

    # Page 2: dùng next_cursor từ Page 1
    cursor1 = b1["pagination"]["next_cursor"]
    r2 = client.get(f"/books?limit=2&cursor={cursor1}")
    assert r2.status_code == 200
    b2 = r2.get_json()
    assert len(b2["data"]) == 2
    assert b2["pagination"]["has_more"] is True
    assert b2["data"][0]["title"] == "Book 3"
    assert b2["data"][1]["title"] == "Book 4"

    # Page 3: lấy nốt trang cuối
    cursor2 = b2["pagination"]["next_cursor"]
    r3 = client.get(f"/books?limit=2&cursor={cursor2}")
    assert r3.status_code == 200
    b3 = r3.get_json()
    assert len(b3["data"]) == 1
    assert b3["pagination"]["has_more"] is False
    assert b3["pagination"]["next_cursor"] is None
    assert b3["data"][0]["title"] == "Book 5"


def test_books_filter_and_sort(client):
    """Test Filter (author, published_year) và Sort (sort, order)."""
    client.post("/books", json={"title": "1984", "author": "Orwell", "published_year": 1949})
    client.post("/books", json={"title": "Animal Farm", "author": "Orwell", "published_year": 1945})
    client.post("/books", json={"title": "Clean Code", "author": "Martin", "published_year": 2008})

    # Filter theo author
    r_author = client.get("/books?author=Orwell")
    assert r_author.status_code == 200
    b_author = r_author.get_json()
    assert len(b_author["data"]) == 2
    assert all(b["author"] == "Orwell" for b in b_author["data"])

    # Filter theo published_year
    r_year = client.get("/books?published_year=2008")
    assert r_year.status_code == 200
    assert len(r_year.get_json()["data"]) == 1
    assert r_year.get_json()["data"][0]["title"] == "Clean Code"

    # Sort theo published_year DESC
    r_sort = client.get("/books?author=Orwell&sort=-published_year")
    assert r_sort.status_code == 200
    items = r_sort.get_json()["data"]
    assert items[0]["published_year"] == 1949
    assert items[1]["published_year"] == 1945


def test_books_sparse_fieldsets(client):
    """Test Sparse Fieldsets: fields=id,title chỉ trả về 2 trường đó."""
    client.post("/books", json={"title": "Refactoring", "author": "Fowler", "published_year": 1999})

    resp = client.get("/books?fields=id,title")
    assert resp.status_code == 200
    data = resp.get_json()["data"]
    assert len(data) >= 1
    first = data[0]
    assert "id" in first
    assert "title" in first
    assert "author" not in first
    assert "published_year" not in first
    assert "etag" not in first
