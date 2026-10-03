from flask import Flask, jsonify
from config import BASE_DIR
from db.connection import init_db, close_connection
from routes.books import books_bp
from routes.orders import orders_bp
from errors import NotFoundError, ValidationError, ConflictError, ProblemError
from werkzeug.exceptions import HTTPException
import logging
from flask import request

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Tự động đóng DB sau mỗi Request
app.teardown_appcontext(close_connection)

# Đăng ký các API cho Books
app.register_blueprint(books_bp, url_prefix="/books")

# Đăng ký các API cho Orders
app.register_blueprint(orders_bp, url_prefix="/orders")

# --- XỬ LÝ LỖI TẬP TRUNG (GLOBAL ERROR HANDLERS) ---
@app.errorhandler(ProblemError)
def handle_problem_error(error):
    response = jsonify(error.to_dict(req_path=request.path))
    response.status_code = error.status
    response.content_type = "application/problem+json"
    return response

@app.errorhandler(HTTPException)
def handle_http_exception(error):
    response_data = {
        "type": "about:blank",
        "title": error.name,
        "detail": error.description,
        "status": error.code,
        "instance": request.path
    }
    response = jsonify(response_data)
    response.status_code = error.code
    response.content_type = "application/problem+json"
    return response

@app.errorhandler(Exception)
def handle_uncaught_exception(error):
    logger.exception("An uncaught exception occurred:")
    response_data = {
        "type": "about:blank",
        "title": "Internal Server Error",
        "detail": "An unexpected error occurred on the server.",
        "status": 500,
        "instance": request.path
    }
    response = jsonify(response_data)
    response.status_code = 500
    response.content_type = "application/problem+json"
    return response

@app.errorhandler(NotFoundError)
def handle_not_found(error):
    return handle_problem_error(ProblemError(status=404, title="Not Found", detail=str(error)))

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return handle_problem_error(ProblemError(status=400, title="Bad Request", detail=str(error)))

@app.errorhandler(ConflictError)
def handle_conflict_error(error):
    return handle_problem_error(ProblemError(status=412, title="Precondition Failed", detail=str(error)))

if __name__ == '__main__':
    # Khởi tạo bảng nếu chưa có
    init_db(app)
    app.run(debug=True, port=5000)
