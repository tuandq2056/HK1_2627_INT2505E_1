# app.py
from flask import Flask
from flask_smorest import Api
from extensions import db
from api.products import blp as ProductBlueprint  

app = Flask(__name__)

app.config["API_TITLE"] = "Product API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = (
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
)

# Cấu hình SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

api = Api(app)
api.register_blueprint(ProductBlueprint)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)