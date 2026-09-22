-- Bảng books (có sẵn cột etag)
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    published_year INTEGER,
    etag TEXT
);

-- Bảng orders
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    total_price REAL NOT NULL,
    status TEXT NOT NULL
);
