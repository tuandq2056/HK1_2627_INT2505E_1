from pathlib import Path
from flask import Flask, jsonify
from models import db, Book
from routes.books import books_bp


def create_app(test_config=None):
    """Create and configure the Flask application instance."""
    app = Flask(__name__)
    db_path = Path(__file__).resolve().parent / "bookstore.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    app.register_blueprint(books_bp)

    @app.route("/")
    def index():
        """Root endpoint returning service status and route map."""
        return jsonify({
            "message": "Welcome to Bookstore API - Homework 2",
            "endpoints": {
                "list_books": "GET /api/v1/books",
                "create_book": "POST /api/v1/books",
                "get_book": "GET /api/v1/books/<id>",
            }
        })

    if not app.config.get("TESTING"):
        with app.app_context():
            db.create_all()
            if not Book.query.first():
                sample_books = [
                    Book(title="Clean Code", isbn="9780132350884", genre="tech", price_vnd=450000, stock=10),
                    Book(title="The Pragmatic Programmer", isbn="9780201616224", genre="tech", price_vnd=520000, stock=5),
                    Book(title="Refactoring", isbn="9780201485677", genre="tech", price_vnd=480000, stock=8),
                    Book(title="Domain-Driven Design", isbn="9780321125217", genre="tech", price_vnd=550000, stock=3),
                    Book(title="1984", isbn="9780451524935", genre="fiction", price_vnd=150000, stock=20),
                    Book(title="Brave New World", isbn="9780060850524", genre="fiction", price_vnd=180000, stock=12),
                    Book(title="Dune", isbn="9780441172719", genre="sci-fi", price_vnd=320000, stock=15),
                ]
                db.session.add_all(sample_books)
                db.session.commit()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
