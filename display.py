from dir_utils import subdir_info
from rich.table import Table
from rich.console import Console
from rich.box import ROUNDED
from rich.align import Align


# Convert to human readable format
def readable(size):
    counter = 0
    suffixes = {
        0: "Bytes", 
        1: "KB",
        2: "MB",
        3: "GB",
        4: "TB"
    }

    while size >= 1000:
        size = size / 1000
        counter += 1
    
    # Take only 3 digits
    size = str(size)
    while len(size.replace(".", "")) > 3:
        size = size[:-1]

    if size[-1] == ".":
        size = size[:-1]
    
    return f"{size} {suffixes[counter]}"
    
# Split output into 2 rows
def split_rows(rows):
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
    full_list = subdir_info(directory)

    # Convert sizes to human readable
    for x in range(len(full_list)):
        full_list[x][1] = readable(full_list[x][1])

    console = Console()
    table = Table(show_header=False, box=ROUNDED)

    # Split columns if too long
    if len(full_list) > 20:
        full_list = split_rows(full_list)

        table.add_column("Folder Name", style="cyan")
        table.add_column("Size", style="white")

    table.add_column("Folder Name", style="cyan")
    table.add_column("Size", style="white")

    for row in full_list:
        table.add_row(*row)

    print("\n")
    console.print(Align.center(table))
    print("\n")