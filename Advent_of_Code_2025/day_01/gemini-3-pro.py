pos = 50
count = 0

try:
    # Open the file in read mode
    with open('input.txt', 'r') as file:
        # Iterate over each line in the file directly
        for line in file:
            line = line.strip()
            if not line: continue
            
            direction = line[0]
            val = int(line[1:])
            
            if direction == 'R':
                pos = (pos + val) % 100
            elif direction == 'L':
                pos = (pos - val) % 100
            
            if pos == 0:
                count += 1

    print(f"{count=}")

except FileNotFoundError:
    print("Error: 'input.txt' file not found.")
except ValueError:
    print("Error: File contains invalid data format.")
