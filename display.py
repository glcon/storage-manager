# Convert to human readable format
def readable(size):
    counter = 0
    suffixes = {
        0: "Bytes", 
        1: "KB",
        2: "MB",
        3: "GB",
        4: "TB"
    }

    while size >= 1000:
        size = size / 1000
        counter += 1
    
    # Bytes don't need decimals
    if counter == 0:
        return f"{size} {suffixes[counter]}"
    else:
        return f"{size:.2f} {suffixes[counter]}"
    
# Split output into 2 rows
def split_rows(rows):
    half = (len(rows) + 1) // 2  # Round up
    left_rows = rows[:half]
    right_rows = rows[half:]

    # If right row is shorter, pad with empty rows
    while len(right_rows) < len(left_rows):
        right_rows.append(["", ""])

    combined_rows = []
    for left, right in zip(left_rows, right_rows):
        combined_rows.append(left + right)

    return combined_rows