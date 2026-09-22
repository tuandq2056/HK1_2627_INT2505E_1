import pytest
from unittest.mock import MagicMock
from app import app
from routes import books
from services import book_service
from errors import NotFoundError, ValidationError, ConflictError

@pytest.fixture
def client():
    # Cấu hình app để test
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_list_books_success(client):
    # Mock service
    fake_result = {
        "data": [{"id": 1, "title": "Test"}],
        "pagination": {"page": 1, "size": 20},
        "_links": {}
    }
    books.book_service.get_books_list = MagicMock(return_value=fake_result)
    
    # Mock db connection
    books.get_db = MagicMock()

    response = client.get("/books?page=1&size=20")
    assert response.status_code == 200
    assert response.json["data"][0]["title"] == "Test"
    books.book_service.get_books_list.assert_called_once()

def test_list_books_invalid_params(client):
    # Route phải tự chặn lỗi ValueError (chữ cái thay vì số)
    response = client.get("/books?page=abc")
    assert response.status_code == 400
    assert "error" in response.json

def test_get_book_detail_success(client):
    books.get_db = MagicMock()
    books.book_service.get_book_detail = MagicMock(return_value=({"title": "Test"}, "etag_123"))
    
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json["title"] == "Test"
    assert response.headers["ETag"] == "etag_123"

def test_get_book_detail_not_modified(client):
    books.get_db = MagicMock()
    books.book_service.get_book_detail = MagicMock(return_value=({"title": "Test"}, "etag_123"))
    
    # Gửi Header If-None-Match
    response = client.get("/books/1", headers={"If-None-Match": "etag_123"})
    assert response.status_code == 304
    assert response.data == b"" # 304 không có body

def test_create_book_success(client):
    books.get_db = MagicMock()
    books.book_service.create_book = MagicMock(return_value=({"id": 1, "title": "A"}, "etag_new"))
    
    response = client.post("/books", json={"title": "A", "author": "B"})
    assert response.status_code == 201
    assert response.headers["Location"] == "/books/1"
    assert response.headers["ETag"] == "etag_new"

def test_update_book_missing_if_match(client):
    # Route phải tự chặn 428 nếu không có If-Match
    response = client.put("/books/1", json={"title": "New"})
    assert response.status_code == 428

def test_update_book_success(client):
    books.get_db = MagicMock()
    books.book_service.update_book = MagicMock(return_value=({"id": 1, "title": "New"}, "etag_updated"))
    
    response = client.put("/books/1", json={"title": "New"}, headers={"If-Match": "etag_old"})
    assert response.status_code == 200
    assert response.json["title"] == "New"
    assert response.headers["ETag"] == "etag_updated"

def test_delete_book_success(client):
    books.get_db = MagicMock()
    books.book_service.delete_book = MagicMock()
    
    response = client.delete("/books/1")
    assert response.status_code == 204
    assert response.data == b""

# Test Global Error Handlers
def test_global_not_found_handler(client):
    books.get_db = MagicMock()
    books.book_service.get_book_detail = MagicMock(side_effect=NotFoundError("Not found"))
    
    response = client.get("/books/999")
    assert response.status_code == 404
    assert "Not found" in response.json["error"]

def test_global_conflict_handler(client):
    books.get_db = MagicMock()
    books.book_service.update_book = MagicMock(side_effect=ConflictError("ETag mismatch"))
    
    response = client.put("/books/1", json={"title": "A"}, headers={"If-Match": "bad_etag"})
    assert response.status_code == 412
    assert "ETag mismatch" in response.json["error"]
