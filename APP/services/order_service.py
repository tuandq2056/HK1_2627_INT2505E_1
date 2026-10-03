from repos import order_repo
from errors import NotFoundError, ValidationError
from config import DEFAULT_SIZE, MAX_SIZE

VALID_STATUSES = {"pending", "paid", "shipped", "cancelled"}

def _validate(customer_name, total_price, status):
    """Business Validation dùng chung cho create và update."""
    if not customer_name or not isinstance(customer_name, str):
        raise ValidationError("customer_name là bắt buộc.")
    # bool là subclass của int nên phải loại riêng
    if isinstance(total_price, bool) or not isinstance(total_price, (int, float)) or total_price < 0:
        raise ValidationError("total_price phải là số không âm.")
    if status not in VALID_STATUSES:
        raise ValidationError(f"status phải là một trong: {', '.join(sorted(VALID_STATUSES))}.")

def _to_dict(row):
    return {k: row[k] for k in row.keys()}

def get_order_detail(db, order_id: int):
    """
    Lấy chi tiết đơn hàng theo ID.
    Nếu không tìm thấy, raise NotFoundError.
    """
    row = order_repo.find_order_by_id(db, order_id)
    if not row:
        raise NotFoundError(f"Không tìm thấy đơn hàng có ID = {order_id}!")
    return _to_dict(row)

def get_orders_list(db, page: int = 1, size: int = DEFAULT_SIZE, filters: dict = None):
    """
    Lấy danh sách đơn hàng theo phân trang và filter.
    Trả về dictionary chứa data, pagination info và HATEOAS links.
    """
    page = max(page, 1)
    if size <= 0 or size > MAX_SIZE:
        size = DEFAULT_SIZE

    total = order_repo.count_orders(db, filters)
    total_pages = max((total + size - 1) // size, 1)
    offset = (page - 1) * size

    rows = order_repo.find_orders(db, filters, size, offset)
    items = [_to_dict(row) for row in rows]

    def build_url(p):
        return f"/orders?page={p}&size={size}"

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

def create_order(db, payload: dict):
    """
    Tạo đơn hàng mới. Mặc định status = "pending".
    """
    customer_name = payload.get("customer_name")
    total_price = payload.get("total_price")
    status = payload.get("status", "pending")

    _validate(customer_name, total_price, status)

    new_id = order_repo.insert_order(db, customer_name, total_price, status)
    return {
        "id": new_id,
        "customer_name": customer_name,
        "total_price": total_price,
        "status": status
    }

def update_order(db, order_id: int, payload: dict):
    """
    Cập nhật đơn hàng theo ID. Trường nào không gửi lên sẽ giữ nguyên giá trị cũ.
    """
    row = order_repo.find_order_by_id(db, order_id)
    if not row:
        raise NotFoundError(f"Không tìm thấy đơn hàng có ID = {order_id}!")

    customer_name = payload.get("customer_name", row["customer_name"])
    total_price = payload.get("total_price", row["total_price"])
    status = payload.get("status", row["status"])

    _validate(customer_name, total_price, status)

    order_repo.update_order(db, order_id, customer_name, total_price, status)
    return {
        "id": order_id,
        "customer_name": customer_name,
        "total_price": total_price,
        "status": status
    }

def delete_order(db, order_id: int):
    """
    Xóa đơn hàng theo ID.
    Nếu không tìm thấy, raise NotFoundError.
    """
    row = order_repo.find_order_by_id(db, order_id)
    if not row:
        raise NotFoundError(f"Không tìm thấy đơn hàng có ID = {order_id}!")

    order_repo.delete_order(db, order_id)
