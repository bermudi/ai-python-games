def calculate_password(rotations):
    """
    Calculate the actual password to open the door.

    Args:
    rotations (list): A list of rotations, where each rotation is a string
                      in the format 'LX' or 'RX', where X is the distance.

    Returns:
    int: The actual password to open the door.
    """
    position = 50
    password = 0

    for rotation in rotations:
        direction, distance = rotation[0], int(rotation[1:])
        if direction == 'L':
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100

        if position == 0:
            password += 1

    return password


def main():
    with open('input.txt', 'r') as file:
        rotations = file.readlines()

    rotations = [rotation.strip() for rotation in rotations]
    password = calculate_password(rotations)

    print("The actual password to open the door is:", password)


if __name__ == "__main__":
    main()
