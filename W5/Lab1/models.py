from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """Author entity representing book authors."""
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)

    def __init__(self, name: str = "", bio: str | None = None, **kwargs):
        """Initialize Author instance."""
        super().__init__()
        self.name = name
        self.bio = bio
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        """Serialize Author to dictionary representation."""
        return {
            "id": f"author_{self.id}",
            "raw_id": self.id,
            "name": self.name,
            "bio": self.bio,
        }


class Book(db.Model):
    """Book entity representing bookstore inventory."""
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=True)
    genre = db.Column(db.String(50), default="tech")
    price_vnd = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, default=0)

    def __init__(
        self,
        title: str = "",
        isbn: str | None = None,
        genre: str = "tech",
        price_vnd: int = 0,
        stock: int = 0,
        **kwargs,
    ):
        """Initialize Book instance."""
        super().__init__()
        self.title = title
        self.isbn = isbn
        self.genre = genre
        self.price_vnd = price_vnd
        self.stock = stock
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        """Serialize Book entity to REST API resource representation."""
        return {
            "id": f"book_{self.id}",
            "raw_id": self.id,
            "title": self.title,
            "isbn": self.isbn,
            "genre": self.genre,
            "price": {
                "amount": self.price_vnd,
                "currency": "VND",
            },
            "price_vnd": self.price_vnd,
            "stock": self.stock,
            "inStock": self.stock > 0,
        }
