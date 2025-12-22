def calculate_password():
    """
    Calculate the actual password to open the door.
    """
    position = 50
    password = 0

    with open('input.txt', 'r') as file:
        for line in file:
            rotation = line.strip()
            direction = rotation[0]
            distance = int(rotation[1:])

            if direction == 'L':
                position = (position - distance) % 100
            elif direction == 'R':
                position = (position + distance) % 100

            if position == 0:
                password += 1

    return password

# Example usage
password = calculate_password()
print(f"The actual password to open the door is: {password}")
