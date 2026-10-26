from functools import wraps
from flask import g, jsonify
from flask_jwt_extended import get_jwt


# Decorator 1: roles (OR) — coarse
# g.current_user phải được nạp trước (xem before_request trong app.py)
def require_roles(*allowed):
    def d(fn):
        @wraps(fn)
        def w(*a, **kw):
            urs = set(g.current_user["roles"])
            if not urs & set(allowed):
                return jsonify({
                    "error": "forbidden",
                    "need_one_of": list(allowed)
                }), 403
            return fn(*a, **kw)
        return w
    return d


# Decorator 2: scopes (AND) — fine per request
def require_scopes(*needed):
    def d(fn):
        @wraps(fn)
        def w(*a, **kw):
            granted = set(get_jwt().get("scopes", []))
            if not set(needed).issubset(granted):
                return jsonify({
                    "error": "insufficient_scope",
                    "need_all_of": list(needed)
                }), 403
            return fn(*a, **kw)
        return w
    return d


# Decorator 3: ownership — chống BOLA (OWASP API1)
def user_owns_resource(param, store):
    def d(fn):
        @wraps(fn)
        def w(*a, **kw):
            order = store.get(kw[param])
            if order is None:
                return jsonify({"error": "not_found"}), 404
            if order["owner"] != g.current_user["id"] and "admin" not in g.current_user["roles"]:
                return jsonify({"error": "forbidden"}), 403
            return fn(*a, **kw)
        return w
    return d
