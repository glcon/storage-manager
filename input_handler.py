import os
import time
from ui_spinner import stop_spinner
from display import navigate

def _go_back(ui_state):
    if not ui_state.current_path:
        print("Already at root.")
    else:
        ui_state.current_path.pop()
        navigate(ui_state)

def _handle_command_input(ui_state, user_input):
    def exit(ui_state):
        ui_state.should_exit = True
        os.system("cls")

    def refresh(ui_state):
        navigate(ui_state)

    def help(_):
        os.system("cls")
        print("/exit        Exit the application")
        print("/refresh     Refresh the display")
        print("/help        Show this help message")
        print("b            Go back to previous folder")
        print("[number]     Open folder at that number")
        print("\n")
        input("Hit any key to return. ")
        navigate(ui_state)

    command_list = {
    "/exit": exit,
    "/refresh": refresh,
    "/help": help
    }

    if user_input in command_list:
        command_list[user_input](ui_state)
    else:
        print("Invalid command.")

def _handle_selection_input(ui_state, user_input):
    index = int(user_input) - 1

    if 0 <= index < len(ui_state.selections):
        try:
            selected_folder = ui_state.selections[index]
            ui_state.current_path.append(selected_folder)

            navigate(ui_state)
        except Exception:
            stop_spinner()
            print("Can't access that folder. Returning to previous.")
            time.sleep(4)

            ui_state.current_path.pop()
            navigate(ui_state)
    else:
        print("Invalid selection.")

def handle_input(ui_state, user_input):
    if not user_input:
        print("No input provided.")
        return
    
    if user_input.startswith("/"):
        _handle_command_input(ui_state, user_input)
        return

    if user_input.isdigit():
        _handle_selection_input(ui_state, user_input)
        return
    
    if user_input == "b":
        _go_back(ui_state)
        return
    
    else:
        print("Invalid input.")