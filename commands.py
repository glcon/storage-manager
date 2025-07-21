import os
from display import navigate

def exit(ui_state):
    ui_state.should_exit = True
    os.system("cls")

def refresh(ui_state):
    navigate(ui_state)

def help(ui_state):
    os.system("cls")
    print("/exit          Exit the application")
    print("/refresh       Refresh the display")
    print("/help          Show this help message")
    print("/togglecnc     Turns on/off displaying files whose size can't be found.")
    print("b              Go back to previous folder")
    print("[number]       Open folder at that number")
    print("\n")
    input("Hit any key to return. ")
    navigate(ui_state)

def toggle_cnc(ui_state):
    ui_state.show_cnc = not ui_state.show_cnc

    if ui_state.show_cnc == False:
        print("Hiding uncalculatable folders.")
    else:
        print("Showing uncalculatable folders.")

command_list = {
"/exit": exit,
"/refresh": refresh,
"/help": help,
"/togglecnc": toggle_cnc
}