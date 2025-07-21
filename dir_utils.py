import string
import os
import subprocess
import psutil

# Gets the size of a directory
def _get_dir_size(ui_state, dir_path):
    process_variable = subprocess.run(
        ["dir_size.exe", dir_path],
        capture_output=True,
        text=True
    )

    output = int(process_variable.stdout.strip())

    if ui_state.show_cnc == False and output == 0:
        return

    return output

# Returns a list of all drives and their sizes
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

# Determines if file's size should be calculated
def _should_calculate(ui_state, full_path):
    # Ignore non-folders when inside any drive
    if len(ui_state.current_path) == 1:
        if not os.path.isdir(full_path):
            return False
    
    if os.path.islink(full_path):
        return False
    
    # Inaccessible
    try:
        os.stat(full_path)
    except (PermissionError, FileNotFoundError, OSError):
        return False
    
    return True

# Build a list of all subdirs and their sizes, takes in a dir
def subdirs_and_sizes(ui_state, main_dir):
    subdir_names = []
    subdir_sizes = []

    for directory in os.listdir(main_dir):
        full_path = os.path.join(main_dir, directory)

        if not _should_calculate(ui_state, full_path):
            continue

        current_directory_size = _get_dir_size(ui_state, full_path)

        # If folder name is too long, truncate it
        if len(directory) >= 29:
            cutoff = 26

            # Dont land on a space
            if directory[cutoff - 1] == " ":
                cutoff -= 2
            
            directory = directory[:cutoff] + "..."
        
        # Dont add
        if current_directory_size == None:
            continue

        subdir_names.append(directory)
        subdir_sizes.append(current_directory_size)

    names_and_sizes = []
    for name, size in zip(subdir_names, subdir_sizes):
        names_and_sizes.append([name, size])

    return names_and_sizes