FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app

EXPOSE 5000

# BT4: docker tự gọi /healthz để biết container còn sống không
HEALTHCHECK --interval=10s --timeout=3s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/healthz')"

# Tạo bảng (migration) rồi chạy server
CMD flask db upgrade && gunicorn -b 0.0.0.0:5000 -w 2 "app:create_app()"
