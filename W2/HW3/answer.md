``` bash
(.venv) tuanlala@192:~/INT_3505E_1/W2/BT1+2$ curl -i -H "If-None-Match: 663dead1348b68da300fbba06a1a11a1" http://127.0.0.1:5000/books/1
HTTP/1.1 304 NOT MODIFIED
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Mon, 21 Sep 2026 14:23:11 GMT
ETag: 663dead1348b68da300fbba06a1a11a1
Connection: close
```
