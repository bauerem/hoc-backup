from pymongo import MongoClient
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("REMOTE_MONGODB_URL"))
db = client["logs"]

collections_to_sanitize = ["traces"]


def sanitize_collection(collection_name):
    collection = db[collection_name]

    cutoff_date = datetime.now() - timedelta(days=31)

    # Use $dateFromString operator to parse the date string
    filter_expression = {
        "$expr": {
            "$lt": [
                {"$dateFromString": {"dateString": "$datetime"}},
                cutoff_date
            ]
        }
    }

    # Fetch all matching documents in one query
    matching_docs = list(collection.find(filter_expression))

    # Count matching documents
    doc_count = len(matching_docs)

    # Find the oldest and newest dates
    min_datetime = min(datetime.fromisoformat(
        doc["datetime"]) for doc in matching_docs)
    max_datetime = max(datetime.fromisoformat(
        doc["datetime"]) for doc in matching_docs)

    print(f"Date range in collection: {min_datetime} to {max_datetime}")
    print(f"Cutoff date: {cutoff_date}")
    print(f"Found {doc_count} documents older than {cutoff_date}")

    confirmation = input("Delete {doc_count} documents? y/N\n")

    if confirmation == "y":

        deleted_count = 0
        for doc in matching_docs:
            try:
                result = collection.delete_one({"_id": doc["_id"]})
                if result.deleted_count > 0:
                    deleted_count += 1
            except Exception as e:
                print(f"Error deleting document {doc['_id']}: {str(e)}")

        print(f"Deleted {deleted_count} documents from {collection_name}")


for collection in collections_to_sanitize:
    sanitize_collection(collection)

print("Sanitization process completed successfully.")
client.close()
