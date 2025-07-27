from dir_utils import subdirs_and_sizes, get_drives
from rich.table import Table
from rich.console import Console
from rich.box import ROUNDED
from rich.align import Align
import messages
from ui_spinner import start_spinner, stop_spinner
import shutil
import os

def welcome_message():
    show_welcome_path = r"src\stman\show_welcome.txt"

    if os.path.exists(show_welcome_path):
        try:
            with open(show_welcome_path, "r") as f:
                if f.read().strip().lower() == "no":
                    return  # Don't show message
        except (IOError, OSError):
            # If we can't read the file, show the welcome message anyway
            pass
    
    os.system("cls")

    print(messages.welcome_text)

    print()
    input("Hit any key to continue. ")

# Prints layer and folder name above a table
def _print_header(ui_state):
    layer_number = len(ui_state.current_path)
    
    if not ui_state.current_path:
        current_folder_name = "Root"
    else:
        current_folder_name = ui_state.current_path[-1]

    try:
        width = shutil.get_terminal_size().columns
    except OSError:
        width = 80  # Default width if terminal size can't be determined
    
    info_message = f"Current Folder: {current_folder_name}        Layer: {layer_number}"

    print(info_message.center(width))

# Converts bytes to human readable format
def _convert_to_readable(size) -> str:
    # Could not calculate size
    if size == "ERR":
        return "CNC"

    suffixes = ["Bytes", "KiB", "MiB", "GiB", "TiB", "PiB"]

    for suffix in suffixes:
        if size < 1024:
            break
        
        size = size / 1024
    
    return f"{size:.3g} {suffix}"
    
# Turn a 2 column list into a 4 column one
def _split_rows(rows) -> list:
    if not rows:
        return []
        
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

# Builds list that gets displayed on ui
def _build_display_list(ui_state):
    # current_path empty -> return drives
    if not ui_state.current_path:
        display_list = get_drives()
    else:
        directory = os.path.join(*ui_state.current_path)
        display_list = subdirs_and_sizes(ui_state, directory)

    return display_list

def _format_display_list(display_list, table):
    # Create a new list to avoid mutating the input
    formatted_list = []
    
    for index, item in enumerate(display_list):
        formatted_item = [
            f"[dim]{index + 1})[/dim] [cyan]{item[0]}",
            _convert_to_readable(item[1])
        ]
        formatted_list.append(formatted_item)

    # Split columns if list is long
    if len(formatted_list) > 20:
        formatted_list = _split_rows(formatted_list)

        table.add_column("Folder Name")
        table.add_column("Size", style = "white", justify = "right")

    return formatted_list

def _update_selections(ui_state, display_list):
    ui_state.selections = [subdir_name for subdir_name, _ in display_list]

# Displays the main ui interface
def display_table(ui_state):
    start_spinner()

    console = Console()
    table = Table(show_header = False, box = ROUNDED)
    table.add_column("Folder Name")
    table.add_column("Size", style = "white", justify = "right")

    # Check cache
    path_key = "\\".join(ui_state.current_path) if ui_state.current_path else "root"
    cache_value = ui_state.cache_get(path_key)
    if cache_value:
        display_list = cache_value
    else:
        display_list = _build_display_list(ui_state)
        ui_state.cache_set(path_key, display_list)

    # Sort, update selections, format
    def sort_key(item):
        size = item[1]
        if isinstance(size, str):
            return -1  # Put string values (like "ERR") at the end
        return size
    
    display_list = sorted(display_list, key=sort_key, reverse=True)
    _update_selections(ui_state, display_list)
    display_list = _format_display_list(display_list, table)

    for row in display_list:
        table.add_row(*row)

    stop_spinner()

    print("\n")
    _print_header(ui_state)
    print()
    console.print(Align.center(table))
    print("\n")