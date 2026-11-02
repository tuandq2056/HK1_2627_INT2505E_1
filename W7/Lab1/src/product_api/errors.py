from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException


class ApiError(Exception):
    """Base — mọi lỗi nghiệp vụ kế thừa class này."""

    status_code = 500
    code = "internal_error"

    def __init__(self, message="", code=None, status=None):
        super().__init__(message)
        if code:
            self.code = code
        if status:
            self.status_code = status
        self.message = message


class NotFound(ApiError):
    status_code = 404
    code = "not_found"


class Conflict(ApiError):
    status_code = 409
    code = "conflict"


class OutOfStock(ApiError):
    status_code = 409
    code = "out_of_stock"


def _error(code, detail, status):
    return jsonify({"error": code, "detail": detail}), status


def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def _on_api(err):
        return _error(err.code, err.message, err.status_code)

    @app.errorhandler(ValidationError)
    def _on_validation(err):
        # Cú pháp JSON đúng nhưng nội dung sai → 422
        return _error("validation_error", err.messages, 422)

    @app.errorhandler(HTTPException)
    def _on_http(err):
        return _error(err.name.lower().replace(" ", "_"), err.description, err.code)

    @app.errorhandler(Exception)
    def _on_unhandled(err):
        app.logger.exception("unhandled")
        return _error("internal_error", "unexpected error", 500)
