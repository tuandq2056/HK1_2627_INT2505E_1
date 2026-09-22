import sqlite3
from flask import g
from config import DATABASE_PATH, SCHEMA_PATH


def get_db():
    """Lấy kết nối Database từ Flask g object. Nếu chưa có kết nối thì tạo mới.
    Hàm này được gọi mỗi khi cần truy vấn Database trong các route."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
        # Ép kiểu dữ liệu trả về thành dictionary thay vì tuple
        db.row_factory = sqlite3.Row
    return db


def close_connection(exception):
    """
    Đóng kết nối Database khi request kết thúc."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db(app):
    """
    Khởi tạo cấu trúc Database bằng cách đọc từ file schema.sql.
    Hàm này được gọi 1 lần khi server vừa start.
    """
    with app.app_context():
        db = get_db()
        with open(SCHEMA_PATH, 'r') as f:
            # executescript() cho phép chạy nhiều lệnh SQL (ngăn cách bởi dấu ;) cùng lúc
            db.executescript(f.read())
        db.commit()
