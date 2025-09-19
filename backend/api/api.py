from fastapi import FastAPI

from backend.api.data_processing import json_response

# Initialize the fastapi object
app = FastAPI()

# Endpoint for getting all groceries
@app.get("/groceries") 
def fetch_groceries():
    query = """
        SELECT DISTINCT
            number,
            grocery_name,
        FROM mart.mart_grocery_nutrients
    """
    json_object = json_response(query=query)
    # Opens connection to duckdb
    return json_object
    


if __name__ == "__main__":
    print(type(fetch_groceries()))