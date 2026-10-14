import math
from flask import Flask, jsonify, request

app = Flask(__name__)

FAKE_PRODUCTS = [
    {
        "id": i,
        "name": f"Bàn phím cơ Model {i}",
        "price": 500000 + i * 10000,
        "category": "Gear",
    }
    for i in range(1, 26)
]


@app.get("/api/v1/products")
def get_products():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 5))
    except ValueError:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Các tham số 'page' và 'limit' phải là số nguyên dương.",
                }
            ),
            400,
        )

    if page < 1 or limit < 1:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "'page' và 'limit' phải lớn hơn hoặc bằng 1.",
                }
            ),
            400,
        )

    limit = min(limit,10)
    limit = max(limit, 1)
    total_items = len(FAKE_PRODUCTS)
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 1

    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_data = FAKE_PRODUCTS[start_index:end_index]

    has_next = page < total_pages
    has_prev = page > 1

    next_url = (
        f"/api/v1/products?page={page + 1}&limit={limit}" if has_next else None
    )
    prev_url = (
        f"/api/v1/products?page={page - 1}&limit={limit}" if has_prev else None
    )

    response = {
        "status": "success",
        "data": paginated_data,
        "pagination": {
            "current_page": page,
            "limit": limit,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_prev": has_prev,
        },
        "links": {
            "self": f"/api/v1/products?page={page}&limit={limit}",
            "next": next_url,
            "prev": prev_url,
        },
    }

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)