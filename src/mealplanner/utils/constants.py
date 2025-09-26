from pathlib import Path

# API
BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = "/groceries/"

# OLAP Database
DATABASE_NAME = "groceries.duckdb"
DATA_PATH = Path(__file__).parents[1] / "backend" / "data" / DATABASE_NAME
