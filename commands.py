import os
from display import display_table

def exit(ui_state):
    ui_state.should_exit = True
    os.system("cls")

def go_back(ui_state):
    if not ui_state.current_path:
        print("Already at root.")
    else:
        ui_state.current_path.pop()
        display_table(ui_state)

def refresh(ui_state):
    display_table(ui_state)

def help(ui_state):
    os.system("cls")
    print("exit                Exit the application")
    print("r                   Refresh the display")
    print("help                Show this help message")
    print("togglecnc           Hide/show files whose size can't be found")
    print("b                   Go back to previous folder")
    print("togglewelcome       Hide/show startup welcome message")
    print("[number]            Open folder at that number")
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
    filename = "show_welcome.txt"

    if not os.path.exists(filename):
        print(f"\"{filename}\" does not exist. Can't toggle.")
        return

    with open(filename, "r") as f:
        current = f.read().strip().lower()

    if current == "yes":
        new_value = "no"
    elif current == "no":
        new_value = "yes"
    else:
        print(f"Unexpected value in \"{filename}\": Defaulting to 'no'.")
        new_value = "no"

    with open(filename, "w") as f:
        f.write(new_value)

    print(f"Welcome message toggled to: {new_value}")

command_list = {
"exit": exit,
"r": refresh,
"help": help,
"b": go_back,
"togglecnc": toggle_cnc,
"togglewelcome": toggle_welcome
}