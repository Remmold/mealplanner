from fastapi import FastAPI
from mealplanner.backend.data_processing import json_response

# Initialize the fastapi object
app = FastAPI()

# Endpoint for getting all groceries
@app.get("/groceries") 
async def fetch_groceries():
    """
    Fetches id and name of all groceries.
    """
    query = """
        SELECT DISTINCT
            grocery_id,
            grocery_name,
        FROM mart.mart_grocery_nutrients
        ORDER BY grocery_name
    """
    json_object = json_response(query=query)
    return json_object
    
@app.get("/groceries/{grocery_id}")
async def fetch_grocery_nutrients(grocery_id: str):
    """
    Fetches grocery item with its id. 
    """
    query = f"""
        SELECT
            nutrient_name,
            nutrient_value,
            nutrient_measurement_unit
        FROM mart.mart_grocery_nutrients
        WHERE grocery_id = '{grocery_id}' 
        """
    json_object = json_response(query)    
    return json_object

if __name__ == "__main__":
    print(type(fetch_groceries()))