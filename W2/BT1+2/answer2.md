
``` bash
=== 1. Test phân trang (page=2, size=10) ===
HTTP/1.1 200 OK
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Fri, 18 Sep 2026 14:02:59 GMT
Content-Type: application/json
Content-Length: 1775
Cache-Control: public, max-age=30
Connection: close

{
  "_links": {
    "first": {
      "href": "/books?page=1&size=10"
    },
    "last": {
      "href": "/books?page=3&size=10"
    },
    "next": {
      "href": "/books?page=3&size=10"
    },
    "prev": {
      "href": "/books?page=1&size=10"
    },
    "self": {
      "href": "/books?page=2&size=10"
    }
  },
  "data": [
    {
      "author": "Robert C. Martin",
      "id": 11,
      "published_year": 2011,
      "title": "Clean Code Ph\u1ea7n 11"
    },
    {
      "author": "Orwell",
      "id": 12,
      "published_year": 2012,
      "title": "Clean Architecture Ph\u1ea7n 12"
    },
    {
      "author": "Robert C. Martin",
      "id": 13,
      "published_year": 2013,
      "title": "Clean Code Ph\u1ea7n 13"
    },
    {
      "author": "Orwell",
      "id": 14,
      "published_year": 2014,
      "title": "Clean Architecture Ph\u1ea7n 14"
    },
    {
      "author": "Robert C. Martin",
      "id": 15,
      "published_year": 2015,
      "title": "Clean Code Ph\u1ea7n 15"
    },
    {
      "author": "Orwell",
      "id": 16,
      "published_year": 2016,
      "title": "Clean Architecture Ph\u1ea7n 16"
    },
    {
      "author": "Robert C. Martin",
      "id": 17,
      "published_year": 2017,
      "title": "Clean Code Ph\u1ea7n 17"
    },
    {
      "author": "Orwell",
      "id": 18,
      "published_year": 2018,
      "title": "Clean Architecture Ph\u1ea7n 18"
    },
    {
      "author": "Robert C. Martin",
      "id": 19,
      "published_year": 2019,
      "title": "Clean Code Ph\u1ea7n 19"
    },
    {
      "author": "Orwell",
      "id": 20,
      "published_year": 2020,
      "title": "Clean Architecture Ph\u1ea7n 20"
    }
  ],
  "pagination": {
    "page": 2,
    "size": 10,
    "total": 25,
    "total_pages": 3
  }
}



=== 2. Test lọc theo tác giả (author=Orwell) ===
HTTP/1.1 200 OK
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Fri, 18 Sep 2026 14:02:59 GMT
Content-Type: application/json
Content-Length: 1949
Cache-Control: public, max-age=30
Connection: close

{
  "_links": {
    "first": {
      "href": "/books?page=1&size=20&author=Orwell"
    },
    "last": {
      "href": "/books?page=1&size=20&author=Orwell"
    },
    "self": {
      "href": "/books?page=1&size=20&author=Orwell"
    }
  },
  "data": [
    {
      "author": "Orwell",
      "id": 2,
      "published_year": 2002,
      "title": "Clean Architecture Ph\u1ea7n 2"
    },
    {
      "author": "Orwell",
      "id": 4,
      "published_year": 2004,
      "title": "Clean Architecture Ph\u1ea7n 4"
    },
    {
      "author": "Orwell",
      "id": 6,
      "published_year": 2006,
      "title": "Clean Architecture Ph\u1ea7n 6"
    },
    {
      "author": "Orwell",
      "id": 8,
      "published_year": 2008,
      "title": "Clean Architecture Ph\u1ea7n 8"
    },
    {
      "author": "Orwell",
      "id": 10,
      "published_year": 2010,
      "title": "Clean Architecture Ph\u1ea7n 10"
    },
    {
      "author": "Orwell",
      "id": 12,
      "published_year": 2012,
      "title": "Clean Architecture Ph\u1ea7n 12"
    },
    {
      "author": "Orwell",
      "id": 14,
      "published_year": 2014,
      "title": "Clean Architecture Ph\u1ea7n 14"
    },
    {
      "author": "Orwell",
      "id": 16,
      "published_year": 2016,
      "title": "Clean Architecture Ph\u1ea7n 16"
    },
    {
      "author": "Orwell",
      "id": 18,
      "published_year": 2018,
      "title": "Clean Architecture Ph\u1ea7n 18"
    },
    {
      "author": "Orwell",
      "id": 20,
      "published_year": 2020,
      "title": "Clean Architecture Ph\u1ea7n 20"
    },
    {
      "author": "Orwell",
      "id": 22,
      "published_year": 2022,
      "title": "Clean Architecture Ph\u1ea7n 22"
    },
    {
      "author": "Orwell",
      "id": 24,
      "published_year": 2024,
      "title": "Clean Architecture Ph\u1ea7n 24"
    }
  ],
  "pagination": {
    "page": 1,
    "size": 20,
    "total": 12,
    "total_pages": 1
  }
}



=== 3. Test tìm kiếm tiêu đề (q=clean) ===
HTTP/1.1 200 OK
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Fri, 18 Sep 2026 14:02:59 GMT
Content-Type: application/json
Content-Length: 3080
Cache-Control: public, max-age=30
Connection: close

{
  "_links": {
    "first": {
      "href": "/books?page=1&size=20&q=clean"
    },
    "last": {
      "href": "/books?page=2&size=20&q=clean"
    },
    "next": {
      "href": "/books?page=2&size=20&q=clean"
    },
    "self": {
      "href": "/books?page=1&size=20&q=clean"
    }
  },
  "data": [
    {
      "author": "Robert C. Martin",
      "id": 1,
      "published_year": 2001,
      "title": "Clean Code Ph\u1ea7n 1"
    },
    {
      "author": "Orwell",
      "id": 2,
      "published_year": 2002,
      "title": "Clean Architecture Ph\u1ea7n 2"
    },
    {
      "author": "Robert C. Martin",
      "id": 3,
      "published_year": 2003,
      "title": "Clean Code Ph\u1ea7n 3"
    },
    {
      "author": "Orwell",
      "id": 4,
      "published_year": 2004,
      "title": "Clean Architecture Ph\u1ea7n 4"
    },
    {
      "author": "Robert C. Martin",
      "id": 5,
      "published_year": 2005,
      "title": "Clean Code Ph\u1ea7n 5"
    },
    {
      "author": "Orwell",
      "id": 6,
      "published_year": 2006,
      "title": "Clean Architecture Ph\u1ea7n 6"
    },
    {
      "author": "Robert C. Martin",
      "id": 7,
      "published_year": 2007,
      "title": "Clean Code Ph\u1ea7n 7"
    },
    {
      "author": "Orwell",
      "id": 8,
      "published_year": 2008,
      "title": "Clean Architecture Ph\u1ea7n 8"
    },
    {
      "author": "Robert C. Martin",
      "id": 9,
      "published_year": 2009,
      "title": "Clean Code Ph\u1ea7n 9"
    },
    {
      "author": "Orwell",
      "id": 10,
      "published_year": 2010,
      "title": "Clean Architecture Ph\u1ea7n 10"
    },
    {
      "author": "Robert C. Martin",
      "id": 11,
      "published_year": 2011,
      "title": "Clean Code Ph\u1ea7n 11"
    },
    {
      "author": "Orwell",
      "id": 12,
      "published_year": 2012,
      "title": "Clean Architecture Ph\u1ea7n 12"
    },
    {
      "author": "Robert C. Martin",
      "id": 13,
      "published_year": 2013,
      "title": "Clean Code Ph\u1ea7n 13"
    },
    {
      "author": "Orwell",
      "id": 14,
      "published_year": 2014,
      "title": "Clean Architecture Ph\u1ea7n 14"
    },
    {
      "author": "Robert C. Martin",
      "id": 15,
      "published_year": 2015,
      "title": "Clean Code Ph\u1ea7n 15"
    },
    {
      "author": "Orwell",
      "id": 16,
      "published_year": 2016,
      "title": "Clean Architecture Ph\u1ea7n 16"
    },
    {
      "author": "Robert C. Martin",
      "id": 17,
      "published_year": 2017,
      "title": "Clean Code Ph\u1ea7n 17"
    },
    {
      "author": "Orwell",
      "id": 18,
      "published_year": 2018,
      "title": "Clean Architecture Ph\u1ea7n 18"
    },
    {
      "author": "Robert C. Martin",
      "id": 19,
      "published_year": 2019,
      "title": "Clean Code Ph\u1ea7n 19"
    },
    {
      "author": "Orwell",
      "id": 20,
      "published_year": 2020,
      "title": "Clean Architecture Ph\u1ea7n 20"
    }
  ],
  "pagination": {
    "page": 1,
    "size": 20,
    "total": 25,
    "total_pages": 2
  }
}



=== 4. Test lấy tất cả (kèm header Accept: application/json) để check caching ===
HTTP/1.1 200 OK
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Fri, 18 Sep 2026 14:02:59 GMT
Content-Type: application/json
Content-Length: 3048
Cache-Control: public, max-age=30
Connection: close

{
  "_links": {
    "first": {
      "href": "/books?page=1&size=20"
    },
    "last": {
      "href": "/books?page=2&size=20"
    },
    "next": {
      "href": "/books?page=2&size=20"
    },
    "self": {
      "href": "/books?page=1&size=20"
    }
  },
  "data": [
    {
      "author": "Robert C. Martin",
      "id": 1,
      "published_year": 2001,
      "title": "Clean Code Ph\u1ea7n 1"
    },
    {
      "author": "Orwell",
      "id": 2,
      "published_year": 2002,
      "title": "Clean Architecture Ph\u1ea7n 2"
    },
    {
      "author": "Robert C. Martin",
      "id": 3,
      "published_year": 2003,
      "title": "Clean Code Ph\u1ea7n 3"
    },
    {
      "author": "Orwell",
      "id": 4,
      "published_year": 2004,
      "title": "Clean Architecture Ph\u1ea7n 4"
    },
    {
      "author": "Robert C. Martin",
      "id": 5,
      "published_year": 2005,
      "title": "Clean Code Ph\u1ea7n 5"
    },
    {
      "author": "Orwell",
      "id": 6,
      "published_year": 2006,
      "title": "Clean Architecture Ph\u1ea7n 6"
    },
    {
      "author": "Robert C. Martin",
      "id": 7,
      "published_year": 2007,
      "title": "Clean Code Ph\u1ea7n 7"
    },
    {
      "author": "Orwell",
      "id": 8,
      "published_year": 2008,
      "title": "Clean Architecture Ph\u1ea7n 8"
    },
    {
      "author": "Robert C. Martin",
      "id": 9,
      "published_year": 2009,
      "title": "Clean Code Ph\u1ea7n 9"
    },
    {
      "author": "Orwell",
      "id": 10,
      "published_year": 2010,
      "title": "Clean Architecture Ph\u1ea7n 10"
    },
    {
      "author": "Robert C. Martin",
      "id": 11,
      "published_year": 2011,
      "title": "Clean Code Ph\u1ea7n 11"
    },
    {
      "author": "Orwell",
      "id": 12,
      "published_year": 2012,
      "title": "Clean Architecture Ph\u1ea7n 12"
    },
    {
      "author": "Robert C. Martin",
      "id": 13,
      "published_year": 2013,
      "title": "Clean Code Ph\u1ea7n 13"
    },
    {
      "author": "Orwell",
      "id": 14,
      "published_year": 2014,
      "title": "Clean Architecture Ph\u1ea7n 14"
    },
    {
      "author": "Robert C. Martin",
      "id": 15,
      "published_year": 2015,
      "title": "Clean Code Ph\u1ea7n 15"
    },
    {
      "author": "Orwell",
      "id": 16,
      "published_year": 2016,
      "title": "Clean Architecture Ph\u1ea7n 16"
    },
    {
      "author": "Robert C. Martin",
      "id": 17,
      "published_year": 2017,
      "title": "Clean Code Ph\u1ea7n 17"
    },
    {
      "author": "Orwell",
      "id": 18,
      "published_year": 2018,
      "title": "Clean Architecture Ph\u1ea7n 18"
    },
    {
      "author": "Robert C. Martin",
      "id": 19,
      "published_year": 2019,
      "title": "Clean Code Ph\u1ea7n 19"
    },
    {
      "author": "Orwell",
      "id": 20,
      "published_year": 2020,
      "title": "Clean Architecture Ph\u1ea7n 20"
    }
  ],
  "pagination": {
    "page": 1,
    "size": 20,
    "total": 25,
    "total_pages": 2
  }
}



=== 5. Test Sorting (Sắp xếp theo năm xuất bản giảm dần) ===
HTTP/1.1 200 OK
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Fri, 18 Sep 2026 14:02:59 GMT
Content-Type: application/json
Content-Length: 3182
Cache-Control: public, max-age=30
Connection: close

{
  "_links": {
    "first": {
      "href": "/books?page=1&size=20&sort=published_year&order=desc"
    },
    "last": {
      "href": "/books?page=2&size=20&sort=published_year&order=desc"
    },
    "next": {
      "href": "/books?page=2&size=20&sort=published_year&order=desc"
    },
    "self": {
      "href": "/books?page=1&size=20&sort=published_year&order=desc"
    }
  },
  "data": [
    {
      "author": "Robert C. Martin",
      "id": 25,
      "published_year": 2025,
      "title": "Clean Code Ph\u1ea7n 25"
    },
    {
      "author": "Orwell",
      "id": 24,
      "published_year": 2024,
      "title": "Clean Architecture Ph\u1ea7n 24"
    },
    {
      "author": "Robert C. Martin",
      "id": 23,
      "published_year": 2023,
      "title": "Clean Code Ph\u1ea7n 23"
    },
    {
      "author": "Orwell",
      "id": 22,
      "published_year": 2022,
      "title": "Clean Architecture Ph\u1ea7n 22"
    },
    {
      "author": "Robert C. Martin",
      "id": 21,
      "published_year": 2021,
      "title": "Clean Code Ph\u1ea7n 21"
    },
    {
      "author": "Orwell",
      "id": 20,
      "published_year": 2020,
      "title": "Clean Architecture Ph\u1ea7n 20"
    },
    {
      "author": "Robert C. Martin",
      "id": 19,
      "published_year": 2019,
      "title": "Clean Code Ph\u1ea7n 19"
    },
    {
      "author": "Orwell",
      "id": 18,
      "published_year": 2018,
      "title": "Clean Architecture Ph\u1ea7n 18"
    },
    {
      "author": "Robert C. Martin",
      "id": 17,
      "published_year": 2017,
      "title": "Clean Code Ph\u1ea7n 17"
    },
    {
      "author": "Orwell",
      "id": 16,
      "published_year": 2016,
      "title": "Clean Architecture Ph\u1ea7n 16"
    },
    {
      "author": "Robert C. Martin",
      "id": 15,
      "published_year": 2015,
      "title": "Clean Code Ph\u1ea7n 15"
    },
    {
      "author": "Orwell",
      "id": 14,
      "published_year": 2014,
      "title": "Clean Architecture Ph\u1ea7n 14"
    },
    {
      "author": "Robert C. Martin",
      "id": 13,
      "published_year": 2013,
      "title": "Clean Code Ph\u1ea7n 13"
    },
    {
      "author": "Orwell",
      "id": 12,
      "published_year": 2012,
      "title": "Clean Architecture Ph\u1ea7n 12"
    },
    {
      "author": "Robert C. Martin",
      "id": 11,
      "published_year": 2011,
      "title": "Clean Code Ph\u1ea7n 11"
    },
    {
      "author": "Orwell",
      "id": 10,
      "published_year": 2010,
      "title": "Clean Architecture Ph\u1ea7n 10"
    },
    {
      "author": "Robert C. Martin",
      "id": 9,
      "published_year": 2009,
      "title": "Clean Code Ph\u1ea7n 9"
    },
    {
      "author": "Orwell",
      "id": 8,
      "published_year": 2008,
      "title": "Clean Architecture Ph\u1ea7n 8"
    },
    {
      "author": "Robert C. Martin",
      "id": 7,
      "published_year": 2007,
      "title": "Clean Code Ph\u1ea7n 7"
    },
    {
      "author": "Orwell",
      "id": 6,
      "published_year": 2006,
      "title": "Clean Architecture Ph\u1ea7n 6"
    }
  ],
  "pagination": {
    "page": 1,
    "size": 20,
    "total": 25,
    "total_pages": 2
  }
}



=== 6. Test Tìm kiếm mở rộng (q tìm trong cả title và author) ===
HTTP/1.1 200 OK
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Fri, 18 Sep 2026 14:02:59 GMT
Content-Type: application/json
Content-Length: 2092
Cache-Control: public, max-age=30
Connection: close

{
  "_links": {
    "first": {
      "href": "/books?page=1&size=20&q=robert"
    },
    "last": {
      "href": "/books?page=1&size=20&q=robert"
    },
    "self": {
      "href": "/books?page=1&size=20&q=robert"
    }
  },
  "data": [
    {
      "author": "Robert C. Martin",
      "id": 25,
      "published_year": 2025,
      "title": "Clean Code Ph\u1ea7n 25"
    },
    {
      "author": "Robert C. Martin",
      "id": 23,
      "published_year": 2023,
      "title": "Clean Code Ph\u1ea7n 23"
    },
    {
      "author": "Robert C. Martin",
      "id": 21,
      "published_year": 2021,
      "title": "Clean Code Ph\u1ea7n 21"
    },
    {
      "author": "Robert C. Martin",
      "id": 19,
      "published_year": 2019,
      "title": "Clean Code Ph\u1ea7n 19"
    },
    {
      "author": "Robert C. Martin",
      "id": 17,
      "published_year": 2017,
      "title": "Clean Code Ph\u1ea7n 17"
    },
    {
      "author": "Robert C. Martin",
      "id": 15,
      "published_year": 2015,
      "title": "Clean Code Ph\u1ea7n 15"
    },
    {
      "author": "Robert C. Martin",
      "id": 13,
      "published_year": 2013,
      "title": "Clean Code Ph\u1ea7n 13"
    },
    {
      "author": "Robert C. Martin",
      "id": 11,
      "published_year": 2011,
      "title": "Clean Code Ph\u1ea7n 11"
    },
    {
      "author": "Robert C. Martin",
      "id": 9,
      "published_year": 2009,
      "title": "Clean Code Ph\u1ea7n 9"
    },
    {
      "author": "Robert C. Martin",
      "id": 7,
      "published_year": 2007,
      "title": "Clean Code Ph\u1ea7n 7"
    },
    {
      "author": "Robert C. Martin",
      "id": 5,
      "published_year": 2005,
      "title": "Clean Code Ph\u1ea7n 5"
    },
    {
      "author": "Robert C. Martin",
      "id": 3,
      "published_year": 2003,
      "title": "Clean Code Ph\u1ea7n 3"
    },
    {
      "author": "Robert C. Martin",
      "id": 1,
      "published_year": 2001,
      "title": "Clean Code Ph\u1ea7n 1"
    }
  ],
  "pagination": {
    "page": 1,
    "size": 20,
    "total": 13,
    "total_pages": 1
  }
}

```