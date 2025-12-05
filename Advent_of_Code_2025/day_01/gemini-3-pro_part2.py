import math

# Read input_data from input.txt
try:
    with open("input.txt", "r") as f:
        input_data = f.read()
except FileNotFoundError:
    print(
        "Error: input.txt not found. Please create input.txt with the necessary data."
    )
    exit()

pos = 50
count = 0
lines = input_data.strip().split("\n")


for line in lines:
    line = line.strip()
    if not line:
        continue

    direction = line[0]
    val = int(line[1:])

    if direction == "R":
        start = pos
        end = pos + val
        # Range is (start, end].
        # number of multiples of 100 in (start, end]
        # = floor(end/100) - floor(start/100)
        c = math.floor(end / 100) - math.floor(start / 100)
        count += c
        pos = end % 100
        # Adjust pos if it becomes negative due to modulo of negative numbers in Python
        if pos < 0:
            pos += 100

    elif direction == "L":
        start = pos
        end = pos - val
        # Range is [end, start).
        # We are moving downwards from start to end.
        # We want to count multiples of 100 in [end, start).
        # The integers visited are start-1, start-2, ..., end.
        # Actually, let's stick to the range logic.
        # The set of integers touched is {start-1, start-2, ..., end}.
        # Range is [end, start-1].
        # number of multiples of 100 in [end, start-1]
        # = floor((start-1)/100) - floor((end-1)/100)
        c = math.floor((start - 1) / 100) - math.floor((end - 1) / 100)
        count += c
        pos = end % 100
        # Adjust pos if it becomes negative due to modulo of negative numbers in Python
        if pos < 0:
            pos += 100

print(f"{count=}")
