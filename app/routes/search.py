from fastapi import APIRouter, HTTPException
from app.db import laureates_collection
from pymongo import ASCENDING
from app.routes.search_helpers import serialize_laureate  # Import the helper function

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

router = APIRouter()

# Serialize laureate object (helper function to handle ObjectId)
def serialize_laureate(laureate):
    # Check if the '_id' exists in the laureate object; otherwise, skip it.
    if "_id" in laureate:
        laureate["_id"] = str(laureate["_id"])
    return laureate


# Fuzzy search laureates by name
@router.get("/search/name/")
def fuzzy_search_by_name(name: str):
    # Get all laureates from the database
    all_laureates = laureates_collection.find()
    all_laureates_list = list(all_laureates)
    
    # Prepare a list of names (firstname + surname) for fuzzy matching
    full_names = [
        (laureate.get('firstname', '') + " " + laureate.get('surname', ''), laureate)
        for doc in all_laureates_list if 'laureates' in doc  # Ensure 'laureates' key exists
        for laureate in doc['laureates']
    ]
    
    # Use FuzzyWuzzy to find the closest match
    best_matches = process.extract(name, [full_name[0] for full_name in full_names], limit=10, scorer=fuzz.partial_ratio)

    # Filter matches with a score above a threshold
    matched_laureates = [
        full_names[i][1] for match, score in best_matches if score >= 80 for i, full_name in enumerate(full_names) if full_name[0] == match
    ]
    
    if matched_laureates:
        return [serialize_laureate(laureate) for laureate in matched_laureates]
    raise HTTPException(status_code=404, detail="No laureates found with the given name")




# # Search laureates by name
# @router.get("/search/name/")
# def search_by_name(name: str):
#     results = laureates_collection.find({
#         "laureates": {
#             "$elemMatch": {
#                 "$or": [
#                     {"firstname": {"$regex": name, "$options": "i"}},
#                     {"surname": {"$regex": name, "$options": "i"}}
#                 ]
#             }
#         }
#     }).sort("year", ASCENDING)

#     laureates = list(results)
#     if laureates:
#         return [serialize_laureate(laureate) for laureate in laureates]
#     raise HTTPException(status_code=404, detail="No laureates found with the given name")


# Search laureates by category
@router.get("/search/category/")
def search_by_category(category: str):
    results = laureates_collection.find({
        "category": {"$regex": category, "$options": "i"}
    }).sort("year", ASCENDING)

    laureates = list(results)
    if laureates:
        return [serialize_laureate(laureate) for laureate in laureates]  # Serialize each laureate
    raise HTTPException(status_code=404, detail="No laureates found for the given category")

# Search laureates by description (motivation)
@router.get("/search/description/")
def search_by_description(description: str):
    results = laureates_collection.find({
        "laureates": {
            "$elemMatch": {
                "motivation": {"$regex": description, "$options": "i"}
            }
        }
    }).sort("year", ASCENDING)

    laureates = list(results)
    if laureates:
        return [serialize_laureate(laureate) for laureate in laureates]
    raise HTTPException(status_code=404, detail="No laureates found matching the description")
