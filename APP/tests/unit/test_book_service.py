import pytest
from unittest.mock import MagicMock
from services import book_service
from errors import NotFoundError, ValidationError

def test_get_books_list_pagination_math():
    """Test toán học phân trang: tính total_pages và offset"""
    fake_db = MagicMock()
    
    # Mock tổng số sách là 25 cuốn
    book_service.book_repo.count_books = MagicMock(return_value=25)
    # Mock data trả về rỗng (chỉ quan tâm tính toán pagination)
    book_service.book_repo.find_books = MagicMock(return_value=[])
    
    # Yêu cầu trang 1, size 10 -> mong đợi total_pages = 3, gọi offset = 0
    result = book_service.get_books_list(fake_db, page=1, size=10, filters={})
    
    assert result["pagination"]["total"] == 25
    assert result["pagination"]["total_pages"] == 3
    
    # Kiểm tra xem có gọi xuống DB với limit=10, offset=0 không
    # arg thứ 5 là limit, thứ 6 là offset trong hàm find_books(db, where, params, sort, limit, offset)
    book_service.book_repo.find_books.assert_called_once_with(fake_db, "", [], "", 10, 0)

def test_get_books_list_negative_page():
    """Test nếu user lỡ truyền page âm thì phải tự ép về page 1"""
    fake_db = MagicMock()
    book_service.book_repo.count_books = MagicMock(return_value=25)
    book_service.book_repo.find_books = MagicMock(return_value=[])
    
    result = book_service.get_books_list(fake_db, page=-5, size=10, filters={})
    
    assert result["pagination"]["page"] == 1
    # Offset vẫn phải là 0
    book_service.book_repo.find_books.assert_called_once_with(fake_db, "", [], "", 10, 0)

def test_get_books_list_hateoas_links():
    """Test tự động sinh HATEOAS Links"""
    fake_db = MagicMock()
    book_service.book_repo.count_books = MagicMock(return_value=25)
    book_service.book_repo.find_books = MagicMock(return_value=[])
    
    # Đang ở trang 1, size 10 (có 3 trang)
    result_page1 = book_service.get_books_list(fake_db, page=1, size=10, filters={})
    links_1 = result_page1["_links"]
    assert "self" in links_1
    assert "next" in links_1
    assert "prev" not in links_1 # Trang 1 thì ko có prev
    
    # Đang ở trang 3, size 10 (Trang cuối)
    result_page3 = book_service.get_books_list(fake_db, page=3, size=10, filters={})
    links_3 = result_page3["_links"]
    assert "prev" in links_3
    assert "next" not in links_3 # Trang cuối thì ko có next

def test_create_book_validation_year():
    """Test Validation: Năm xuất bản phải hợp lý trước khi lưu DB"""
    fake_db = MagicMock()
    
    # Mock hàm insert để check xem có bị gọi không
    book_service.book_repo.insert_book = MagicMock()
    
    # Cố tình truyền năm xuất bản 1800
    with pytest.raises(ValidationError) as exc:
        book_service.create_book(fake_db, {"title": "X", "author": "Y", "published_year": 1800})
        
    assert "phải lớn hơn hoặc bằng 1900" in str(exc.value).lower()
    # Đảm bảo hàm insert của repo chưa bị gọi (Chặn ngay từ cửa)
    book_service.book_repo.insert_book.assert_not_called()

def test_create_book_generates_etag():
    """Test tính năng tự sinh ETag khi tạo sách"""
    fake_db = MagicMock()
    # Mock repo trả về ID = 1 khi insert
    book_service.book_repo.insert_book = MagicMock(return_value=1)
    
    payload = {"title": "X", "author": "Y", "published_year": 2024}
    book, etag = book_service.create_book(fake_db, payload)
    
    assert etag is not None
    assert len(etag) > 0 # Chắc chắn ETag đã được tạo
    # Kiểm tra xem cái ETag này có được truyền xuống Repo không
    # Gọi với arguments: (db, title, author, year, etag)
    args = book_service.book_repo.insert_book.call_args[0]
    assert args[1] == "X"
    assert args[4] == etag # param etag ở vị trí cuối
