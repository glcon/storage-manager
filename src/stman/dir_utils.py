import string
import os
import ctypes
import psutil
import copy
from ctypes import wintypes, WinDLL, c_wchar_p

# Load the DLL
dir_size_dll = WinDLL(r"dir_size\dir_size.dll")
dir_size_dll.get_directory_size.argtypes = [wintypes.LPCWSTR]
dir_size_dll.get_directory_size.restype = c_wchar_p

# Gets the size of a directory
# Returning none prevents it from being displayed
def _get_dir_size(ui_state, dir_path):
    output = dir_size_dll.get_directory_size(dir_path)

    if ui_state.show_cnc == False and output == "ERR":
        return None

    # Convert successful calculations back to integers
    if output != "ERR":
        try:
            return int(output)
        except (ValueError, TypeError):
            return "ERR"  # If conversion fails, treat as error

    return output


# Returns a list of all drives and their sizes
def get_drives() -> list:
    drives = []

    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"

        if os.path.exists(drive):
            try:
                # Get disk usage info
                usage = psutil.disk_usage(drive)
                size = usage.used
                drives.append([drive, size])
            except (OSError, PermissionError):
                # Skip drives we can't access
                continue

    return drives

# Determines if file's size should be calculated
def _should_calculate(ui_state, full_path) -> bool:
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
def subdirs_and_sizes(ui_state, main_dir) -> list:  
    subdir_names = []
    subdir_sizes = []

    for directory in os.listdir(main_dir):
        full_path = os.path.join(main_dir, directory)

        if not _should_calculate(ui_state, full_path):
            continue

        current_directory_size = _get_dir_size(ui_state, full_path)

        # Dont add
        if current_directory_size == None:
            continue
        
        # If folder name is too long, truncate it
        if len(directory) >= 29:
            cutoff = 26

            # Dont land on a space
            if cutoff > 1 and directory[cutoff - 1] == " ":
                cutoff -= 2
            
            # Ensure cutoff doesn't go below 0
            cutoff = max(0, cutoff)
            directory = directory[:cutoff] + "..."

        subdir_names.append(directory)
        subdir_sizes.append(current_directory_size)

    names_and_sizes = []
    for name, size in zip(subdir_names, subdir_sizes):
        names_and_sizes.append([name, size])

    # Will be a list of lists
    return names_and_sizes