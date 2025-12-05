def calculate_password():
    current_position = 50
    zero_count = 0

    with open("input.txt", "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            direction = line[0]
            distance = int(line[1:])

            if direction == "L":
                current_position -= distance
                if current_position < 0:
                    current_position += 100
            elif direction == "R":
                current_position += distance
                current_position %= 100

            if current_position == 0:
                zero_count += 1

    return zero_count


password = calculate_password()
print(password)
