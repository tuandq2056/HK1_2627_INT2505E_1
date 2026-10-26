import os
from flask import Flask, g, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

from auth import require_roles, require_scopes, user_owns_resource

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY", "dev-only-change-me-0123456789abcdef")
JWTManager(app)

# Demo: dict thay cho DB (mật khẩu plaintext chỉ để demo RBAC, xem Ex1/Ex2 cho bcrypt)
USERS = {
    1: {"id": 1, "name": "an", "password": "an123",
        "roles": ["user"], "scopes": ["orders:read"]},
    2: {"id": 2, "name": "binh", "password": "binh123",
        "roles": ["manager"], "scopes": ["orders:read", "orders:write"]},
    3: {"id": 3, "name": "admin", "password": "admin123",
        "roles": ["admin"], "scopes": ["orders:read", "orders:write"]},
}
ORDERS = {
    1: {"id": 1, "owner": 1, "item": "book"},
    2: {"id": 2, "owner": 2, "item": "pen"},
}


@app.post("/api/auth/login")
def login():
    body = request.get_json(silent=True) or {}
    user = next((u for u in USERS.values() if u["name"] == body.get("name")), None)
    if not user or user["password"] != body.get("password"):
        return jsonify(error="invalid_credentials"), 401
    token = create_access_token(
        identity=str(user["id"]),
        additional_claims={"roles": user["roles"], "scopes": user["scopes"]})
    return jsonify(access=token)


# Middleware: nạp g.current_user từ token
@app.before_request
def load_current_user():
    from flask_jwt_extended import verify_jwt_in_request
    verify_jwt_in_request(optional=True)
    uid = get_jwt_identity()
    g.current_user = USERS.get(int(uid)) if uid else None


@app.get("/api/orders/<int:id>")
@jwt_required()
@require_scopes("orders:read")
@user_owns_resource("id", ORDERS)
def get_order(id):
    return jsonify(ORDERS[id])


# 3 lớp check chồng lên một route
@app.delete("/api/orders/<int:id>")
@jwt_required()
@require_roles("admin", "manager")
@require_scopes("orders:write")
@user_owns_resource("id", ORDERS)
def delete_order(id):
    ORDERS.pop(id)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
