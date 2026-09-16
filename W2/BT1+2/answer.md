``` bash
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl  localhost:5000/all_books
{
  "data": [],
  "length": 0
}
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl -X POST http://localhost:5000/books   -H "Content-Type: application/json"   -d '{"title":"Dế Mèn Phiêu Lưu Ký","author":"Tô Hoài","published_year":1941}'
{
  "author": "T\u00f4 Ho\u00e0i",
  "id": 1,
  "published_year": 1941,
  "title": "D\u1ebf M\u00e8n Phi\u00eau L\u01b0u K\u00fd"
}
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl  localhost:5000/all_books
{
  "data": [
    {
      "author": "T\u00f4 Ho\u00e0i",
      "id": 1,
      "published_year": 1941,
      "title": "D\u1ebf M\u00e8n Phi\u00eau L\u01b0u K\u00fd"
    }
  ],
  "length": 1
}
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl -X PATCH http://localhost:5000/books/1   -H "Content-Type: application/json"   -d '{"title":"Dế Mèn Phiêu Lưu Ký","author":"Tô Hoài","published_year":1940}'
{
  "author": "T\u00f4 Ho\u00e0i",
  "id": 1,
  "published_year": 1940,
  "title": "D\u1ebf M\u00e8n Phi\u00eau L\u01b0u K\u00fd"
}
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl  localhost:5000/all_books
{
  "data": [
    {
      "author": "T\u00f4 Ho\u00e0i",
      "id": 1,
      "published_year": 1940,
      "title": "D\u1ebf M\u00e8n Phi\u00eau L\u01b0u K\u00fd"
    }
  ],
  "length": 1
}
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl  localhost:5000/all_books
{
  "data": [],
  "length": 0
}
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl -X POST http://localhost:5000/books   -H "Content-Type: application/json"   -d '{"title":"Dế Mèn Phiêu Lưu Ký","author":"Tô Hoài","published_year":1941}'
{
  "author": "T\u00f4 Ho\u00e0i",
  "id": 1,
  "published_year": 1941,
  "title": "D\u1ebf M\u00e8n Phi\u00eau L\u01b0u K\u00fd"
}
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl  localhost:5000/all_books
{
  "data": [
    {
      "author": "T\u00f4 Ho\u00e0i",
      "id": 1,
      "published_year": 1941,
      "title": "D\u1ebf M\u00e8n Phi\u00eau L\u01b0u K\u00fd"
    }
  ],
  "length": 1
}
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl -X PATCH http://localhost:5000/books/1   -H "Content-Type: application/json"   -d '{"title":"Dế Mèn Phiêu Lưu Ký","author":"Tô Hoài","published_year":1940}'
{
  "author": "T\u00f4 Ho\u00e0i",
  "id": 1,
  "published_year": 1940,
  "title": "D\u1ebf M\u00e8n Phi\u00eau L\u01b0u K\u00fd"
}
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl  localhost:5000/all_books
{
  "data": [
    {
      "author": "T\u00f4 Ho\u00e0i",
      "id": 1,
      "published_year": 1940,
      "title": "D\u1ebf M\u00e8n Phi\u00eau L\u01b0u K\u00fd"
    }
  ],
  "length": 1
}
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl -X DELETE http://localhost:5000/books/1
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl  localhost:5000/all_books
{
  "data": [],
  "length": 0
}

```