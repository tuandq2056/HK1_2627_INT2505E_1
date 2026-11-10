from flask import Blueprint, jsonify

from extensions import db

from .models import Product

health_bp = Blueprint("health", __name__)


# liveness — không đụng DB
@health_bp.get("/healthz")
def liveness():
    return jsonify({"status": "ok"}), 200


# readiness — thử query DB qua ORM
@health_bp.get("/ready")
def readiness():
    try:
        db.session.execute(db.select(Product).limit(1))
        return jsonify({"status": "ok", "db": "ok"}), 200
    except Exception:
        return jsonify({"status": "degraded", "db": "error"}), 503
