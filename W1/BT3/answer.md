``` bash
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl -X POST http://127.0.0.1:5000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Dế Mèn Phiêu Lưu Ký", "author": "Tô Hoài", "published_year": 1941}'
{
  "book": {
    "author": "T\u00f4 Ho\u00e0i",
    "id": "66e46ec0-e935-4e5e-892b-c57e7122ad4c",
    "published_year": 1941,
    "title": "D\u1ebf M\u00e8n Phi\u00eau L\u01b0u K\u00fd"
  },
  "message": "Book created successfully"
}
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl -X POST http://127.0.0.1:5000/books \
  -H "Content-Type: application/json" \
  -d '{title: "Lỗi JSON"}'
{
  "error": "Invalid JSON"
}
```