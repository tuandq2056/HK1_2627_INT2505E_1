from pathlib import Path
from flask import Flask, jsonify
from models import db, Book
from routes.books import books_bp


def create_app(test_config=None):
    app = Flask(__name__)
    db_path = Path(__file__).resolve().parent / "bookstore.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    # Khởi tạo db với Flask app
    db.init_app(app)

    # Đăng ký Blueprint books
    app.register_blueprint(books_bp)

    @app.route("/")
    def index():
        return jsonify({
            "message": "Welcome to Bookstore API - Lab 1",
            "endpoints": {
                "list_books": "GET /api/v1/books",
                "create_book": "POST /api/v1/books",
                "get_book": "GET /api/v1/books/<id>"
            }
        })

    # Tạo bảng và nạp 2 cuốn sách mẫu nếu DB mới tạo (chỉ khi không phải TESTING)
    if not app.config.get("TESTING"):
        with app.app_context():
            db.create_all()
            if not Book.query.first():
            book1 = Book(
                title="Clean Code",
                isbn="9780132350884",
                price_vnd=450000,
                stock=10
            )
            book2 = Book(
                title="The Pragmatic Programmer",
                isbn="9780201616224",
                price_vnd=520000,
                stock=5
            )
            db.session.add_all([book1, book2])
            db.session.commit()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
