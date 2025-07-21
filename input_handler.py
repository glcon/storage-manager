import commands
import time
from ui_spinner import stop_spinner
from display import display_table

def _handle_command_input(ui_state, user_input):
    if user_input in commands.command_list:
        # Function call
        commands.command_list[user_input](ui_state)
    else:
        print("Invalid command.")

def _handle_selection_input(ui_state, user_input):
    index = int(user_input) - 1

    if 0 <= index < len(ui_state.selections):
        try:
            selected_folder = ui_state.selections[index]
            ui_state.current_path.append(selected_folder)

            display_table(ui_state)
        except Exception:
            stop_spinner()
            print("Can't access that folder. Returning to previous.")
            time.sleep(4)

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