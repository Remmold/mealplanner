import duckdb
import dlt
from resources import grocery_resources

def run_pipeline():
    pipeline = dlt.pipeline(
    pipeline_name="Groceries",
    destination="duckdb",           # Fix destination
    dataset_name="raw",
    progress="log"
    )

    info = pipeline.run(grocery_resources())
    return info

if __name__ == "__main__":
    load_info = run_pipeline()
    print(load_info)