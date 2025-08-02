from rich.table import Table
from rich.console import Console
from rich.box import ROUNDED
from rich.align import Align
import messages
from state import AppState
from dir_utils import map_children_to_sizes, map_drives_to_sizes
from ui_spinner import start_spinner, stop_spinner
import shutil
import os

def welcome_message():
    '''
    Displays the welcome message to the user.

    Returns:
        None
    '''

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

def _truncate_name(directory_name: str) -> str:
    '''
    Truncates a directory name to 26 characters.

    Args:
        directory_name: The name of the directory to truncate.

    Returns:
        A string representing the truncated directory name.
    '''

    cutoff = 26
    directory_name = directory_name[:cutoff] + "..."
    
    # If there is a space before "...", remove it -> looks cleaner
    if directory_name[-4] == " ":
        directory_name = directory_name[: -4] + "..."

    return directory_name

def _print_header(ui_state):
    '''
    Prints the layer and folder name above a table.

    Args:
        ui_state: An object containing the current UI state, including the current path.

    Returns:
        None
    '''

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


def _convert_to_readable(size) -> str:
    '''
    Converts bytes to human readable format.

    Args:
        size: The size in bytes or a string error indicator.

    Returns:
        A string representing the size in a human readable format.
    '''

    if size == "access_denied":
        return "X"
    
    # See dir_size.cpp "get_directory_size" func docstring for context
    if "*" in size:
        partial_calculation = True
        size = int(size.replace("*", ""))
    else:
        partial_calculation = False
        size = int(size)

    suffixes = ["Bytes", "KiB", "MiB", "GiB", "TiB", "PiB"]

    for suffix in suffixes:
        if size < 1024:
            break
        
        size = size / 1024
    
    if partial_calculation:
        return f"[green]{size:.3g} {suffix}"
    else:
        return f"{size:.3g} {suffix}"
    
def _split_rows(rows) -> list:
    '''
    Splits a list of rows into two columns.

    Args:
        rows: A list of rows to split.

    Returns:
        A list of rows split into two columns.
    '''

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

def _build_raw_mapping(ui_state: AppState) -> dict:
    """
    Builds and returns the list of directory entries to display in the UI.

    If the current path is empty, returns the list of system drives.
    Otherwise, returns the list of subdirectories and their sizes for the current directory.

    Args:
        ui_state: An object containing the current UI state, including the current path.

    Returns:
        A list representing drives or subdirectories with their sizes, suitable for display.
    """

    if not ui_state.current_path:
        dictionary = map_drives_to_sizes()
    else:
        directory = os.path.join(*ui_state.current_path)
        dictionary = map_children_to_sizes(directory)

    return dictionary

def _get_cache_or_build_mapping(ui_state: AppState) -> dict:
    '''
    Gets the cached mapping for the current path, or builds and caches it if it doesn't exist.

    Args:
        ui_state: An object containing the current UI state, including the current path.

    Returns:
        A dictionary representing the mapping of directory names to sizes.
    '''

    path_key = "\\".join(ui_state.current_path) if ui_state.current_path else "root"

    if ui_state.cache_has(path_key):
        return ui_state.cache_get(path_key)
    else:
        raw_mapping = _build_raw_mapping(ui_state)
        ui_state.cache_set(path_key, raw_mapping)
        return raw_mapping

def display_ui(ui_state: AppState) -> None:
    '''
    Displays the UI for the user.

    Args:
        ui_state: An object containing the current UI state, including the current path.

    Returns:
        None
    '''

    start_spinner()

    raw_mapping = _get_cache_or_build_mapping(ui_state)
    
    def sort_key(item):
        size = item[1]
        # See dir_size.cpp "get_directory_size" func docstring for context     
        return -1 if size == "access_denied" else int(size.replace("*", ""))

    sorted_items = sorted(raw_mapping.items(), key=sort_key, reverse=True)
    
    # Update user selections
    ui_state.selections = [name for name, _ in sorted_items]

    # Format items for display
    formatted_rows = []
    for index, (name, size) in enumerate(sorted_items):
        display_name = _truncate_name(name) if len(name) > 26 else name
        
        formatted_row = [
            f"[dim]{index + 1})[/dim] [cyan]{display_name}",
            _convert_to_readable(size)
        ]
        formatted_rows.append(formatted_row)

    console = Console()
    table = Table(show_header=False, box=ROUNDED)
    table.add_column("Folder Name")
    table.add_column("Size", style="white", justify="right")

    # Split into multiple columns if there are many items
    if len(formatted_rows) > 20:
        formatted_rows = _split_rows(formatted_rows)

        table.add_column("Folder Name")
        table.add_column("Size", style="white", justify="right")

    for row in formatted_rows:
        table.add_row(*row)

    stop_spinner()

    print("\n")
    _print_header(ui_state)
    print()
    console.print(Align.center(table))
    print("\n")