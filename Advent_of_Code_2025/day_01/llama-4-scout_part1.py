def main():
    with open("input.txt", "r") as f:
        rotations = [line.strip() for line in f]

    dial_position = 50
    password = 0

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == 'L':
            dial_position = (dial_position - distance) % 100
        elif direction == 'R':
            dial_position = (dial_position + distance) % 100

        if dial_position == 0:
            password += 1

    print(password)

if __name__ == "__main__":
    main()
