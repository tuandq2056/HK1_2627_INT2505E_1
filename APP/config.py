import os

# DATABASE ABS PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "app.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "db", "schema.sql")

#CONFIG 
DEFAULT_SIZE = 20
MAX_SIZE = 100
