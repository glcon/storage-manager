import commands
import time
from state import AppState
from ui_spinner import stop_spinner
from display import display_ui
import os

def _handle_command_input(ui_state: AppState, user_input: str) -> None:
    '''
    Handles command input.

    Args:
        ui_state: The current UI state.
        user_input: The user's input.
    '''

    if user_input in commands.command_list:
        # Function call
        commands.command_list[user_input](ui_state)
    else:
        print("Invalid command.")

def _handle_selection_input(ui_state: AppState, user_input: str) -> None:
    '''
    Handles selection input.

    Args:
        ui_state: The current UI state.
        user_input: The user's input.
    '''

    def _can_go_there(path: str) -> bool:
        '''
        Checks if the user can go to the given path.

        Args:
            path: The path to check.

        Returns:
            True if the user can go to the given path, False otherwise.
        '''

        try:
            # Check for access
            if not os.access(path, os.R_OK | os.X_OK):
                print("Can't access that folder. Permission denied.")
                return False

            # Check if it's actually a directory
            if not os.path.isdir(path):
                print("That's not a folder.")
                return False

            # Check if directory is empty
            if len(os.listdir(path)) == 0:
                print("Can't access that folder. It's empty.")
                return False
        except Exception as e:
            print(f"Error accessing folder: {e}")
            return False
        
        return True

    index = int(user_input) - 1

    if 0 <= index < len(ui_state.selections):
        selected_folder = ui_state.selections[index]
        new_path = os.path.join(*ui_state.current_path, selected_folder)

        if not _can_go_there(new_path):
            return

        # Try to go there
        try:
            ui_state.current_path.append(selected_folder)
            display_ui(ui_state)
        except Exception as e:
            stop_spinner()
            print(f"Error accessing folder: {e}")
            print("Returning to previous folder.")
            time.sleep(5)
            ui_state.current_path.pop()
            display_ui(ui_state)
    else:
        print("Invalid selection.")

def handle_input(ui_state: AppState, user_input: str) -> None:
    '''
    Handles user input.

    Args:
        ui_state: The current UI state.
        user_input: The user's input.
    '''

    if not user_input:
        print("No input provided.")
        return
    
    # Check if it's a command first
    if user_input in commands.command_list:
        _handle_command_input(ui_state, user_input)
        return

    # Check if it's a number (selection)
    if user_input.isdigit():
        _handle_selection_input(ui_state, user_input)
        return
    
    else:
        print("Invalid input.")