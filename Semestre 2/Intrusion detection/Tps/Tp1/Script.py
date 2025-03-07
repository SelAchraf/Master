import os
import hashlib
import time
import tkinter as tk
from tkinter import messagebox
import shutil

# Define the directory to monitor
directory_to_monitor = "/home/shito/Master/Semestre 2/Intrusion detection/Tps/Tp1/directory_to_monitor"

# Define the path for the baseline file
baseline_file = "/home/shito/Master/Semestre 2/Intrusion detection/Tps/Tp1/baseline.txt"

# Define the path for the backup directory
backup_directory = "/home/shito/Master/Semestre 2/Intrusion detection/Tps/Tp1/backup_directory"

def calculate_file_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_baseline(directory):
    """Generate hashes for all files in the directory and store them in the baseline file.
    If the baseline file already exists, its content will be replaced with the new hashes."""
    # Calculate hashes for all files in the directory
    current_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_file_hash(file_path)
            current_hashes[file_path] = file_hash

    # Write the new hashes to the baseline file, replacing its content
    with open(baseline_file, "w") as f:
        for file_path, file_hash in current_hashes.items():
            f.write(f"{file_path}|{file_hash}\n")

def load_baseline():
    """Load the hashes from the baseline file into a dictionary."""
    hashes = {}
    if os.path.exists(baseline_file):
        with open(baseline_file, "r") as f:
            for line in f:
                file_path, file_hash = line.strip().split("|")
                hashes[file_path] = file_hash
    return hashes

def show_popup(message):
    """Display a popup alert with the given message."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Alert", message)
    root.destroy()

def restore_file_from_backup(file_path):
    """Restore a file from the backup directory to the monitored directory."""
    # Get the relative path of the file
    relative_path = os.path.relpath(file_path, directory_to_monitor)
    backup_file_path = os.path.join(backup_directory, relative_path)

    # Check if the file exists in the backup directory
    if os.path.exists(backup_file_path):
        # Create the directory structure in the monitored directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Copy the file from the backup to the monitored directory
        shutil.copy2(backup_file_path, file_path)
        return True  # Indicate that the file was restored
    else:
        return False  # Indicate that the file was not restored

def check_for_changes():
    """Compare the current state of the directory with the baseline hashes."""
    current_hashes = {}
    for root, _, files in os.walk(directory_to_monitor):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_file_hash(file_path)
            current_hashes[file_path] = file_hash

    # Load the baseline hashes
    baseline_hashes = load_baseline()

    # Check for new or modified files
    for file_path, file_hash in current_hashes.items():
        if file_path not in baseline_hashes:
            show_popup(f"New file detected: {file_path}")
        elif baseline_hashes[file_path] != file_hash:
            # File modified: restore it and show a single alert
            if restore_file_from_backup(file_path):
                show_popup(f"File modified and restored: {file_path}")
                # Update the current_hashes with the restored file's hash
                current_hashes[file_path] = calculate_file_hash(file_path)

    # Check for deleted files
    for file_path in baseline_hashes:
        if file_path not in current_hashes:
            # File deleted: restore it and show a single alert
            if restore_file_from_backup(file_path):
                show_popup(f"File deleted and restored: {file_path}")
                # Update the current_hashes with the restored file's hash
                current_hashes[file_path] = calculate_file_hash(file_path)

    # Update the baseline file with the current state
    with open(baseline_file, "w") as f:
        for file_path, file_hash in current_hashes.items():
            f.write(f"{file_path}|{file_hash}\n")

def copy_files_to_backup():
    """Copy all files from the monitored directory to the backup directory.
    If the backup directory already exists, its content will be replaced with the new files."""
    # Create the backup directory if it doesn't exist
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)
    else:
        # Clear the backup directory if it exists
        for root, _, files in os.walk(backup_directory, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)  # Delete each file

    # Copy all files from the monitored directory to the backup directory
    for root, _, files in os.walk(directory_to_monitor):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory_to_monitor)
            backup_file_path = os.path.join(backup_directory, relative_path)

            # Create the directory structure in the backup directory if it doesn't exist
            os.makedirs(os.path.dirname(backup_file_path), exist_ok=True)

            # Copy the file
            shutil.copy2(file_path, backup_file_path)

# Generate or update the baseline
generate_baseline(directory_to_monitor)

# Create a backup of the files in the monitored directory
copy_files_to_backup()

# Start monitoring
print(f"Monitoring directory: {directory_to_monitor}")
try:
    while True:
        check_for_changes()
        time.sleep(1)
except KeyboardInterrupt:
    print("Monitoring stopped.")