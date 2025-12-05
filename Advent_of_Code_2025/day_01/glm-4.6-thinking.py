def solve():
    # Read the input file
    with open("input.txt", "r") as f:
        rotations = f.readlines()

    # Initial position
    position = 50

    # Count of times the dial is at 0
    count = 0

    # Process each rotation
    for rotation in rotations:
        # Get the direction and distance
        direction = rotation[0]
        distance = int(rotation[1:])

        # Update the position based on the direction
        if direction == "L":
            position = (position - distance) % 100
        else:  # 'R'
            position = (position + distance) % 100

        # Check if the dial is at 0
        if position == 0:
            count += 1

    # Return the count
    return count


# Call the function and print the result
print(solve())
