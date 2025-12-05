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

        # Count how many times we pass through 0 during this rotation
        if direction == "L":
            # Calculate how many full rotations we make
            full_rotations = distance // 100
            count += full_rotations

            # Check if we pass through 0 in the remaining rotation
            remaining = distance % 100
            if position < remaining:
                count += 1

            # Update the position
            position = (position - distance) % 100
        else:  # 'R'
            # Calculate how many full rotations we make
            full_rotations = distance // 100
            count += full_rotations

            # Check if we pass through 0 in the remaining rotation
            remaining = distance % 100
            if position + remaining >= 100:
                count += 1

            # Update the position
            position = (position + distance) % 100

        # Check if the dial is at 0 after the rotation
        if position == 0:
            count += 1

    # Return the count
    return count


# Call the function and print the result
print(solve())
