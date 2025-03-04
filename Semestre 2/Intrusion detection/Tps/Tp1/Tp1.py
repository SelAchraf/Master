import os
import hashlib
import time
import tkinter as tk
from tkinter import messagebox

# Define the directory to monitor
directory_to_monitor = "/home/shito/Master/Semestre 2/Intrusion detection/Tps/Tp1"

# Define the path for the baseline file (outside the monitored directory)
baseline_file = "/home/shito/Master/Semestre 2/Intrusion detection/Tps/baseline.txt"

def calculate_file_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_baseline(directory):
    """Generate hashes for all files in the directory and store them in the baseline file."""
    hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_file_hash(file_path)
            hashes[file_path] = file_hash

    # Write the hashes to the baseline file
    with open(baseline_file, "w") as f:
        for file_path, file_hash in hashes.items():
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
            show_popup(f"File modified: {file_path}")

    # Check for deleted files
    for file_path in baseline_hashes:
        if file_path not in current_hashes:
            show_popup(f"File deleted: {file_path}")

    # Update the baseline file with the current state
    with open(baseline_file, "w") as f:
        for file_path, file_hash in current_hashes.items():
            f.write(f"{file_path}|{file_hash}\n")

# Generate initial baseline if the baseline file doesn't exist
if not os.path.exists(baseline_file):
    generate_baseline(directory_to_monitor)

# Start monitoring
print(f"Monitoring directory: {directory_to_monitor}")
try:
    while True:
        check_for_changes()  # Check for changes evry 5 seconds
        time.sleep(1)  # Wait for 5 seconds before the next check
except KeyboardInterrupt:
    print("Monitoring stopped.")