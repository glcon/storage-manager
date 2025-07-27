from display import display_table
import os
import messages
from pathlib import Path

def exit(ui_state):
    ui_state.should_exit = True
    os.system("cls")

def goto(ui_state):
    try:
        # Convert user path to list
        user_input = input("Enter a path: ")

        if len(user_input) == 2 and user_input[1] == ":":
            user_input += "\\"

        # Check if path exists
        if not os.path.exists(user_input):
            print("Path does not exist.")
            return

        desired_path = list(Path(user_input).parts)

        ui_state.current_path = desired_path
        display_table(ui_state)
    except Exception:
        print("Not a valid path.")
        return

def top(ui_state):
    if not ui_state.current_path:
        print("Already at root.")
    else:
        ui_state.current_path = []
        display_table(ui_state)

def go_back(ui_state):
    if not ui_state.current_path:
        print("Already at root.")
    else:
        ui_state.current_path.pop()
        display_table(ui_state)

def refresh(ui_state):
    path_key = "\\".join(ui_state.current_path) if ui_state.current_path else "root"
    ui_state.cache_library.pop(path_key, None)
    
    display_table(ui_state)

def help(ui_state):
    os.system("cls")

    print(messages.help_text)

    print("\n")
    input("Hit any key to return. ")
    display_table(ui_state)

def toggle_cnc(ui_state):
    ui_state.show_cnc = not ui_state.show_cnc

    if ui_state.show_cnc == False:
        print("Hiding uncalculatable folders.")
    else:
        print("Showing uncalculatable folders.")

def toggle_welcome(_):
    show_welcome_path = os.path.join(os.path.dirname(__file__), "show_welcome.txt")

    if not os.path.exists(show_welcome_path):
        print(f"\"{show_welcome_path}\" does not exist. Can't toggle.")
        return

    try:
        with open(show_welcome_path, "r") as f:
            current_value = f.read().strip().lower()

        if current_value == "yes":
            new_value = "no"
        elif current_value == "no":
            new_value = "yes"
        else:
            print("Invalid value in show_welcome.txt")
            return

        with open(show_welcome_path, "w") as f:
            f.write(new_value)

        if new_value == "no":
            print("Welcome message will be hidden.")
        elif new_value == "yes":
            print("Welcome message will display.")
    except (IOError, OSError) as e:
        print(f"Error toggling welcome message: {e}")
        return

def clear_cache(ui_state):
    ui_state.cache_clear()
    print("Cache cleared.")

command_list = {
"exit": exit,
"r": refresh,
"help": help,
"b": go_back,
"togglecnc": toggle_cnc,
"togglewelcome": toggle_welcome,
"top": top,
"goto": goto,
"clearcache": clear_cache
}