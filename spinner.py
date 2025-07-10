import itertools
import threading
import sys
import time
import shutil

_spinner_stop_event = None
_spinner_thread = None

def _spinner_function(stop_event):
    spinner_cycle = itertools.cycle(['|', '/', '-', '\\'])
    width = shutil.get_terminal_size().columns

    # Hide cursor
    sys.stdout.write('\033[?25l')
    sys.stdout.flush()

    print('\n' * 2, end='')
    working_text = "Working"
    print(working_text.center(width))

    while not stop_event.is_set():
        spinner_char = next(spinner_cycle)

        sys.stdout.write('\r' + spinner_char.center(width))
        sys.stdout.flush()
        time.sleep(0.1)

    # Clear spinner line
    sys.stdout.write('\r' + ' ' * width + '\r')

    # Show cursor again
    sys.stdout.write('\033[?25h')
    sys.stdout.flush()

def start_spinner():
    global _spinner_stop_event, _spinner_thread

    if _spinner_thread and _spinner_thread.is_alive():
        return
    
    _spinner_stop_event = threading.Event()
    _spinner_thread = threading.Thread(target=_spinner_function, args=(_spinner_stop_event,), daemon=True)
    _spinner_thread.start()

def stop_spinner():
    global _spinner_stop_event, _spinner_thread

    if _spinner_stop_event:
        _spinner_stop_event.set()
        
    if _spinner_thread:
        _spinner_thread.join()