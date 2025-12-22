# Read the input file
with open('input.txt', 'r') as f:
    rotations = [line.strip() for line in f.readlines()]

# Start position
current = 50
count_zero = 0

for rotation in rotations:
    if not rotation:  # Skip empty lines
        continue
    direction = rotation[0]
    distance = int(rotation[1:])
    
    if direction == 'L':
        current = (current - distance) % 100
    elif direction == 'R':
        current = (current + distance) % 100
    
    # Check if after this rotation, the dial points to 0
    if current == 0:
        count_zero += 1

print(count_zero)
