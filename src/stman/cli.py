from display import display_ui, welcome_message
from input_handler import handle_input
from state import AppState

def main():
    welcome_message()

    ui_state = AppState()
    display_ui(ui_state)

    while not ui_state.should_exit:
        user_input = input(">>> ").strip().lower()

        handle_input(ui_state, user_input)

if __name__ == "__main__":
    main()