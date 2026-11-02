import os
import sys

# Cho phép chạy trực tiếp từ thư mục project mà chưa cần `pip install -e .`
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from product_api.factory import create_app  # noqa: E402

app = create_app()
