from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
import bcrypt
import os

app = Flask(__name__)
app.config.update(
    JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY", "dev-only-change-me-0123456789abcdef"),
    JWT_ACCESS_TOKEN_EXPIRES=900,        # 15 phút (minh họa)
    JWT_REFRESH_TOKEN_EXPIRES=2592000,   # 30 ngày (minh họa)
    JWT_ALGORITHM="HS256",
)
jwt = JWTManager(app)

# Demo: dùng dict thay cho DB
_users = {
    "an@vnu.edu.vn": {
        "id": 1,
        "pwd_hash": bcrypt.hashpw(b"correct horse battery staple", bcrypt.gensalt()),
        "roles": ["user"],
        "scopes": ["orders:read"],
    }
}
_orders = {"1": ["o-001", "o-002"]}

# Blocklist thu hồi jti (demo in-memory, thực tế dùng Redis)
_revoked = set()


@jwt.token_in_blocklist_loader
def check_revoked(_header, claims):
    return claims["jti"] in _revoked


def load_permissions(uid):
    for u in _users.values():
        if str(u["id"]) == str(uid):
            return {"roles": u["roles"], "scopes": u["scopes"]}
    return {"roles": [], "scopes": []}


# Login — cấp access + refresh kèm claims
@app.post("/api/auth/login")
def login():
    body = request.get_json(silent=True) or {}
    user = _users.get(body.get("email"))
    pwd = body.get("password", "").encode()
    if not user or not bcrypt.checkpw(pwd, user["pwd_hash"]):
        return jsonify(error="invalid_credentials"), 401
    claims = load_permissions(user["id"])
    uid = str(user["id"])
    return jsonify(
        access=create_access_token(identity=uid, additional_claims=claims),
        refresh=create_refresh_token(identity=uid, additional_claims=claims),
    )


# Protected — check scope từ claims
@app.get("/api/orders")
@jwt_required()
def list_orders():
    uid = get_jwt_identity()
    claims = get_jwt()
    if "orders:read" not in claims.get("scopes", []):
        return jsonify(error="insufficient_scope"), 403
    return jsonify(orders=_orders.get(uid, []))


# Refresh — chấp nhận refresh token, cấp access mới
@app.post("/api/auth/refresh")
@jwt_required(refresh=True)
def refresh():
    uid = get_jwt_identity()
    claims = load_permissions(uid)
    return jsonify(access=create_access_token(identity=uid, additional_claims=claims))


# Logout — thu hồi token đang dùng
@app.post("/api/auth/logout")
@jwt_required(verify_type=False)
def logout():
    _revoked.add(get_jwt()["jti"])
    return jsonify(msg="revoked")


if __name__ == "__main__":
    app.run(debug=True)
