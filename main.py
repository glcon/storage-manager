from display import navigate
import os

def main():
    command_list = ["b", "options"]
    current_path = []
    user_input = None
    # Nav will return all subdirs the user can go into
    selections = navigate(current_path)

    while True:
        user_input = input(">>> ")

        if user_input.isdigit() and (int(user_input) - 1) in range(len(selections)):
            # Add to current path and go to that folder
            current_path.append(selections[int(user_input) - 1])
            
            selections = navigate(current_path)
        elif user_input == "b":
            # Go back
            current_path = current_path[:-1]
            selections = navigate(current_path)
        elif user_input == "/exit":
            break
        else:
            print("Invalid input.")


if __name__ == "__main__":
    main()