#!/bin/bash

echo "curl -i http://127.0.0.1:5000/books"
curl -i http://127.0.0.1:5000/books
echo -e "\n\n"

echo "curl -i http://127.0.0.1:5000/books/999"
curl -i http://127.0.0.1:5000/books/999
echo -e "\n\n"

echo 'curl -i -X POST localhost:5000/books -H "Content-Type: application/json" -d '\''{"title":"DDIA","author":"Kleppmann", "year":2020}'\'
curl -i -X POST localhost:5000/books -H "Content-Type: application/json" -d '{"title":"DDIA","author":"Kleppmann", "year":2020}'
echo -e "\n\n"

echo 'curl -i -X PUT localhost:5000/books/1 -H "Content-Type: application/json" -d '\''{"title":"CC 2nd ed.", "author": "R. Martin", "year":2008}'\'
curl -i -X PUT localhost:5000/books/1 -H "Content-Type: application/json" -d '{"title":"CC 2nd ed.", "author": "R. Martin", "year":2008}'
echo -e "\n\n"

echo "curl -i -X DELETE localhost:5000/books/2"
curl -i -X DELETE localhost:5000/books/2
echo -e "\n\n"

echo 'curl -i -X POST localhost:5000/books -H "Content-Type: application/json" -d '\''{}'\'
curl -i -X POST localhost:5000/books -H "Content-Type: application/json" -d '{}'
echo -e "\n\n"

echo 'curl -i "http://127.0.0.1:5000/books?q=python"'
curl -i "http://127.0.0.1:5000/books?q=python"
echo -e "\n\n"

echo 'curl -i "http://127.0.0.1:5000/books?sort=title"'
curl -i "http://127.0.0.1:5000/books?sort=title"
echo -e "\n\n"

echo 'curl -i -X POST localhost:5000/books -H "Content-Type: application/json" -d '\''{"title":"Sách Cổ","author":"Ai đó", "year":1899}'\'
curl -i -X POST localhost:5000/books -H "Content-Type: application/json" -d '{"title":"Sách Cổ","author":"Ai đó", "year":1899}'
echo -e "\n\n"