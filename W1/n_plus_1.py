from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memory.db'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    book = db.relationship('Book', backref=db.backref('orders', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'quantity': self.quantity,
            'book': self.book.to_dict() if self.book else None
        }


with app.app_context():
    db.create_all()

    books = [
        Book(title="The Great Gatsby", author="F. Scott Fitzgerald", year=1925),
        Book(title="To Kill a Mockingbird", author="Harper Lee", year=1960),
        Book(title="1984", author="George Orwell", year=1949),
    ]

    db.session.add_all(books)
    db.session.commit()

    o1 = Order(book_id=1, quantity=2)
    o2 = Order(book_id=2, quantity=1)
    db.session.add_all([o1, o2])
    db.session.commit()

    print("Initial data added to the database.")

@app.route('/bad_request')
def bad_request():
    print("A bad API was called and a n+1 problem was detected.")
    orders = Order.query.all()
    result = []
    for order in orders:
        book = Book.query.get(order.book_id)  # This will cause an N+1 problem
        result.append({
            'order_id': order.id,
            'book_title': book.title if book else None,
            'quantity': order.quantity
        })
    return jsonify(result), 200

@app.route('/good_request')
def good_request():
    print("A good API was called and the N+1 problem was avoided.")
    orders = Order.query.options(joinedload(Order.book)).all()
    result = []
    for order in orders:
        result.append({
            'order_id': order.id,
            'book_title': order.book.title if order.book else None,
            'quantity': order.quantity
        })
    return jsonify(result), 200


if __name__ == '__main__':
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.run(host='127.0.0.1', port=5002, debug=True)
