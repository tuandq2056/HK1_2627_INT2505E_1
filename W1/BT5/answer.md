
``` bash
(.venv) tuanlala@fedora:~/INT_3505E_1/W1/BT5$ curl -X DELETE http://127.0.0.1:5000/books/66e46ec0-e935-4e5e-892b-c57e7122ad4c -v
*   Trying 127.0.0.1:5000...
* Established connection to 127.0.0.1 (127.0.0.1 port 5000) from 127.0.0.1 port 40194 
* using HTTP/1.x
> DELETE /books/66e46ec0-e935-4e5e-892b-c57e7122ad4c HTTP/1.1
> Host: 127.0.0.1:5000
> User-Agent: curl/8.18.0
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 404 NOT FOUND
< Server: Werkzeug/3.1.8 Python/3.14.7
< Date: Sat, 12 Sep 2026 15:54:45 GMT
< Content-Type: application/json
< Content-Length: 32
< Connection: close
< 
{
  "error": "Book not found"
}
* shutting down connection #0 ```