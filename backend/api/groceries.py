from fastapi import APIRouter, HTTPException, Query
from backend.models.grocery import Grocery
from backend.core.db import get_connection

# Create a new APIRouter instance
# This keeps grocery endpoints modular, so we can include it in main.py
router = APIRouter()

# -------------------------
# Endpoint: List groceries
# -------------------------
@router.get("/", response_model=list[Grocery])
def list_groceries(limit: int = Query(10, ge=1, le=200), offset: int = 0):
    """
    List groceries with pagination.
    - `limit` controls number of items returned (default 10)
    - `offset` controls starting index (default 0)
    """

    # Open a read-only connection to DuckDB
    conn = get_connection()

    # SQL query: select surrogate key (id), Livsmedelsverket number, name, version timestamp
    # 'LIMIT ? OFFSET ?' will be filled with Python variables safely to avoid SQL injection
    query = """
        SELECT 
            id,       -- surrogate key (from dim_grocery)
            number,   -- original Livsmedelsverket food number
            name,     -- name of the grocery
            version   -- last updated timestamp
        FROM dim_grocery
        LIMIT ? OFFSET ?
    """

    # Execute query and fetch all rows
    rows = conn.execute(query, [limit, offset]).fetchall()
    # Close connection
    conn.close()

    # Convert each row to a Pydantic Grocery model instance
    # Pydantic ensures the response matches our model and will automatically convert datetime
    return [
        Grocery(
            id=r[0],
            number=r[1],
            name=r[2],
            version=r[3]
        )
        for r in rows
    ]


# -----------------------------
# Endpoint: Get single grocery
# -----------------------------
@router.get("/{grocery_id}", response_model=Grocery)
def get_grocery(grocery_id: int):
    """
    Fetch a single grocery item by its surrogate ID.
    - Returns 404 if the grocery is not found.
    """
    conn = get_connection()

    # SQL query to select a single grocery
    query = """
        SELECT 
            id,
            number,
            name,
            version
        FROM dim_grocery
        WHERE id = ?
    """
    # Fetch one row matching the id
    result = conn.execute(query, [grocery_id]).fetchone()
    conn.close()

    # Raise 404 if no row was found
    if not result:
        raise HTTPException(status_code=404, detail="Grocery not found")

    # Return Pydantic model instance
    return Grocery(
        id=result[0],
        number=result[1],
        name=result[2],
        version=result[3]
    )