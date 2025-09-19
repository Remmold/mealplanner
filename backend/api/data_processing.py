import json
import duckdb
from pathlib import Path

DATABASE_NAME = "groceries.duckdb"
DATA_PATH = Path(__file__).parents[2] / DATABASE_NAME
conn = duckdb.connect(DATA_PATH)

def json_response(query):
    with conn:
        connection_relation_object = conn.query(query=query)
        df = connection_relation_object.df()
        string_containing_json = df.to_json(orient="records")
    return json.loads(string_containing_json) 

