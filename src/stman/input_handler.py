import commands
import time
from ui_spinner import stop_spinner
from display import display_table
import os

def _handle_command_input(ui_state, user_input):
    if user_input in commands.command_list:
        # Function call
        commands.command_list[user_input](ui_state)
    else:
        print("Invalid command.")

def _handle_selection_input(ui_state, user_input):
    index = int(user_input) - 1

    if 0 <= index < len(ui_state.selections):
        selected_folder = ui_state.selections[index]
        new_path = os.path.join(*ui_state.current_path, selected_folder)

        # Check for access
        if not os.access(new_path, os.R_OK | os.X_OK):
            print("Can't access that folder. Permission denied.")
            return

        # Try to go there
        try:
            ui_state.current_path.append(selected_folder)
            display_table(ui_state)
        except Exception as e:
            stop_spinner()
            print(f"Error accessing folder: {e}")
            print("Returning to previous folder.")
            time.sleep(5)
            ui_state.current_path.pop()
            display_table(ui_state)
    else:
        print("Invalid selection.")

def handle_input(ui_state, user_input):
    if not user_input:
        print("No input provided.")
        return
    
    if user_input.isalpha():
        _handle_command_input(ui_state, user_input)
        return

    if user_input.isdigit():
        _handle_selection_input(ui_state, user_input)
        return
    
    else:
        print("Invalid input.")