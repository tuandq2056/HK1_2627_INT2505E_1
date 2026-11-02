import os

bind = "0.0.0.0:5000"
workers = int(os.environ.get("GUNICORN_WORKERS", 2))  # điều chỉnh theo CPU
worker_class = "sync"
timeout = 60
graceful_timeout = 30
keepalive = 5
preload_app = False  # mỗi worker tự mở connection pool riêng
accesslog = "-"
errorlog = "-"
loglevel = "info"
proc_name = "product-api"
