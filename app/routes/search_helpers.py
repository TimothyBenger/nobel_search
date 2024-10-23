from bson import ObjectId

def serialize_laureate(laureate):
    laureate["_id"] = str(laureate["_id"])
    return laureate