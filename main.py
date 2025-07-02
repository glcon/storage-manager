from dir_utils import build_table as bt

def main():
    user_input = input("Enter a system path: ")
    
    try:
        print("\n" + bt(user_input) + "\n")
    except Exception:
        print("Couldn't find that path.")

if __name__ == "__main__":
    main()