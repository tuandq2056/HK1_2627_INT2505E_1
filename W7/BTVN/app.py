import os

from flask import Flask, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from api.health import health_bp
from api.orders import orders_bp
from api.products import products_bp
from extensions import db, migrate


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL", "sqlite:///dev.db")
    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(health_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)

    @app.errorhandler(ValidationError)
    def on_validation_error(err):
        return jsonify({"error": "validation_error", "detail": err.messages}), 422

    @app.errorhandler(HTTPException)
    def on_http_error(err):
        return jsonify({"error": err.name.lower().replace(" ", "_"),
                        "detail": err.description}), err.code

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
