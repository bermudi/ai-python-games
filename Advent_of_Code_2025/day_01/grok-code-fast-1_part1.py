# Read the input from input.txt
with open('input.txt', 'r') as file:
    rotations = file.readlines()

# Initialize position and count
position = 50
count = 0

# Process each rotation
for rotation in rotations:
    rotation = rotation.strip()
    direction = rotation[0]
    distance = int(rotation[1:])
    
    if direction == 'L':
        position = (position - distance) % 100
    elif direction == 'R':
        position = (position + distance) % 100
    
    if position == 0:
        count += 1

# Output the password
print(count)