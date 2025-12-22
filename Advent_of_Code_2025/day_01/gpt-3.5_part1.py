# Read rotations from input.txt
with open('input.txt', 'r') as file:
    rotations = file.read().strip().split('\n')

# Initialize variables
dial_position = 50
zero_count = 0

# Simulate dial movements
for rotation in rotations:
    direction, distance = rotation[0], int(rotation[1:])
    
    if direction == 'L':
        dial_position = (dial_position - distance) % 100
    elif direction == 'R':
        dial_position = (dial_position + distance) % 100
    
    if dial_position == 0:
        zero_count += 1

# Print the password
print(zero_count)