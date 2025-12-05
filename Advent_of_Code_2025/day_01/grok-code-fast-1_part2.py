# Read the input from input.txt
with open('input.txt', 'r') as file:
    rotations = file.readlines()

# Initialize position and total count
position = 50
total = 0

# Process each rotation
for rotation in rotations:
    rotation = rotation.strip()
    direction = rotation[0]
    D = int(rotation[1:])
    step = -1 if direction == 'L' else 1
    clicked = []
    for i in range(1, D + 1):
        new_pos = (position + step * i) % 100
        clicked.append(new_pos)
    # Count zeros during the rotation (intermediate clicks)
    during_zeros = clicked[:-1].count(0)
    # Count zero at the end
    end_zero = 1 if clicked[-1] == 0 else 0
    total += during_zeros + end_zero
    # Update position
    position = clicked[-1]

# Output the password
print(total)
