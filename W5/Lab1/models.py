from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """Entity Author (Slide 16)"""
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)

    def __init__(self, name: str = "", bio: str | None = None, **kwargs):
        super().__init__(name=name, bio=bio, **kwargs)

    def to_dict(self):
        return {
            "id": f"author_{self.id}",
            "raw_id": self.id,
            "name": self.name,
            "bio": self.bio,
        }


class Book(db.Model):
    """Entity Book - Trọng tâm của Lab 1 (Slide 14, 16)"""
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=True)
    price_vnd = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, default=0)

    # Constructor tường minh giúp Pylance/VS Code nhận diện tham số và hỗ trợ autocomplete
    def __init__(
        self,
        title: str = "",
        isbn: str | None = None,
        price_vnd: int = 0,
        stock: int = 0,
        **kwargs,
    ):
        super().__init__(
            title=title,
            isbn=isbn,
            price_vnd=price_vnd,
            stock=stock,
            **kwargs,
        )

    def to_dict(self):
        """
        API Resource Representation (Mục tiêu 1 của Lab 1 - Slide 13, 14):
        Tách biệt DB Schema với dữ liệu JSON trả về cho Client.
        """
        return {
            "id": f"book_{self.id}",
            "raw_id": self.id,
            "title": self.title,
            "isbn": self.isbn,
            "price": {
                "amount": self.price_vnd,
                "currency": "VND",
            },
            "price_vnd": self.price_vnd,
            "stock": self.stock,
            "inStock": self.stock > 0,
        }
