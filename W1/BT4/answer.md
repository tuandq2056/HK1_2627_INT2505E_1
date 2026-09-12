``` bash
(.venv) tuanlala@fedora:~/INT_3505E_1$ curl "http://127.0.0.1:5000/books?sort=title&limit=5"
{
  "items": [
    {
      "author": "T\u00f4 Ho\u00e0i",
      "id": "49452e84-4758-489b-b0d3-7c9ea4bf5e43",
      "published_year": 1941,
      "title": "D\u1ebf M\u00e8n Phi\u00eau L\u01b0u K\u00fd"
    },
    {
      "author": "Guido van Rossum",
      "id": "72dc312a-07de-4691-919f-bf3569248d13",
      "published_year": 2020,
      "title": "L\u1eadp Tr\u00ecnh Python C\u01a1 B\u1ea3n"
    },
    {
      "author": "Miguel Grinberg",
      "id": "46326f4f-aecc-4272-8578-db8a596b3a58",
      "published_year": 2018,
      "title": "Flask Web Development"
    },
    {
      "author": "Luciano Ramalho",
      "id": "4b00e133-5565-43f1-b273-5ef37f6bfa22",
      "published_year": 2022,
      "title": "H\u1ecdc Python N\u00e2ng Cao"
    },
    {
      "author": "Ng\u00f4 T\u1ea5t T\u1ed1",
      "id": "c520c287-c1c7-439f-a908-5f739b3bd61b",
      "published_year": 1939,
      "title": "T\u1eaft \u0110\u00e8n"
    }
  ]
}
```