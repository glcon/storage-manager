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

# Build a list of all subdirs and their sizes, takes in a dir
def build_table(main_dir):
    # Lists for full paths and just names of each subdir
    full_subdir_paths = []
    subdir_names = []

    # Gather a list of full paths to parallel process on
    for item in os.listdir(main_dir):
        # Combine the main dir and subdir to make a full path, then add to list
        full_subdir_paths.append(
            os.path.join(main_dir, item)
        )
        
        # Gather a list of just subdir names for printing later
        subdir_names.append(item)


    # Use parallel processing to find many dir sizes at once
    with ThreadPoolExecutor() as executor:
        subdir_sizes = executor.map(get_dir_size, full_subdir_paths)

    # Convert sizes from iterator to list, then combine sizes and names
    names_and_sizes = list(zip(subdir_names, subdir_sizes))

    full_table = tabulate(
        names_and_sizes, 
        headers = ["Folder Name", "Size"], 
        tablefmt = "simple"
    )

    return full_table

def main():
    start = time.time()

    my_path = "C:\\Program Files"
    print(build_table(my_path))

    end = time.time()
    print(end - start)

if __name__ == "__main__":
    main()
