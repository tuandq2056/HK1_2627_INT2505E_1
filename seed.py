import sqlite3

DATABASE = "app.db"

print("Đang khởi tạo database và nạp dữ liệu...")
db = sqlite3.connect(DATABASE)

# 1. Khởi tạo bảng books
db.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        published_year INTEGER
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
    db.execute(
        "INSERT INTO books (id, title, author, published_year) VALUES (?, ?, ?, ?)",
        (i, title, author, year)
    )

db.commit()
db.close()
print("🎉 Đã fill thành công 200 sách vào 'app.db'!")
