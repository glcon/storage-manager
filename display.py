from dir_utils import subdir_info, get_drives
from rich.table import Table
from rich.console import Console
from rich.box import ROUNDED
from rich.align import Align
import os
from spinner import start_spinner, stop_spinner

# Convert to human readable format
def _readable(size):
    # Tell user "could not calculate"
    if size == 0:
        return "CNC"

    counter = 0
    suffixes = {
        0: "Bytes", 
        1: "KiB",
        2: "MiB",
        3: "GiB",
        4: "TiB"
    }

    while size >= 1024:
        size = size / 1024
        counter += 1
    
    # Take only 3 digits
    size = str(size)
    while len(size.replace(".", "")) > 3:
        size = size[:-1]

    if size[-1] == ".":
        size = size[:-1]
    
    return f"{size} {suffixes[counter]}"
    
# Split output into 2 rows
def _split_rows(rows):
    half = (len(rows) + 1) // 2  # Round up
    left_rows = rows[:half]
    right_rows = rows[half:]

    # If right row is shorter, pad with empty rows
    while len(right_rows) < len(left_rows):
        right_rows.append(["", ""])

    combined_rows = []
    for left, right in zip(left_rows, right_rows):
        combined_rows.append(left + right)

    return combined_rows

def navigate(directory):
    os.system("cls")
    start_spinner()

    # Init console + table, create first columns
    console = Console()
    table = Table(show_header = False, box = ROUNDED)

    table.add_column("Folder Name")
    table.add_column("Size", style = "white", justify = "right")
    
    is_split = False

    # If list empty -> display drives
    if not directory:
        display_list = get_drives()
    else:
        # Create a single path string from the passed list
        directory = os.path.join(*directory)

        display_list = subdir_info(directory)

    display_list = sorted(display_list, key=lambda x: x[1])
    display_list.reverse()

    # Store the possible folders for the user to go to after navigating
    # Needs to be done right after sort to maintain order
    if not directory:
        possible_selections = [drive_name for drive_name, _ in display_list]
    else:
        possible_selections = [subdir_name for subdir_name, _ in display_list]

    # Convert byte sizes to human readable
    for index in range(len(display_list)):
        display_list[index][1] = _readable(display_list[index][1])
        
        # If split, need to convert the 4th column's bytes too
        if is_split:
            display_list[index][3] = _readable(display_list[index][3])

        # Add numbers + coloring for accessibility
        display_list[index][0] = f"[dim]{index + 1})[/dim] [cyan]{display_list[index][0]}"

    # Split columns if too long
    if len(display_list) > 20:
        display_list = _split_rows(display_list)

        table.add_column("Folder Name")
        table.add_column("Size", style = "white", justify = "right")

        is_split = True

    for row in display_list:
        table.add_row(*row)

    stop_spinner()
    os.system("cls")

    print("\n")
    console.print(Align.center(table))
    print("\n")

    return possible_selections