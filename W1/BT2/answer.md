``` bash
(.venv) tuanlala@192:~/INT_3505E_1$  curl -i http://127.0.0.1:5000/health
HTTP/1.1 200 OK
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Wed, 09 Sep 2026 09:42:28 GMT
Content-Type: application/json
Content-Length: 21
Connection: close

{
  "status": "OK"
}
(.venv) tuanlala@192:~/INT_3505E_1$  curl -i http://127.0.0.1:5000/echo -d '{"name" : "Tuan", "age" : 21}'
HTTP/1.1 415 UNSUPPORTED MEDIA TYPE
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Wed, 09 Sep 2026 09:43:25 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 215
Connection: close

<!doctype html>
<html lang=en>
<title>415 Unsupported Media Type</title>
<h1>Unsupported Media Type</h1>
<p>Did not attempt to load JSON data because the request Content-Type was not &#39;application/json&#39;.</p>
(.venv) tuanlala@192:~/INT_3505E_1$  curl -i http://127.0.0.1:5000/echo \ -d '{"name" : "Tuan", "age" : 21}'
HTTP/1.1 405 METHOD NOT ALLOWED
Server: Werkzeug/3.1.8 Python/3.14.7
Date: Wed, 09 Sep 2026 09:43:56 GMT
Content-Type: text/html; charset=utf-8
Allow: OPTIONS, POST
Content-Length: 153
Connection: close

<!doctype html>
<html lang=en>
<title>405 Method Not Allowed</title>
<h1>Method Not Allowed</h1>
<p>The method is not allowed for the requested URL.</p>
curl: (3) URL rejected: Malformed input to a URL function
curl: (3) URL rejected: Malformed input to a URL function
curl: (3) URL rejected: Malformed input to a URL function
(.venv) tuanlala@192:~/INT_3505E_1$  curl -X http://127.0.0.1:5000/echo \ -d '{"name" : "Tuan", "age" : 21}'
curl: (3) URL rejected: Malformed input to a URL function
curl: (3) URL rejected: Malformed input to a URL function
curl: (3) URL rejected: Malformed input to a URL function
(.venv) tuanlala@192:~/INT_3505E_1$  curl -X http://127.0.0.1:5000/echo \-H "Content-Type: application/json" \
 -d '{"name" : "Tuan", "age" : 21}'
curl: (2) no URL specified
curl: try 'curl --help' for more information
(.venv) tuanlala@192:~/INT_3505E_1$ curl -X POST http://127.0.0.1:5000/echo -H "Content-Type: application/json" -d '{"name": "Tuan", "age": 21}'
{
  "age": 21,
  "name": "Tuan"
}
```