import os
import shutil
import time
import logging
import hashlib
from argparse import ArgumentParser

# Logging
def setup_logging(log_file):
    
    log_folder = os.path.dirname(log_file)
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    
    consolidated_log_file = os.path.join(log_folder, "All_Exec_logs.log")
    # Clear Instance-specific log file
    open(log_file, 'w').close()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),  # Instance-specific log file
            logging.StreamHandler(),
            logging.FileHandler(consolidated_log_file, mode='a')  # All execution log file 
        ]
    )



# MD5
def md5(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def sync_folders(source, replica):
    # Go through source folder and sync with replica
    for root, dirs, files in os.walk(source):
        # Get relative path
        relative_path = os.path.relpath(root, source)
        replica_dir = os.path.join(replica, relative_path)

        # Create directories in the replica folder if they do not exist
        if not os.path.exists(replica_dir):
            os.makedirs(replica_dir)
            logging.info(f"Created directory: {replica_dir}")

        # Process files in the directory
        for file_name in files:
            source_file = os.path.join(root, file_name)
            replica_file = os.path.join(replica_dir, file_name)

            # Check if the file does not exists in the replica or was changed
            if not os.path.exists(replica_file) or md5(source_file) != md5(replica_file):
                shutil.copy2(source_file, replica_file)
                logging.info(f"Copied file: {source_file} to {replica_file}")

    # Check for deleted files or folders in the source folder that still are in the replica folder
    for root, dirs, files in os.walk(replica, topdown=False):
        relative_path = os.path.relpath(root, replica)
        source_dir = os.path.join(source, relative_path)

        # Identify files that were removed from the source folder
        for file_name in files:
            replica_file = os.path.join(root, file_name)
            source_file = os.path.join(source_dir, file_name)
            if not os.path.exists(source_file):
                os.remove(replica_file)
                logging.info(f"Deleted file from replica: {replica_file}")

        # Identify directories that no longer exist in the source
        
        if not os.path.exists(os.path.join(source, relative_path)):
            # If the directory doesn't exist in source, delete it
            shutil.rmtree(root)
            logging.info(f"Deleted directory from replica: {root}")


def main():
    
    parser = ArgumentParser(description="Synchronize source and replica folders")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")

    args = parser.parse_args()

    
    setup_logging(args.log_file)

    while True:
        logging.info("Starting synchronization...")
        sync_folders(args.source, args.replica)
        logging.info("Synchronization complete.")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
