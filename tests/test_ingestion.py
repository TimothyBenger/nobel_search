from app.db import laureates_collection

def test_data_ingestion(client):
    # Verify if the laureates collection is not empty after ingestion
    count = laureates_collection.count_documents({})
    assert count > 0, "Ingestion failed, laureates collection is empty."
