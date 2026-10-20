import pytest
from app import create_app
from models import db, Book


@pytest.fixture
def client():
    """Create test application client with in-memory SQLite database and test dataset."""
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})

    with app.app_context():
        db.create_all()

        sample_data = [
            ("Clean Code", "9780132350884", "tech", 450000, 10),
            ("The Pragmatic Programmer", "9780201616224", "tech", 520000, 5),
            ("Refactoring", "9780201485677", "tech", 450000, 8),
            ("Domain-Driven Design", "9780321125217", "tech", 550000, 3),
            ("1984", "9780451524935", "fiction", 150000, 20),
            ("Brave New World", "9780060850524", "fiction", 180000, 12),
            ("Dune", "9780441172719", "sci-fi", 320000, 15),
            ("Foundation", "9780553293357", "sci-fi", 290000, 7),
        ]
        for title, isbn, genre, price_vnd, stock in sample_data:
            db.session.add(Book(title=title, isbn=isbn, genre=genre, price_vnd=price_vnd, stock=stock))
        db.session.commit()

        with app.test_client() as test_client:
            yield test_client

        db.session.remove()
        db.drop_all()


def test_offset_pagination(client):
    """Test offset strategy pagination metadata and slicing."""
    res = client.get("/api/v1/books?strategy=offset&offset=0&limit=3")
    assert res.status_code == 200
    data = res.get_json()
    assert data["pagination"]["strategy"] == "offset"
    assert data["pagination"]["offset"] == 0
    assert data["pagination"]["limit"] == 3
    assert data["pagination"]["total"] == 8
    assert data["pagination"]["has_next"] is True
    assert len(data["data"]) == 3

    res_next = client.get("/api/v1/books?strategy=offset&offset=6&limit=3")
    assert res_next.status_code == 200
    data_next = res_next.get_json()
    assert data_next["pagination"]["has_next"] is False
    assert len(data_next["data"]) == 2


def test_cursor_pagination(client):
    """Test cursor strategy pagination and page-by-page traversal."""
    res_page1 = client.get("/api/v1/books?strategy=cursor&limit=3&sort=id")
    assert res_page1.status_code == 200
    page1 = res_page1.get_json()
    assert page1["pagination"]["strategy"] == "cursor"
    assert len(page1["data"]) == 3
    assert page1["pagination"]["has_more"] is True
    assert page1["pagination"]["next_cursor"] is not None

    cursor = page1["pagination"]["next_cursor"]
    res_page2 = client.get(f"/api/v1/books?strategy=cursor&limit=3&sort=id&cursor={cursor}")
    assert res_page2.status_code == 200
    page2 = res_page2.get_json()
    assert len(page2["data"]) == 3

    ids_page1 = [b["raw_id"] for b in page1["data"]]
    ids_page2 = [b["raw_id"] for b in page2["data"]]
    assert set(ids_page1).isdisjoint(set(ids_page2))


def test_filter_by_genre(client):
    """Test filtering books by genre."""
    res = client.get("/api/v1/books?genre=fiction")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data["data"]) == 2
    for book in data["data"]:
        assert book["genre"] == "fiction"


def test_multi_key_sort(client):
    """Test multi-key sorting (e.g. price descending, title ascending)."""
    res = client.get("/api/v1/books?strategy=offset&sort=-price,title&limit=10")
    assert res.status_code == 200
    data = res.get_json()["data"]

    prices = [b["price_vnd"] for b in data]
    assert prices == sorted(prices, reverse=True)

    same_price_books = [b for b in data if b["price_vnd"] == 450000]
    assert len(same_price_books) == 2
    assert same_price_books[0]["title"] <= same_price_books[1]["title"]


def test_cursor_with_multi_key_sort(client):
    """Test cursor pagination while using multi-key sort."""
    res_p1 = client.get("/api/v1/books?strategy=cursor&sort=-price,title&limit=3")
    assert res_p1.status_code == 200
    p1 = res_p1.get_json()
    assert len(p1["data"]) == 3
    assert p1["pagination"]["has_more"] is True

    cursor = p1["pagination"]["next_cursor"]
    res_p2 = client.get(f"/api/v1/books?strategy=cursor&sort=-price,title&limit=3&cursor={cursor}")
    assert res_p2.status_code == 200
    p2 = res_p2.get_json()
    assert len(p2["data"]) == 3

    p1_ids = [b["raw_id"] for b in p1["data"]]
    p2_ids = [b["raw_id"] for b in p2["data"]]
    assert set(p1_ids).isdisjoint(set(p2_ids))


def test_cursor_sort_changed_rejection(client):
    """Test that changing sort parameter with existing cursor yields 400."""
    res = client.get("/api/v1/books?strategy=cursor&sort=-price&limit=2")
    cursor = res.get_json()["pagination"]["next_cursor"]

    res_tampered = client.get(f"/api/v1/books?strategy=cursor&sort=title&cursor={cursor}")
    assert res_tampered.status_code == 400
    assert res_tampered.get_json()["error"] == "sort_changed"


def test_invalid_parameters(client):
    """Test validation errors for invalid strategy, sort, and cursor."""
    res_strat = client.get("/api/v1/books?strategy=random")
    assert res_strat.status_code == 400
    assert res_strat.get_json()["error"] == "invalid_strategy"

    res_sort = client.get("/api/v1/books?sort=non_existent_column")
    assert res_sort.status_code == 400
    assert res_sort.get_json()["error"] == "bad_sort"

    res_cursor = client.get("/api/v1/books?strategy=cursor&cursor=bad_token")
    assert res_cursor.status_code == 400
    assert res_cursor.get_json()["error"] == "invalid_cursor"


def test_crud_and_schema_validation(client):
    """Test book creation schema validation and retrieval."""
    res_fail = client.post("/api/v1/books", json={"genre": "tech"})
    assert res_fail.status_code == 400
    assert res_fail.get_json()["error"] == "validation_failed"

    res_create = client.post("/api/v1/books", json={
        "title": "Clean Architecture",
        "isbn": "9780134494166",
        "genre": "tech",
        "price_vnd": 490000,
        "stock": 10
    })
    assert res_create.status_code == 201
    created_id = res_create.get_json()["raw_id"]

    res_get = client.get(f"/api/v1/books/{created_id}")
    assert res_get.status_code == 200
    assert res_get.get_json()["title"] == "Clean Architecture"

    res_delete = client.delete(f"/api/v1/books/{created_id}")
    assert res_delete.status_code == 200
