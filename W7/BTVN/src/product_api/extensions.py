from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Khai báo ở module-level, chưa gắn app — factory sẽ gọi init_app()
db = SQLAlchemy()
migrate = Migrate()
