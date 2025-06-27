import os
import subprocess
import time

start = time.time()

# Initialize directory path
dir_path = None

def get_dir_size(dir_path):
    # Run powershell script with desired path as input
    process_var = subprocess.run(
        ["powershell", "-File", "dirSize.ps1", "-DirPath", dir_path],
        
        # .ps1 file outputs size in bytes, so capture it
        capture_output = True,
        text = True
    )

    # The shell can return spaces or newlines, exclude or "strip" them
    output = process_var.stdout.strip()
    
    # Sanity check, make sure output is a number
    if output.isdigit():
        return int(output)
    else:
        return 0
   
dir_path = "C:\\Program Files\\"

testing = get_dir_size(dir_path)

end = time.time()

print(testing, round(end - start, 2))
