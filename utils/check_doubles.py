# Open the file in read mode
with open("/data/home/acw507/music_recognition/data/GT.txt", "r") as f:
    # Read the lines into a list
    lines = f.readlines()

# Create an empty dictionary to keep track of lines
seen_lines = {}

# Loop over the lines
for i, line in enumerate(lines):
    # Strip whitespace and newline characters
    line = line.strip()

    # If the line has been seen before, increment the count
    if line in seen_lines:
        seen_lines[line] += 1
    # Otherwise, add the line to the dictionary
    else:
        seen_lines[line] = 1

# Loop over the dictionary and print any lines that have a count greater than 1
for line, count in seen_lines.items():
    if count > 1:
        print(count)