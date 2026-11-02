import json
import logging
import sys
import time
import uuid

from flask import g, has_request_context, request


class JsonFormatter(logging.Formatter):
    """Một dòng JSON cho mỗi sự kiện log."""

    EXTRA_FIELDS = ("method", "path", "status", "ms")

    def format(self, rec):
        payload = {
            "ts": self.formatTime(rec, "%Y-%m-%dT%H:%M:%S%z"),
            "level": rec.levelname,
            "msg": rec.getMessage(),
        }
        if has_request_context():
            payload["request_id"] = g.get("request_id", "-")
        for key in self.EXTRA_FIELDS:
            if hasattr(rec, key):
                payload[key] = getattr(rec, key)
        if rec.exc_info:
            payload["exc"] = self.formatException(rec.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(app):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    app.logger.handlers = [handler]
    app.logger.setLevel(app.config["LOG_LEVEL"])
    app.logger.propagate = False

    @app.before_request
    def _start_timer():
        g.t0 = time.perf_counter()
        g.request_id = request.headers.get("X-Request-Id") or uuid.uuid4().hex

    @app.after_request
    def _log_request(resp):
        ms = int((time.perf_counter() - g.get("t0", time.perf_counter())) * 1000)
        resp.headers["X-Request-Id"] = g.get("request_id", "-")
        app.logger.info(
            "request done",
            extra={
                "method": request.method,
                "path": request.path,
                "status": resp.status_code,
                "ms": ms,
            },
        )
        return resp
