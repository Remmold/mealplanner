import dlt
import requests




@dlt.resource(name="food_resources", write_disposition="replace")
def fetch_from_livsmedelsvarket():
    base_url = "https://dataportal.livsmedelsverket.se/livsmedel" # <-- Correct base URL
    endpoint = "/api/v1/livsmedel"
    
    offset = 0
    limit = 100

    while True:
        params = {
            "offset": offset,
            "limit": limit
        }
        
        response = requests.get(base_url + endpoint, params=params)
        response.raise_for_status()
        page_data = response.json()
        print(page_data)

        if not page_data or offset >= 100:
            # If the API returns an empty list, what should you do?
            print("No more data found. Stopping.")
            break

        print(f"Fetched {len(page_data)} items from offset {offset}")
        
        # Instead of yielding the whole list, what should you do here?
        # Hint: A for loop
        for item in page_data:
            yield item

        # How do you prepare for the next page?
        offset += limit

        if __name__ == "__main__":
            # If this module is run directly, print the first item
            first_item = next(fetch_from_livsmedelsvarket())
            print("First item:", first_item)