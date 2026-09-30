from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

API_V1_PREFIX = "/api/v1"

MOCK_POSTS = [
    {"id": "1", "title": "Flask API Design", "author_id": 1, "content": "A guide to Flask API design."},
    {"id": "2", "title": "RESTful Principles", "author_id": 2, "content": "Core REST principles explained."},
    {"id": "3", "title": "Python Decorators", "author_id": 3, "content": "Understanding decorators in Python."},
    {"id": "4", "title": "Database Transactions", "author_id": 4, "content": "ACID and transaction management."},
]

MOCK_COMMENTS = [
    {"id": "101", "post_id": "1", "author_id": 2, "content": "Great article!"},
    {"id": "102", "post_id": "1", "author_id": 3, "content": "Thanks for sharing."},
    {"id": "103", "post_id": "2", "author_id": 1, "content": "Very helpful."},
]


@app.get(f"{API_V1_PREFIX}/posts")
def get_posts():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    author_id = request.args.get("author_id", type=int)

    filtered = MOCK_POSTS
    if author_id is not None:
        filtered = [p for p in filtered if p["author_id"] == author_id]

    total = len(filtered)
    start = (page - 1) * limit
    end = start + limit
    paginated = filtered[start:end]

    return jsonify({
        "data": paginated,
        "meta": {
            "page": page,
            "limit": limit,
            "total": total
        }
    }), 200


@app.post(f"{API_V1_PREFIX}/posts")
def create_post():
    data = request.get_json()

    if not data or not data.get("title") or not data.get("content"):
        return jsonify({"error": {"code": 400, "message": "Missing title or content"}}), 400

    new_post = {
        "id": str(len(MOCK_POSTS) + 1),
        "title": data["title"],
        "content": data["content"],
        "author_id": data.get("author_id")
    }
    MOCK_POSTS.append(new_post)

    return jsonify({"data": new_post}), 201


@app.get(f"{API_V1_PREFIX}/posts/<string:post_id>")
def get_post(post_id):
    post = next((p for p in MOCK_POSTS if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": {"code": 404, "message": "Post not found"}}), 404

    return jsonify({"data": post}), 200


@app.put(f"{API_V1_PREFIX}/posts/<string:post_id>")
def update_post(post_id):
    post = next((p for p in MOCK_POSTS if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": {"code": 404, "message": "Post not found"}}), 404

    data = request.get_json()
    if not data or not data.get("title") or not data.get("content"):
        return jsonify({"error": {"code": 400, "message": "PUT requires title and content"}}), 400

    post["title"] = data["title"]
    post["content"] = data["content"]
    if "author_id" in data:
        post["author_id"] = data["author_id"]

    return jsonify({"data": post}), 200


@app.patch(f"{API_V1_PREFIX}/posts/<string:post_id>")
def partial_update_post(post_id):
    post = next((p for p in MOCK_POSTS if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": {"code": 404, "message": "Post not found"}}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": {"code": 400, "message": "Request body is empty"}}), 400

    if "title" in data:
        post["title"] = data["title"]
    if "content" in data:
        post["content"] = data["content"]
    if "author_id" in data:
        post["author_id"] = data["author_id"]

    return jsonify({"data": post}), 200


@app.delete(f"{API_V1_PREFIX}/posts/<string:post_id>")
def delete_post(post_id):
    post = next((p for p in MOCK_POSTS if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": {"code": 404, "message": "Post not found"}}), 404

    MOCK_POSTS.remove(post)

    return make_response("", 204)


@app.get(f"{API_V1_PREFIX}/posts/<string:post_id>/comments")
def get_post_comments(post_id):
    post = next((p for p in MOCK_POSTS if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": {"code": 404, "message": "Post not found"}}), 404

    comments = [c for c in MOCK_COMMENTS if c["post_id"] == post_id]

    return jsonify({"data": comments}), 200


@app.post(f"{API_V1_PREFIX}/posts/<string:post_id>/comments")
def add_post_comment(post_id):
    post = next((p for p in MOCK_POSTS if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": {"code": 404, "message": "Post not found"}}), 404

    data = request.get_json()
    if not data or not data.get("content"):
        return jsonify({"error": {"code": 400, "message": "Comment content missing"}}), 400

    new_comment = {
        "id": str(len(MOCK_COMMENTS) + 1),
        "post_id": post_id,
        "author_id": data.get("author_id"),
        "content": data["content"]
    }
    MOCK_COMMENTS.append(new_comment)

    return jsonify({"data": new_comment}), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)
