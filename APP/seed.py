import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "app.db")

print(f"Đang khởi tạo database và nạp dữ liệu vào {DATABASE}...")
db = sqlite3.connect(DATABASE)

# 1. Khởi tạo bảng books
db.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        published_year INTEGER,
        etag TEXT
    )
''')
db.commit()

# 2. Xóa sạch dữ liệu cũ
db.execute("DELETE FROM books")

# 3. Nạp 200 cuốn sách
book_titles = [
    ("Clean Code", "Robert C. Martin"),
    ("Clean Architecture", "Robert C. Martin"),
    ("1984", "George Orwell"),
    ("Animal Farm", "George Orwell"),
    ("Design Patterns", "Gang of Four")
]

for i in range(1, 201):
    base_title, author = book_titles[i % 5]
    title = f"{base_title} - Tập {i}"
    year = 1990 + (i % 30)
    etag = f"etag_{i}"
    db.execute(
        "INSERT INTO books (id, title, author, published_year, etag) VALUES (?, ?, ?, ?, ?)",
        (i, title, author, year, etag)
    )

db.commit()
db.close()
print(f"🎉 Đã nạp thành công 200 sách vào '{DATABASE}'!")
