import dlt
from resources import grocery_resources

from mealplanner.utils.constants import DATA_PATH

def run_pipeline():
    pipeline = dlt.pipeline(
    pipeline_name="Groceries",
    destination=dlt.destinations.duckdb(str(DATA_PATH)),
    dataset_name="raw",
    progress="log"
    )

    info = pipeline.run(grocery_resources())
    return info

if __name__ == "__main__":
    load_info = run_pipeline()
    print(load_info)