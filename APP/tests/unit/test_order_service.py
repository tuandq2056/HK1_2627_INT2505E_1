import pytest
from unittest.mock import MagicMock
from services import order_service
from errors import NotFoundError, ValidationError

def test_get_order_detail_not_found():
    fake_db = MagicMock()
    order_service.order_repo.find_order_by_id = MagicMock(return_value=None)

    with pytest.raises(NotFoundError):
        order_service.get_order_detail(fake_db, 999)

def test_get_orders_list_pagination_math():
    fake_db = MagicMock()
    order_service.order_repo.count_orders = MagicMock(return_value=25)
    order_service.order_repo.find_orders = MagicMock(return_value=[])

    result = order_service.get_orders_list(fake_db, page=2, size=10, filters={})

    assert result["pagination"]["total_pages"] == 3
    assert "prev" in result["_links"] and "next" in result["_links"]
    order_service.order_repo.find_orders.assert_called_once_with(fake_db, {}, 10, 10)

def test_create_order_default_status():
    fake_db = MagicMock()
    order_service.order_repo.insert_order = MagicMock(return_value=1)

    order = order_service.create_order(fake_db, {"customer_name": "A", "total_price": 50})

    assert order["status"] == "pending"
    order_service.order_repo.insert_order.assert_called_once_with(fake_db, "A", 50, "pending")

@pytest.mark.parametrize("payload", [
    {"total_price": 10},                                         # thiếu customer_name
    {"customer_name": "A", "total_price": -1},                   # giá âm
    {"customer_name": "A", "total_price": "10"},                 # giá không phải số
    {"customer_name": "A", "total_price": True},                 # bool không được tính là số
    {"customer_name": "A", "total_price": 10, "status": "lost"}, # status không hợp lệ
])
def test_create_order_validation(payload):
    fake_db = MagicMock()
    order_service.order_repo.insert_order = MagicMock()

    with pytest.raises(ValidationError):
        order_service.create_order(fake_db, payload)
    order_service.order_repo.insert_order.assert_not_called()

def test_update_order_keeps_missing_fields():
    fake_db = MagicMock()
    fake_row = {"id": 1, "customer_name": "A", "total_price": 50.0, "status": "pending"}
    order_service.order_repo.find_order_by_id = MagicMock(return_value=fake_row)
    order_service.order_repo.update_order = MagicMock(return_value=1)

    updated = order_service.update_order(fake_db, 1, {"status": "paid"})

    assert updated == {"id": 1, "customer_name": "A", "total_price": 50.0, "status": "paid"}
    order_service.order_repo.update_order.assert_called_once_with(fake_db, 1, "A", 50.0, "paid")

def test_delete_order_not_found():
    fake_db = MagicMock()
    order_service.order_repo.find_order_by_id = MagicMock(return_value=None)
    order_service.order_repo.delete_order = MagicMock()

    with pytest.raises(NotFoundError):
        order_service.delete_order(fake_db, 999)
    order_service.order_repo.delete_order.assert_not_called()
