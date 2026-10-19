import pytest
from app import create_app
from models import db, Book


@pytest.fixture
def client():
    """Create test application client with in-memory SQLite database."""
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})

    with app.app_context():
        db.create_all()
        for idx in range(1, 16):
            b = Book(
                title=f"Book {idx}",
                isbn=f"9780000000{idx:03d}",
                price_vnd=100000 + idx * 10000,
                stock=5,
            )
            db.session.add(b)
        db.session.commit()

        with app.test_client() as test_client:
            yield test_client

        db.session.remove()
        db.drop_all()


def test_get_books(client):
    """Retrieve book list and verify resource representation format."""
    res = client.get("/api/v1/books")
    assert res.status_code == 200
    data = res.get_json()
    assert "data" in data
    assert len(data["data"]) >= 1

    first_book = data["data"][0]
    assert first_book["id"].startswith("book_")
    assert "price" in first_book
    assert first_book["price"]["currency"] == "VND"


def test_cursor_pagination(client):
    """Test cursor pagination navigation across pages."""
    res_page1 = client.get("/api/v1/books?limit=5")
    assert res_page1.status_code == 200
    page1 = res_page1.get_json()
    assert len(page1["data"]) == 5
    assert page1["page"]["has_more"] is True
    assert page1["page"]["next_cursor"] is not None

    next_cursor = page1["page"]["next_cursor"]
    res_page2 = client.get(f"/api/v1/books?limit=5&cursor={next_cursor}")
    assert res_page2.status_code == 200
    page2 = res_page2.get_json()
    assert len(page2["data"]) == 5

    page1_ids = [item["raw_id"] for item in page1["data"]]
    page2_ids = [item["raw_id"] for item in page2["data"]]
    assert set(page1_ids).isdisjoint(set(page2_ids))


def test_invalid_cursor(client):
    """Test that malformed cursor returns 400 Bad Request."""
    res = client.get("/api/v1/books?cursor=invalid_base64_value")
    assert res.status_code == 400
    data = res.get_json()
    assert data["error"] == "invalid_cursor"


def test_create_book_validation_fail(client):
    """Test JSON Schema validation failure on missing required fields."""
    res = client.post("/api/v1/books", json={"price_vnd": 200000})
    assert res.status_code == 400
    data = res.get_json()
    assert data["error"] == "validation_failed"


def test_create_book_success(client):
    """Test creating a valid book."""
    payload = {
        "title": "Refactoring",
        "isbn": "9780201485677",
        "price_vnd": 480000,
        "stock": 10,
    }
    res = client.post("/api/v1/books", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Refactoring"
    assert data["id"].startswith("book_")


def test_get_book_detail(client):
    """Test fetching single book details."""
    res = client.get("/api/v1/books/1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["id"] == "book_1"


def test_get_book_not_found(client):
    """Test fetching non-existent book returns 404."""
    res = client.get("/api/v1/books/9999")
    assert res.status_code == 404
