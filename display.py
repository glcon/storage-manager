from dir_utils import subdirs_and_sizes, get_drives
from rich.table import Table
from rich.console import Console
from rich.box import ROUNDED
from rich.align import Align
import os
import shutil
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
    
# Turn a 2 column list into a 4 column one
def _split_rows(rows):
    half = (len(rows) + 1) // 2
    left_rows = rows[:half]
    right_rows = rows[half:]

    # If right row is shorter, add an empty row
    if len(right_rows) < len(left_rows):
        right_rows.append(["", ""])

    combined_rows = []
    for left, right in zip(left_rows, right_rows):
        combined_rows.append(left + right)

    return combined_rows

def navigate(ui_state):
    start_spinner()

    console = Console()
    table = Table(show_header = False, box = ROUNDED)

    table.add_column("Folder Name")
    table.add_column("Size", style = "white", justify = "right")

    # current_path empty -> show drives, else show subdirs
    if not ui_state.current_path:
        display_list = get_drives()
    else:
        directory = os.path.join(*ui_state.current_path)
        display_list = subdirs_and_sizes(ui_state, directory)

    display_list = sorted(display_list, key=lambda x: x[1])
    display_list.reverse()

    # Update state to reflect current ui
    if not ui_state.current_path:
        ui_state.selections = [drive_name for drive_name, _ in display_list]
    else:
        ui_state.selections = [subdir_name for subdir_name, _ in display_list]

    for index, item in enumerate(display_list):
        item[1] = _convert_to_readable(item[1])

        # Numbers + coloring for accessibility
        item[0] = f"[dim]{index + 1})[/dim] [cyan]{item[0]}"

    # Split columns if list is long
    if len(display_list) > 20:
        display_list = _split_rows(display_list)

        table.add_column("Folder Name")
        table.add_column("Size", style = "white", justify = "right")

    for row in display_list:
        table.add_row(*row)

    stop_spinner()

    terminal_width = shutil.get_terminal_size().columns
    message = "type \"/help\" for help"
    
    print("\n")
    print(message.center(terminal_width))
    print("\n")
    console.print(Align.center(table))
    print("\n")