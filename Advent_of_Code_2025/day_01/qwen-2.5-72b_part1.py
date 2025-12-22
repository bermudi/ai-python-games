def read_rotations(filename):
    with open(filename, 'r') as file:
        return file.readlines()

def rotate_dial(dial_position, rotation):
    direction, distance = rotation[0], int(rotation[1:])
    if direction == 'L':
        dial_position = (dial_position - distance) % 100
    elif direction == 'R':
        dial_position = (dial_position + distance) % 100
    return dial_position

def count_zero_positions(rotations):
    dial_position = 50
    zero_count = 0
    for rotation in rotations:
        dial_position = rotate_dial(dial_position, rotation.strip())
        if dial_position == 0:
            zero_count += 1
    return zero_count

def main():
    rotations = read_rotations('input.txt')
    password = count_zero_positions(rotations)
    print(f"The actual password is: {password}")

if __name__ == "__main__":
    main()
