import string
import sys
import os
import subprocess
from tabulate import tabulate
from display import split_rows, readable

# Gets the size of a directory
def get_dir_size(dir_path):
    process_variable = subprocess.run(
        ["dir_size.exe", dir_path],
        capture_output=True,
        text=True
    )

    # Remove blank characters
    output = process_variable.stdout.strip()

    return int(output)

# Gets all drives
def get_drives():
    drives = []

    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives

# Determines whether to calculate the dir size or not
def should_skip(main_dir, full_path):
    # If we are in "C:\" ignore anything that isn't a folder
    if os.path.abspath(main_dir) == os.path.abspath("C:\\") and os.path.isdir(full_path) == False:
        return True
    
    # Ignore symlinks
    if os.path.islink(full_path):
        return True
    
    # Ignore files we cant access
    try:
        os.stat(full_path)
    except (PermissionError, FileNotFoundError):
        return True
    
    return False

# Build a list of all subdirs and their sizes, takes in a dir
def build_table(main_dir):
    full_subdir_paths = []
    subdir_names = []

    # Gather gather each full path and subdir name
    for directory in os.listdir(main_dir):
        # Create full path
        full_path = os.path.join(main_dir, directory)

        # Check if we should skip
        if should_skip(main_dir, full_path):
            continue

        # If folder name is too long, truncate it
        if len(directory) >= 27:
            cutoff = 24

            # Dont land on a space
            if directory[cutoff - 1] == " ":
                cutoff -= 2
            directory = directory[:cutoff] + "..."

        full_subdir_paths.append(full_path)
        subdir_names.append(directory)

    # Make a list of each dir name and size
    subdir_sizes = []
    for path in full_subdir_paths:
        subdir_sizes.append(get_dir_size(path))

    names_and_sizes = []
    for name, size in zip(subdir_names, subdir_sizes):
        names_and_sizes.append([name, size])

    # Sort + human readable format
    names_and_sizes = sorted(names_and_sizes, key=lambda x: x[1])
    names_and_sizes.reverse()

    for x in range(len(names_and_sizes)):
        names_and_sizes[x][1] = readable(names_and_sizes[x][1])
    
    headers = ["Folder Name", "Size"]

    # If list is too long, split it
    if len(names_and_sizes) > 20:
        names_and_sizes = split_rows(names_and_sizes)
        headers = headers + headers

    # Turn everything into a table
    full_table = tabulate(
        names_and_sizes, 
        headers, 
        tablefmt = "simple"
    )

    return full_table