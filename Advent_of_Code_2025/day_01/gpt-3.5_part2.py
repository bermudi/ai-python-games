# Read rotations from input.txt
with open('input.txt', 'r') as file:
    rotations = file.read().strip().split('\n')

# Initialize variables
dial_position = 50
zero_count = 0

# Simulate dial movements
for rotation in rotations:
    direction, distance = rotation[0], int(rotation[1:])
    
    for _ in range(distance):
        if dial_position == 0:
            zero_count += 1
        
        if direction == 'L':
            dial_position = (dial_position - 1) % 100
        elif direction == 'R':
            dial_position = (dial_position + 1) % 100

# Print the password using the new method
print(zero_count)
