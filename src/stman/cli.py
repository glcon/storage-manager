from .display import display_ui, welcome_message
from .input_handler import handle_input
from .state import AppState
from .benchmark import run_benchmark
import platform
import sys

def main():
    if platform.system() != "Windows":
        raise RuntimeError("This package is only supported on Windows systems.")

    if len(sys.argv) == 3 and sys.argv[1] == "--benchmark":
        run_benchmark(sys.argv[2])
        return

    welcome_message()

    ui_state = AppState()
    display_ui(ui_state)

    while not ui_state.should_exit:
        user_input = input(">>> ").strip().lower()

        handle_input(ui_state, user_input)

if __name__ == "__main__":
    main()