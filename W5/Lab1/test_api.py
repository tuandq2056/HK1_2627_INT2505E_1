import pytest
from app import create_app
from models import db, Book


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        # Seed 1 cuốn sách mẫu cho test
        sample = Book(title="Sample Book", isbn="9780132350884", price_vnd=100000, stock=5)
        db.session.add(sample)
        db.session.commit()

        with app.test_client() as test_client:
            yield test_client


def test_get_books(client):
    """Mục tiêu 1: Lấy danh sách sách và kiểm tra format Resource Representation"""
    res = client.get("/api/v1/books")
    assert res.status_code == 200
    data = res.get_json()
    assert "data" in data
    assert len(data["data"]) >= 1

    first_book = data["data"][0]
    # Kiểm tra format ID dạng 'book_...' và nested price object
    assert first_book["id"].startswith("book_")
    assert "price" in first_book
    assert first_book["price"]["currency"] == "VND"


def test_create_book_validation_fail(client):
    """Mục tiêu 2: Test validate bằng JSON Schema khi thiếu trường title -> phải trả 400"""
    res = client.post("/api/v1/books", json={"price_vnd": 200000})
    assert res.status_code == 400
    data = res.get_json()
    assert data["error"] == "validation_failed"


def test_create_book_success(client):
    """Mục tiêu 2: Test tạo sách hợp lệ -> trả 201 Created"""
    payload = {
        "title": "Refactoring",
        "isbn": "9780201485677",
        "price_vnd": 480000,
        "stock": 10
    }
    res = client.post("/api/v1/books", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Refactoring"
    assert data["id"].startswith("book_")


def test_get_book_detail(client):
    """Test lấy chi tiết 1 cuốn sách"""
    res = client.get("/api/v1/books/1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["id"] == "book_1"


def test_get_book_not_found(client):
    """Test lấy sách không tồn tại -> trả về 404"""
    res = client.get("/api/v1/books/9999")
    assert res.status_code == 404
