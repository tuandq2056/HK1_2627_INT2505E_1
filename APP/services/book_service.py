import hashlib
from repos import book_repo
from errors import NotFoundError, ValidationError, ConflictError

def make_etag(title: str, author: str, published_year: int) -> str:
    """Sinh ETag bằng cách hash nội dung cuốn sách."""
    raw = f"{title}-{author}-{published_year}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()

def get_book_detail(db, book_id: int):
    """
    Lấy chi tiết sách theo ID.
    Nếu không tìm thấy sách, raise NotFoundError.
    """
    row = book_repo.find_book_by_id(db, book_id)
    if not row:
        raise NotFoundError(f"Không tìm thấy sách có ID = {book_id}!")
    
    book_dict = {k: row[k] for k in row.keys() if k != "etag"}
    return book_dict, row["etag"]

from config import DEFAULT_SIZE, MAX_SIZE

def get_books_list(db, page: int = 1, size: int = DEFAULT_SIZE, filters: dict = None):
    """
    Lấy danh sách sách theo phân trang và filter.
    Trả về dictionary chứa data, pagination info và HATEOAS links.
    """
    # 1. Xử lý toán học cơ bản
    page = max(page, 1) # Ép page âm về 1
    if size <= 0 or size > MAX_SIZE:
        size = DEFAULT_SIZE
    
    # 2. Tính toán Pagination
    # (Việc dịch filters thành SQL là trách nhiệm của tầng Repo)
    total = book_repo.count_books(db, filters)
    total_pages = max((total + size - 1) // size, 1) if size > 0 else 1
    offset = (page - 1) * size
    
    # 3. Lấy data
    rows = book_repo.find_books(db, filters, size, offset)
    items = [{k: row[k] for k in row.keys() if k != "etag"} for row in rows]
    
    # 4. Sinh HATEOAS Links
    def build_url(p):
        return f"/books?page={p}&size={size}"
        
    links = {
        "self": {"href": build_url(page)},
        "first": {"href": build_url(1)},
        "last": {"href": build_url(total_pages)}
    }
    if page > 1:
        links["prev"] = {"href": build_url(page - 1)}
    if page < total_pages:
        links["next"] = {"href": build_url(page + 1)}
        
    return {
        "data": items,
        "pagination": {"page": page, "size": size, "total": total, "total_pages": total_pages},
        "_links": links
    }

def create_book(db, payload: dict):
    """
    Tạo sách mới.
    Thực hiện validation trước khi gọi Repo để insert.
    """
    title = payload.get("title")
    author = payload.get("author")
    year = payload.get("published_year")
    
    # Business Validation
    if not title or not author:
        raise ValidationError("title và author là bắt buộc.")
    if type(year) is not int or year < 1900:
        raise ValidationError("published_year phải lớn hơn hoặc bằng 1900.")
        
    etag = make_etag(title, author, year)
    
    # Gọi Repo để Insert
    new_id = book_repo.insert_book(db, title, author, year, etag)
    
    new_book = {
        "id": new_id,
        "title": title,
        "author": author,
        "published_year": year
    }
    return new_book, etag


def update_book(db, book_id: int, payload: dict, if_match_etag: str):
    """
    Cập nhật sách theo ID.
    Thực hiện validation trước khi gọi Repo để update.
    """
    # 1. Lấy sách hiện tại
    row = book_repo.find_book_by_id(db, book_id)
    if not row:
        raise NotFoundError(f"Không tìm thấy sách có ID = {book_id}!")
    
    # 2. Kiểm tra ETag
    current_etag = row["etag"]
    if current_etag != if_match_etag:
        raise ConflictError("ETag không khớp. Vui lòng tải lại dữ liệu.")
    
    # 3. Lấy dữ liệu mới từ payload
    title = payload.get("title", row["title"])
    author = payload.get("author", row["author"])
    year = payload.get("published_year", row["published_year"])
    
    # 4. Business Validation
    if not title or not author:
        raise ValidationError("title và author là bắt buộc.")
    if type(year) is not int or year < 1900:
        raise ValidationError("published_year phải lớn hơn hoặc bằng 1900.")
        
    new_etag = make_etag(title, author, year)
    
    # 5. Gọi Repo để Update
    book_repo.update_book(db, book_id, title, author, year, new_etag)
    
    updated_book = {
        "id": book_id,
        "title": title,
        "author": author,
        "published_year": year
    }
    return updated_book, new_etag

def delete_book(db, book_id: int):
    """
    Xóa sách theo ID.
    Nếu không tìm thấy sách, raise NotFoundError.
    """
    row = book_repo.find_book_by_id(db, book_id)
    if not row:
        raise NotFoundError(f"Không tìm thấy sách có ID = {book_id}!")
    
    book_repo.delete_book(db, book_id)