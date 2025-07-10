from display import navigate
import os
import time
import sys
from spinner import stop_spinner

def _handle_input(user_input, current_path, selections):
    if user_input.isdigit():
        index = int(user_input) - 1

        if 0 <= index < len(selections):
            try:
                selected_folder = selections[index]
                current_path.append(selected_folder)

                selections = navigate(current_path)
            except Exception:
                stop_spinner()
                os.system("cls")
                print("Can't access that folder. Returning to previous.")
                time.sleep(4)

                current_path.pop()
                selections = navigate(current_path)
        else:
            print("Invalid selection.")
    
    elif user_input == "b":
        if current_path:
            current_path.pop()
            selections = navigate(current_path)
        else:
            print("Already at root.")
    
    elif user_input == "/exit":
        return current_path, selections, True

    else:
        print("Invalid input.")

    return current_path, selections, False

def main():
    command_list = ["b", "options"]
    current_path = []
    user_input = None
    should_exit = False
    
    # Initial nav will put user 
    selections = navigate(current_path)

    while not should_exit:
        user_input = input(">>> ")

        current_path, selections, should_exit = _handle_input(user_input, current_path, selections)

if __name__ == "__main__":
    main()