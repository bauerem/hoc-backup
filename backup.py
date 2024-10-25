from pymongo import MongoClient
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Connect to the MongoDB database
client = MongoClient(os.getenv("REMOTE_MONGODB_URL"))
db = client["logs"]

# Define the collections to backup
collections_to_backup = ["requests", "traces"]


def backup_collection(collection_name):
    collection = db[collection_name]

    # Get all documents in the collection
    all_documents = list(collection.find())

    # Create the base directory if it doesn't exist
    base_dir = '../../Data/hoc-backup'
    os.makedirs(base_dir, exist_ok=True)

    # Create the collection directory
    collection_dir = os.path.join(base_dir, collection_name)
    os.makedirs(collection_dir, exist_ok=True)

    # Group documents by year-month
    grouped_docs = {}
    for doc in all_documents:
        doc["_id"] = str(doc["_id"])
        dt = datetime.strptime(doc['datetime'], "%Y-%m-%dT%H:%M:%S.%f")
        year_month = f"{dt.year}-{str(dt.month).zfill(2)}"
        if year_month not in grouped_docs:
            grouped_docs[year_month] = []
        grouped_docs[year_month].append(doc)

    print(
        f"Starting backup for collection '{collection_name}'.")
    # Process each year-month group
    for year_month, docs in grouped_docs.items():
        output_file = os.path.join(collection_dir, f"{year_month}.jsonl")

        if os.path.exists(output_file):
            # Case 1 or 2: File already exists
            existing_docs = set()
            with open(output_file, 'r', encoding='utf-8') as f:
                for line in f:
                    existing_doc = json.loads(line.strip())
                    existing_docs.add(json.dumps(existing_doc, sort_keys=True))

            new_docs = [doc for doc in docs if json.dumps(
                doc, sort_keys=True) not in existing_docs]

            if new_docs:
                # Case 2: Partially backed up, merging results
                with open(output_file, 'a', encoding='utf-8') as f:
                    for doc in new_docs:
                        json.dump(doc, f, ensure_ascii=False)
                        f.write('\n')
                print(
                    f"Year-month {year_month} already partially backed up, merged results")
            else:
                # Case 1: Already fully backed up
                print(f"Year-month {year_month} already backed up")
        else:
            # Case 3: New backup
            with open(output_file, 'w', encoding='utf-8') as f:
                for doc in docs:
                    json.dump(doc, f, ensure_ascii=False)
                    f.write('\n')
            print(f"Backed up year-month {year_month}")

    print(
        f"Backup completed for collection '{collection_name}'.")


# Backup all specified collections
for collection_name in collections_to_backup:
    backup_collection(collection_name)

print("Backup process completed successfully.")
