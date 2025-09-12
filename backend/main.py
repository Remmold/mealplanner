from fastapi import FastAPI
from backend.api.groceries import router as groceries_router

# We pass metadata here (title, description, version) that will be used in docs (Swagger)
app = FastAPI(
    title="MealPlanner API",
    description="API for meal planning, nutrition and groceries",
    version="0.1.0",
)

# Attach (include) another router to the app
# - groceries_router will contain all endpoints related to groceries
# - prefix means all endpoints will start with "/groceries"
# - tags are labels shown in the auto-generated docs
app.include_router(groceries_router, prefix="/groceries", tags=["groceries"])

# Define a simple root endpoint at "/"
# This is just a simple health check for the API
@app.get("/")
def root():
    return {"message": "Welcome to the MealPlanner API!"}
