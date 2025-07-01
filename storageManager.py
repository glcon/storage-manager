import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from tabulate import tabulate

# Gets the size of a directory by calling a c script
def get_dir_size(dir_path):
    # Run the C script and store its contents
    process_variable = subprocess.run(
        ["directorySize.exe", dir_path],
        capture_output=True,
        text=True
    )

    # Assign contents to a variable, remove blank characters
    output = process_variable.stdout.strip()

    # Check if output is a number before returning
    if output.isdigit():
        return int(output)
    else:
        return -1

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

# Quicksort to sort subdirs by size
def quick_sort(data):
    if len(data) <= 1:
        return data
    
    pivot = data[len(data) // 2][1]
    left = []
    middle = []
    right = []
    
    for item in data:
        if item[1] > pivot:
            left.append(item)
        elif item[1] == pivot:
            middle.append(item)
        else:
            right.append(item)
    
    return quick_sort(left) + middle + quick_sort(right)

# Build a list of all subdirs and their sizes, takes in a dir
def build_table(main_dir):
    full_subdir_paths = []
    subdir_names = []

    # Gather gather each full path and subdir name
    for item in os.listdir(main_dir):
        # Create full path of each subdir
        full_path = os.path.join(main_dir, item)

        # Check if we should skip
        if should_skip(main_dir, full_path):
            continue

        # If folder name is too long, truncate it
        if len(item) >= 27:
            cutoff = 24

            # Dont land on a space -> show that folder name is cut off
            if item[cutoff - 1] == " ":
                cutoff -= 2
            item = item[:cutoff] + "..."

        # Add full path and subdir name to each list
        full_subdir_paths.append(full_path)
        subdir_names.append(item)


    # Parallel processing to find dir sizes
    with ThreadPoolExecutor() as executor:
        subdir_sizes = executor.map(get_dir_size, full_subdir_paths)

    # Combine sizes and names, then convert to list
    names_and_sizes = list(zip(subdir_names, subdir_sizes))
    names_and_sizes = quick_sort(names_and_sizes)

    # Turn everything into a table
    full_table = tabulate(
        names_and_sizes, 
        headers = ["Folder Name", "Size"], 
        tablefmt = "simple"
    )

    return full_table

def main():
    user_input = input("Enter a system path: ")
    
    try:
        print("\n" + build_table(user_input) + "\n")
    except Exception:
        print("Couldn't find that path.")

if __name__ == "__main__":
    main()