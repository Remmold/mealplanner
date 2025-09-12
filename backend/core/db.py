import os
import duckdb

# Allow overriding DB path with env var for flexibility in dev vs CI
DB_PATH = os.getenv("MEALPLANNER_DB", "groceries.duckdb")

def get_connection(read_only: bool = True):
    """Return a duckdb connection. Set read_only=False if you need write access."""
    return duckdb.connect(DB_PATH, read_only=read_only)
