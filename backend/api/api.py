from fastapi import FastAPI
import duckdb
import json
from pathlib import Path

DATABASE_NAME = "groceries.duckdb"
DATA_PATH = Path(__file__).parents[2] / DATABASE_NAME

# Initialize the fastapi object
app = FastAPI()

# Initialize connection to duckdb (opens)
conn = duckdb.connect(DATA_PATH)

# Endpoint for getting grocery data for a selected grocery ????
# Endpoint for getting ALL GROCERIES? 

# Ska url:en "/groceries" verkligen hämta från grocery_nutrient-marten...?

#@app.get("/groceries") 
def fetch_groceries():
    query = """
        SELECT DISTINCT
            number,
            grocery_name,
        FROM mart.mart_grocery_nutrients
    """

    # Opens connection to duckdb
    with conn:
        response = conn.query(query=query).df()
        print(type(response))

    return json.loads(response) 
    


if __name__ == "__main__":
    print(fetch_groceries())