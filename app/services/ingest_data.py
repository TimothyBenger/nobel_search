import requests
from app.db import laureates_collection

NOBEL_API_URL = "https://api.nobelprize.org/v1/prize.json"

async def ingest_data():
    # Check if the data has already been ingested (by checking if the collection is not empty)
    if laureates_collection.count_documents({}) == 0:
        print("Ingesting Nobel Prize data...")

        # Fetch the data from the API
        response = requests.get(NOBEL_API_URL)
        if response.status_code == 200:
            prizes = response.json()["prizes"]

            # Insert the data into MongoDB
            laureates_collection.insert_many(prizes)
            print("Data successfully ingested.")
        else:
            print(f"Failed to fetch data: {response.status_code}")
    else:
        print("Data already exists. Skipping ingestion.")
