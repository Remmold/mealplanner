from pydantic import BaseModel
from datetime import datetime

class Grocery(BaseModel):
    id: str                     # Surrogate key for API usage
    number: int                 # Original Livsmedelsverkets number
    name: str                   # Name of the grocery
    version: datetime = None    # Last update timestamp

    # This model could later on be extended with:
    # - category (from dim_classification)
    # - nutrients (from dim_nutrient)
    # - ingredients (from dim_ingredient)
