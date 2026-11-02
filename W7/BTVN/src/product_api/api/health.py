from flask import Blueprint, current_app
from sqlalchemy import text

from ..extensions import db

health_bp = Blueprint("health", __name__, url_prefix="")


# Liveness — "process còn sống không?" Không chạm DB:
# DB chết không phải lý do để restart API.
@health_bp.get("/healthz")
def liveness():
    return {"status": "ok"}, 200


# Readiness — "nhận traffic được chưa?" Kiểm tra dependency (DB).
# 503 → orchestrator ngừng gửi traffic nhưng KHÔNG restart.
@health_bp.get("/ready")
def readiness():
    checks = {}
    try:
        db.session.execute(text("SELECT 1"))
        checks["db"] = "ok"
    except Exception as exc:  # noqa: BLE001
        db.session.rollback()
        checks["db"] = "error"
        current_app.logger.warning("readiness: db check failed: %s", exc.__class__.__name__)

    ok = all(v == "ok" for v in checks.values())
    return {"status": "ok" if ok else "degraded", "checks": checks}, (200 if ok else 503)
