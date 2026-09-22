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
