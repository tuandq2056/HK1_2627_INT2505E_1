from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)

API_V1_PREFIX = "/api/v1"
MOCK_POSTS = [
    {"id": str(uuid4()), "title": "Flask API Design", "author_id": 1},
    {"id": str(uuid4()), "title": "RESTful Principles", "author_id": 2},
    {"id": str(uuid4()), "title": "Python Decorators", "author_id": 3},
    {"id": str(uuid4()), "title": "Database Transactions", "author_id": 4},
]


@app.get(f'{API_V1_PREFIX}/posts')
def get_posts():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    author_id = request.args.get('author_id')
    
    return jsonify({
        "data": [
            {"id": str(uuid4()), "title": "Flask API Design", "author_id": 1},
            {"id": str(uuid4()), "title": "RESTful Principles", "author_id": 2}
        ],
        "meta": {
            "page": page,
            "limit": limit,
            "total": 2
        }
    }), 200

@app.post(f'{API_V1_PREFIX}/posts')
def create_post():
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"error": {"code": 400, "message": "Missing title or content"}}), 400
        
    new_post_id = str(uuid4())  
    
    return jsonify({
        "data": {
            "id": new_post_id,
            "title": data['title'],
            "content": data['content']
        }
    }), 201

@app.get(f'{API_V1_PREFIX}/posts/<string:post_id>')
def get_post(post_id):
    return jsonify({
        "data": {
            "id": post_id,
            "title": "Sample Post Title",
            "content": "Full content goes here..."
        }
    }), 200

@app.put(f'{API_V1_PREFIX}/posts/<string:post_id>')
def update_post(post_id):
    data = request.get_json()
    # Logic update Database
    return jsonify({
        "data": {
            "id": post_id,
            "title": data.get('title', 'Updated Title'),
            "updated": True
        }
    }), 200

@app.patch(f'{API_V1_PREFIX}/posts/<string:post_id>')
def partial_update_post(post_id):
    data = request.get_json()
    # Logic update Database
    return jsonify({
        "data": {
            "id": post_id,
            "title": data.get('title', 'Partially Updated Title'),
            "updated": True
        }
    }), 200

@app.delete(f'{API_V1_PREFIX}/posts/<string:post_id>')
def delete_post(post_id):
    """Xóa bài viết"""
    # Logic xóa Database
    return jsonify(), 204 # 204 No Content là chuẩn nhất cho thao tác Xóa thành công


@app.get(f'{API_V1_PREFIX}/posts/<int:post_id>/comments')
def get_post_comments(post_id):
    """Lấy danh sách bình luận của một bài viết cụ thể"""
    return jsonify({
        "data": [
            {"id": 101, "post_id": post_id, "content": "Bài viết hay quá!"},
            {"id": 102, "post_id": post_id, "content": "Thanks for sharing."}
        ]
    }), 200

@app.post(f'{API_V1_PREFIX}/posts/<int:post_id>/comments')
def add_post_comment(post_id):
    """Thêm bình luận mới vào bài viết"""
    data = request.get_json()
    if not data or not data.get('content'):
        return jsonify({"error": {"code": 400, "message": "Comment content missing"}}), 400
        
    return jsonify({
        "data": {
            "id": 103,
            "post_id": post_id,
            "content": data['content']
        }
    }), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)