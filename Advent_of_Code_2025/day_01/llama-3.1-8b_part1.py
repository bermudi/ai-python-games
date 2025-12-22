def count_zeroes(rotations):
    position = 50
    zero_count = 0

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == 'L':
            for _ in range(distance):
                position = (position - 1) % 100
                if position == 0:
                    zero_count += 1
        else:
            for _ in range(distance):
                position = (position + 1) % 100
                if position == 0:
                    zero_count += 1

    return zero_count


def main():
    with open('input.txt', 'r') as file:
        rotations = file.readlines()

    rotations = [line.strip() for line in rotations]
    rotations = [line for line in rotations if line]  # Remove empty lines

    password = count_zeroes(rotations)
    print(password)


if __name__ == "__main__":
    main()
