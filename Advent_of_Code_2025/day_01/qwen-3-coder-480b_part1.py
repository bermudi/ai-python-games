# Read input from file
with open("input.txt", "r") as f:
    lines = f.read().strip().split("\n")

# Initial position of the dial
position = 50
count_zeros = 0

# Process each rotation
for line in lines:
    direction = line[0]
    distance = int(line[1:])
    
    if direction == 'L':
        position = (position - distance) % 100
    elif direction == 'R':
        position = (position + distance) % 100
    
    # Check if current position is 0
    if position == 0:
        count_zeros += 1

# Print the result
print(count_zeros)
