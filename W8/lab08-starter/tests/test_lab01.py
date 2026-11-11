"""LAB 1 — add your five tests here. Do not delete the smoke tests.

A. GET /books, empty database -> HTTP 200 and []
B. GET /books/9999 -> HTTP 404, JSON code == NOT_FOUND
C. POST /books with only author -> HTTP 400, errors contains title
D. POST valid book, DELETE it, GET same id -> HTTP 404
BONUS. Validate a Book response using JSON Schema; add an unknown
       field to a *copy* of the response and assert ValidationError.

Useful imports:
    from jsonschema import validate, ValidationError
    import pytest
    from tools import get_book_schema

Do not depend on test execution order. Fixtures: client, app, sample_book.
"""

import copy
import pytest
from jsonschema import ValidationError, validate
from tools import get_book_schema


def test_list_books_empty(client):
    response = client.get("/books")
    assert response.status_code == 200
    body = response.get_json()
    assert body is not None
    assert body == []


def test_get_unknown_book(client):
    response = client.get("/books/9999")
    assert response.status_code == 404
    assert response.get_json()["code"] == "NOT_FOUND"


def test_create_book_without_title(client):
    response = client.post("/books", json={"author": "J.J. Geewax"})
    assert response.status_code == 400
    body = response.get_json()
    assert "title" in [e["field"] for e in body["errors"]]


def test_deleted_book(client):
    created = client.post("/books", json={"title": "Book", "author": "Author"})
    assert created.status_code == 201
    book_id = created.get_json()["id"]

    assert client.delete(f"/books/{book_id}").status_code == 204
    assert client.get(f"/books/{book_id}").status_code == 404


"""

ALLOWED_FIELDS = {"id", "title", "author", "year", "isbn"}


def find_extra_fields(response_json):
    extra = []
    for field in response_json:
        allowed = field in ALLOWED_FIELDS
        print(f"  check field {field!r}: {'OK' if allowed else 'NOT ALLOWED'}")
        if not allowed:
            extra.append(field)
    return extra


def test_response_extra_field_blocked(client, sample_book):
    book = client.get(f"/books/{sample_book}").get_json()

    print("\n[1] real response:", book)
    assert find_extra_fields(book) == []      

    leaked = dict(book)                       
    leaked["password_hash"] = "pbkdf2:sha256:secret"
    print("[2] simulated leaked response:", leaked)
    extra = find_extra_fields(leaked)

    print("[3] extra fields found:", extra)
    assert extra == ["password_hash"]            
"""


def test_response_extra_field_blocked_jsonschema(client, sample_book):
    schema = copy.deepcopy(get_book_schema())
    schema["properties"]["year"] = {"type": ["integer", "null"]}
    schema["properties"]["isbn"] = {"type": ["string", "null"], "pattern": r"^\d{13}$"}

    book = client.get(f"/books/{sample_book}").get_json()
    validate(book, schema)              

    leaked = dict(book)
    leaked["password_hash"] = "pbkdf2:sha256:secret"
    with pytest.raises(ValidationError, match="password_hash"):
        validate(leaked, schema)              
