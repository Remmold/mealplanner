import dlt
from dlt.sources.helpers import requests

BASE_URL = "https://dataportal.livsmedelsverket.se/livsmedel"
s = requests.Session()

@dlt.resource(table_name="raw_grocery", write_disposition="replace")
def load_groceries():
    """
    Fetches basic information for grocery items from Livsmedelsverket.
    This function retrieves a list of grocery items, where each entry contains only fundamental details such as the name and food item number. Note that the response does not include nutritional values, ingredients, or other extended information—only the essential base data for each grocery item is provided.
    """
    endpoint = "/api/v1/livsmedel"
    params = {
        "limit": 2600
    }
    data = s.get(url=BASE_URL+endpoint, params=params).json()
    yield data["livsmedel"]


def _api_factory(name, item):
    """
    Help function for handling redundant code for api handling with diffrent namingend for endpoints
    """
    endpoint = f"/api/v1/livsmedel/{item['nummer']}/{name}"
    response = s.get(url=BASE_URL+endpoint)
    d = response.json()
    for row in d:
        row["grocery_number"] = item["nummer"]
    return d

#naringsvarden /api/v{version}/livsmedel/{nummer}/naringsvarden
@dlt.resource(table_name="raw_grocery_nutrients", write_disposition="replace")
def load_grocery_nutrients():
    """
    Fetches nutritional information for a specific grocery item from Livsmedelsverket.
    """
    data = s.get(url=BASE_URL+"/api/v1/livsmedel", params={"limit": 2600}).json()
    for item in data["livsmedel"]:
        d = _api_factory("naringsvarden", item)
        yield d

# klassificeringar /api/v{version}/livsmedel/{nummer}/klassificeringar
@dlt.resource(table_name="raw_grocery_classifications", write_disposition="replace")
def load_grocery_classifications():
    """
    Fetches classification information for a specific grocery item from Livsmedelsverket.
    """
    data = s.get(url=BASE_URL+"/api/v1/livsmedel", params={"limit": 2600}).json()
    for item in data["livsmedel"]:
        d = _api_factory("klassificeringar", item)
        yield d

# ravaror /api/v{version}/livsmedel/{nummer}/ravaror # materials
@dlt.resource(table_name="raw_grocery_materials", write_disposition="replace")
def load_grocery_materials():
    """
    Fetches material information for a specific grocery item from Livsmedelsverket.
    """
    data = s.get(url=BASE_URL+"/api/v1/livsmedel", params={"limit": 2600}).json()
    for item in data["livsmedel"]:
        d = _api_factory("ravaror", item)
        yield d

#ingredienser /api/v{version}/livsmedel/{nummer}/ingredienser
@dlt.resource(table_name="raw_grocery_ingredients", write_disposition="replace")
def load_grocery_ingredients():
    """
    Fetches ingredient information for a specific grocery item from Livsmedelsverket.
    """
    data = s.get(url=BASE_URL+"/api/v1/livsmedel", params={"limit": 2600}).json()
    for item in data["livsmedel"]:
        d = _api_factory("ingredienser", item)
        yield d

# Source handles the order for each resource, wich should run first.. etc
@dlt.source(name="grocery_api")
def grocery_resources():
    return [load_groceries(), load_grocery_nutrients(), load_grocery_classifications(), load_grocery_materials(), load_grocery_ingredients()]

