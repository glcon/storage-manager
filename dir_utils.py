import string
import os
import subprocess
import psutil

# Gets the size of a directory
def get_dir_size(dir_path):
    process_variable = subprocess.run(
        ["dir_size.exe", dir_path],
        capture_output=True,
        text=True
    )

    # Remove blank characters
    output = process_variable.stdout.strip()

    # add statement to detect char output AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    # will eventually replace the 0s with "error finding" or something
    return int(output)

# Gets all drives
def get_drives():
    drives = []

    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"

        if os.path.exists(drive):
            # Get disk usage info
            usage = psutil.disk_usage(drive)
            size = usage.used
            drives.append([drive, size])

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
def subdir_info(main_dir):
    full_subdir_paths = []
    subdir_names = []
    subdir_sizes = []

    # Gather gather each full path, subdir name, subdir size
    for directory in os.listdir(main_dir):
        # Create full path
        full_path = os.path.join(main_dir, directory)

        # Check if we should skip
        if should_skip(main_dir, full_path):
            continue

        # If folder name is too long, truncate it
        if len(directory) >= 29:
            cutoff = 26

            # Dont land on a space
            if directory[cutoff - 1] == " ":
                cutoff -= 2
            directory = directory[:cutoff] + "..."

        full_subdir_paths.append(full_path)
        subdir_names.append(directory)
        subdir_sizes.append(get_dir_size(full_path))

    names_and_sizes = []
    for name, size in zip(subdir_names, subdir_sizes):
        names_and_sizes.append([name, size])

    return names_and_sizes