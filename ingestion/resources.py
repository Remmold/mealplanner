import duckdb
import dlt
from dlt.sources.helpers import requests

BASE_URL = "https://dataportal.livsmedelsverket.se/livsmedel"

# Fetch raw groceries 
########################################################################
@dlt.resource(table_name="raw_grocery", write_disposition="replace")
def load_groceries():
    """
    Fetches basic information for grocery items from Livsmedelsverket.

    This function retrieves a list of grocery items, where each entry contains only fundamental details such as the name and food item number. Note that the response does not include nutritional values, ingredients, or other extended information—only the essential base data for each grocery item is provided.
    """
    endpoint = "/api/v1/livsmedel"
    params = {
        "limit": 10000
    }
    response = requests.get(url=BASE_URL+endpoint, params=params)
    yield response.json()

########################################################################

# Fetch /api/v{version}/livsmedel/{nummer}/naringsvarden Fetch all ingridents for each grocery (50 ingridents per grocery ish?)
########################################################################

########################################################################

# Source handles the order for each resource, wich should run first.. etc
@dlt.source(name="livsmedel_api")
def grocery_resources():
    return [load_groceries()]