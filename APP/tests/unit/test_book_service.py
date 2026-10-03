import pytest
from unittest.mock import MagicMock
from services import book_service
from errors import NotFoundError, ValidationError, ConflictError

def test_get_book_detail_success():
    fake_db = MagicMock()
    fake_row = {"id": 1, "title": "Sách Mock", "author": "Tác giả Mock", "etag": "abc_mock"}
    book_service.book_repo.find_book_by_id = MagicMock(return_value=fake_row)
    
    book_dict, etag = book_service.get_book_detail(fake_db, 1)
    
    assert etag == "abc_mock"
    assert "etag" not in book_dict
    assert book_dict["title"] == "Sách Mock"
    book_service.book_repo.find_book_by_id.assert_called_once_with(fake_db, 1)

def test_get_book_detail_not_found():
    fake_db = MagicMock()
    book_service.book_repo.find_book_by_id = MagicMock(return_value=None)
    
    with pytest.raises(NotFoundError):
        book_service.get_book_detail(fake_db, 999)

def test_get_books_list_pagination_math():
    fake_db = MagicMock()
    book_service.book_repo.count_books = MagicMock(return_value=25)
    book_service.book_repo.find_books = MagicMock(return_value=[])
    
    result = book_service.get_books_list(fake_db, page=1, size=10, filters={})
    
    assert result["pagination"]["total"] == 25
    assert result["pagination"]["total_pages"] == 3
    book_service.book_repo.find_books.assert_called_once_with(fake_db, {}, 10, 0)

def test_get_books_list_negative_page():
    fake_db = MagicMock()
    book_service.book_repo.count_books = MagicMock(return_value=25)
    book_service.book_repo.find_books = MagicMock(return_value=[])
    
    result = book_service.get_books_list(fake_db, page=-5, size=10, filters={})
    
    assert result["pagination"]["page"] == 1
    book_service.book_repo.find_books.assert_called_once_with(fake_db, {}, 10, 0)

def test_get_books_list_hateoas_links():
    fake_db = MagicMock()
    book_service.book_repo.count_books = MagicMock(return_value=25)
    book_service.book_repo.find_books = MagicMock(return_value=[])
    
    result_page1 = book_service.get_books_list(fake_db, page=1, size=10, filters={})
    links_1 = result_page1["_links"]
    assert "self" in links_1
    assert "next" in links_1
    assert "prev" not in links_1
    
    result_page3 = book_service.get_books_list(fake_db, page=3, size=10, filters={})
    links_3 = result_page3["_links"]
    assert "prev" in links_3
    assert "next" not in links_3

def test_create_book_validation_year():
    fake_db = MagicMock()
    book_service.book_repo.insert_book = MagicMock()
    
    with pytest.raises(ValidationError):
        book_service.create_book(fake_db, {"title": "X", "author": "Y", "published_year": 1800})
    book_service.book_repo.insert_book.assert_not_called()

def test_create_book_generates_etag():
    fake_db = MagicMock()
    book_service.book_repo.insert_book = MagicMock(return_value=1)
    
    payload = {"title": "X", "author": "Y", "published_year": 2024}
    book, etag = book_service.create_book(fake_db, payload)
    
    assert etag is not None
    assert len(etag) > 0
    args = book_service.book_repo.insert_book.call_args[0]
    assert args[1] == "X"
    assert args[4] == etag

def test_update_book_success():
    fake_db = MagicMock()
    fake_row = {"title": "Old", "author": "Old", "published_year": 2020, "etag": "old_etag"}
    book_service.book_repo.find_book_by_id = MagicMock(return_value=fake_row)
    book_service.book_repo.update_book = MagicMock()
    
    book, new_etag = book_service.update_book(fake_db, 1, {"title": "New"}, "old_etag")
    
    assert book["title"] == "New"
    assert book["author"] == "Old"
    assert new_etag != "old_etag"
    book_service.book_repo.update_book.assert_called_once()

def test_update_book_not_found():
    fake_db = MagicMock()
    book_service.book_repo.find_book_by_id = MagicMock(return_value=None)
    
    with pytest.raises(NotFoundError):
        book_service.update_book(fake_db, 999, {}, "etag")

def test_update_book_conflict():
    fake_db = MagicMock()
    fake_row = {"title": "Old", "author": "Old", "published_year": 2020, "etag": "db_etag"}
    book_service.book_repo.find_book_by_id = MagicMock(return_value=fake_row)
    
    with pytest.raises(ConflictError):
        book_service.update_book(fake_db, 1, {}, "wrong_etag_from_client")

def test_delete_book_success():
    fake_db = MagicMock()
    fake_row = {"id": 1}
    book_service.book_repo.find_book_by_id = MagicMock(return_value=fake_row)
    book_service.book_repo.delete_book = MagicMock()
    
    book_service.delete_book(fake_db, 1)
    book_service.book_repo.delete_book.assert_called_once_with(fake_db, 1)

def test_delete_book_not_found():
    fake_db = MagicMock()
    book_service.book_repo.find_book_by_id = MagicMock(return_value=None)
    
    with pytest.raises(NotFoundError):
        book_service.delete_book(fake_db, 999)
