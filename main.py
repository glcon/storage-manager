from display import navigate
import os
import time
from ui_spinner import stop_spinner
from state import AppState

def _handle_input(ui_state, user_input):
    if user_input.isdigit():
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
    
    elif user_input == "b":
        if ui_state.current_path:
            ui_state.current_path.pop()
            navigate(ui_state)
        else:
            print("Already at root.")
    
    elif user_input == "/exit":
        ui_state.should_exit = True

    else:
        print("Invalid input.")

def main():    
    ui_state = AppState()
    navigate(ui_state)

    while not ui_state.should_exit:
        user_input = input(">>> ")

        _handle_input(ui_state, user_input)

if __name__ == "__main__":
    main()