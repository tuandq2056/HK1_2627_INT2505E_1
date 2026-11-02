import os

from flask import Flask

from .api.products import products_bp
from .config import DefaultConfig
from .errors import register_error_handlers
from .extensions import db, migrate
from .logging_config import configure_logging


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config or os.environ.get("APP_CONFIG") or DefaultConfig)
    app.json.sort_keys = False

    db.init_app(app)
    migrate.init_app(app, db)

    configure_logging(app)
    register_error_handlers(app)

    app.register_blueprint(products_bp)
    return app
