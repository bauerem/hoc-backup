import os
import json
from datetime import datetime

# Function to move files to external hard drive


def save_to_external_drive(source_file_path, destination_file_path):
    try:
        if os.path.exists(destination_file_path):
            # Case 1 or 2: File already exists on external drive
            source_docs = set()
            with open(source_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    source_doc = json.loads(line.strip())
                    source_docs.add(json.dumps(source_doc, sort_keys=True))

            destination_docs = set()
            with open(destination_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    destination_doc = json.loads(line.strip())
                    destination_docs.add(json.dumps(
                        destination_doc, sort_keys=True))

            new_docs = source_docs - destination_docs

            if new_docs:
                # Case 2: Partially backed up, merging results
                with open(destination_file_path, 'a', encoding='utf-8') as f:
                    for doc_json in new_docs:
                        doc = json.loads(doc_json)
                        json.dump(doc, f, ensure_ascii=False)
                        f.write('\n')
                print(
                    f"File partially updated on external drive: {destination_file_path}")
            else:
                # Case 1: Already fully backed up
                print(
                    f"File already up-to-date on external drive: {destination_file_path}")
        else:
            # Case 3: New backup
            os.rename(source_file_path, destination_file_path)
            print(
                f"File moved successfully to external drive: {source_file_path}")
    except Exception as e:
        print(f"Error processing file: {e}")


# Path to the external hard drive
external_drive_path = "/path/to/external/harddrive/backups/"

# Move all JSONL files to the external hard drive
for filename in os.listdir():
    if filename.endswith(".jsonl"):
        source_file_path = os.path.abspath(filename)
        destination_file_path = os.path.join(external_drive_path, filename)
        save_to_external_drive(source_file_path, destination_file_path)

print("External drive update process completed.")
