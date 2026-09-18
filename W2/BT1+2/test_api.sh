#!/bin/bash

# Đảm bảo app.py đang chạy ở background hoặc một terminal khác (mặc định ở cổng 5000)
BASE_URL="http://127.0.0.1:5000"

echo "=== 1. Test phân trang (page=2, size=10) ==="
curl -i "$BASE_URL/books?page=2&size=10"
echo -e "\n\n"

echo "=== 2. Test lọc theo tác giả (author=Orwell) ==="
curl -i "$BASE_URL/books?author=Orwell"
echo -e "\n\n"

echo "=== 3. Test tìm kiếm tiêu đề (q=clean) ==="
curl -i "$BASE_URL/books?q=clean"
echo -e "\n\n"

echo "=== 4. Test lấy tất cả (kèm header Accept: application/json) để check caching ==="
curl -i -H "Accept: application/json" "$BASE_URL/books"
echo -e "\n\n"

echo "=== 5. Test Sorting (Sắp xếp theo năm xuất bản giảm dần) ==="
curl -i "$BASE_URL/books?sort=published_year&order=desc"
echo -e "\n\n"

echo "=== 6. Test Tìm kiếm mở rộng (q tìm trong cả title và author) ==="
curl -i "$BASE_URL/books?q=robert"
echo -e "\n\n"
