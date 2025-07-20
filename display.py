from dir_utils import subdirs_and_sizes, get_drives
from rich.table import Table
from rich.console import Console
from rich.box import ROUNDED
from rich.align import Align
import os
from ui_spinner import start_spinner, stop_spinner

# Converts bytes to human readable format
def _convert_to_readable(size):
    # Could not calculate
    if size == 0:
        return "CNC"

    counter = 0
    suffixes = ["Bytes", "KiB", "MiB", "GiB", "TiB", "PiB"]

    for suffix in suffixes:
        if size < 1024:
            break
        
        size = size / 1024
    
    return f"{size:.3g} {suffix}"
    
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

def navigate(ui_state):
    start_spinner()

    # Init console + table, create first columns
    console = Console()
    table = Table(show_header = False, box = ROUNDED)

    table.add_column("Folder Name")
    table.add_column("Size", style = "white", justify = "right")

    # Empty -> show drives, else show subdirs
    if not ui_state.current_path:
        display_list = get_drives()
    else:
        directory = os.path.join(*ui_state.current_path)
        display_list = subdirs_and_sizes(directory)

    display_list = sorted(display_list, key=lambda x: x[1])
    display_list.reverse()

    # Update choices to reflect ui
    if not ui_state.current_path:
        ui_state.selections = [drive_name for drive_name, _ in display_list]
    else:
        ui_state.selections = [subdir_name for subdir_name, _ in display_list]

    for index in range(len(display_list)):
        display_list[index][1] = _convert_to_readable(display_list[index][1])

        # Numbers + coloring for accessibility
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

    print("\n")
    console.print(Align.center(table))
    print("\n")