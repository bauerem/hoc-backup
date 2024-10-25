# hoc-backup

A set of scripts for backing up MongoDB collections, sanitizing old data, and transferring backups to an external drive.

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/bauerem/hoc-backup.git
   cd hoc-backup
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   REMOTE_MONGODB_URL=mongodb://your_connection_string_here
   ```

## Usage

### 1. Backup

Run the backup script to create local backups:

```
python backup.py
```

This script will:

- Connect to the specified MongoDB database
- Backup the "requests" and "traces" collections
- Save backups as JSONL files in the `../../Data/hoc-backup/` directory

### 2. Sanitize

Run the sanitize script to remove old data:

```
python sanitize.py
```

This script will:

- Remove documents older than 31 days from the "traces" collection
- Prompt for confirmation before deletion

### 3. Transfer to External Drive

Run the transfer script to move backups to an external drive:

```
python to_external.py
```

Before running, edit the `external_drive_path` variable in `to_external.py` to point to your external drive's backup folder.

This script will:

- Move JSONL files from the current directory to the specified external drive location
- Merge new data with existing backups if files already exist on the external drive

## Notes

- Ensure sufficient disk space on both local and external drives
- Regularly check and verify the integrity of your backups
- Adjust the `collections_to_backup` and `collections_to_sanitize` lists in the scripts if needed
- Consider setting up cron jobs to automate the backup and sanitization processes

Remember to handle sensitive data securely and comply with relevant data protection regulations.
