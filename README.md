# Folder Synchronization Program

This Python program synchronizes two folders, maintaining an identical copy of the `source` folder in the `replica` folder. Synchronization is one-way, meaning changes are only propagated from `source` to `replica`. The program operates periodically, logging all file operations to both a log file and the console.

## Features
- Synchronizes folders periodically, updating the `replica` folder to match the `source`.
- Logs creation, copying, and deletion of files and folders.
- Maintains an instance-specific log and a consolidated log for all executions.
- Can be customized through command-line arguments.

## Requirements
- Python 3.x

## Usage

### Command-Line Arguments

The program accepts four arguments:
1. **Source Folder Path**: The path to the source folder.
2. **Replica Folder Path**: The path to the replica folder.
3. **Synchronization Interval**: Interval in seconds between each synchronization.
4. **Log File Path**: Path to the instance-specific log file.

### Example Usage

Run the program from the command line as follows:

```bash
python sync_folders.py /path/to/source /path/to/replica 60 /path/to/logs/instance_log.log
