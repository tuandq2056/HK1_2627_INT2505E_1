from flask import Flask, jsonify
from config import BASE_DIR
from db.connection import init_db, close_connection
from routes.books import books_bp
from errors import NotFoundError, ValidationError, ConflictError

app = Flask(__name__)

# Tự động đóng DB sau mỗi Request
app.teardown_appcontext(close_connection)

# Đăng ký các API cho Books
app.register_blueprint(books_bp, url_prefix="/books")

# --- XỬ LÝ LỖI TẬP TRUNG (GLOBAL ERROR HANDLERS) ---
# Dịch các lỗi của tầng Service thành mã HTTP để trả về cho Client

@app.errorhandler(NotFoundError)
def handle_not_found(error):
    return jsonify({"error": str(error)}), 404

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify({"error": str(error)}), 400

@app.errorhandler(ConflictError)
def handle_conflict_error(error):
    return jsonify({"error": str(error)}), 412 # 412 Precondition Failed

if __name__ == '__main__':
    # Khởi tạo bảng nếu chưa có
    init_db(app)
    app.run(debug=True, port=5000)
