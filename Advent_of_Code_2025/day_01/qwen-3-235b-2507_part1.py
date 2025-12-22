# Read the input file
with open('input.txt', 'r') as file:
    rotations = file.readlines()

# Initial position
position = 50
zero_count = 0

for rotation in rotations:
    rotation = rotation.strip()
    if not rotation:
        continue

    direction = rotation[0]
    distance = int(rotation[1:])

    if direction == 'R':
        position = (position + distance) % 100
    elif direction == 'L':
        position = (position - distance) % 100

    # Check if current position is 0 after this rotation
    if position == 0:
        zero_count += 1

print("The password is:", zero_count)
