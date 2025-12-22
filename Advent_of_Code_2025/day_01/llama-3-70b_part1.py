def solve(input_file):
    with open(input_file, 'r') as f:
        rotations = [line.strip() for line in f.readlines()]

    dial = 50
    password = 0

    for rotation in rotations:
        direction, distance = rotation[0], int(rotation[1:])
        if direction == 'L':
            dial = (dial - distance) % 100
        else:
            dial = (dial + distance) % 100
        if dial == 0:
            password += 1

    return password

print(solve('input.txt'))
