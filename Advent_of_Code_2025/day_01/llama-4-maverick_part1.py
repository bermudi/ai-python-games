def main():
    try:
        with open('input.txt', 'r') as file:
            rotations = file.readlines()
        print(calculate_password(rotations))
    except FileNotFoundError:
        print("The file 'input.txt' was not found.")

def calculate_password(rotations):
    position = 50
    count = 0
    for rotation in rotations:
        rotation = rotation.strip()
        if rotation:
            direction = rotation[0]
            distance = int(rotation[1:])
            if direction == 'L':
                position = (position - distance) % 100
            elif direction == 'R':
                position = (position + distance) % 100
            if position == 0:
                count += 1
    return count

if __name__ == "__main__":
    main()
